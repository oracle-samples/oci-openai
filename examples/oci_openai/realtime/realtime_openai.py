# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""
Realtime Voice Agent example with OCI IAM or API key authentication.

Connects via WebSocket, sends a WAV audio file, prints xAI's transcription
and voice response, and saves the response audio to response.wav.

Setup:
    1. pip install websockets oci
    2. For IAM: oci session authenticate --profile-name DEFAULT
    3. Update AUTH_MODE, ENDPOINT, MODEL, COMPARTMENT_ID, PROFILE_NAME, API_KEY below
    4. python realtime_openai.py path/to/audio.wav
       (WAV must be 24kHz PCM16 mono)
"""

import asyncio
import base64
import json
import struct
import sys

import oci
import oci.auth.signers
import oci.config
import oci.signer
import requests
import websockets

ENDPOINT = "wss://inference.generativeai.us-chicago-1.oci.oraclecloud.com"
MODEL = "openai.gpt-realtime"
AUTH_MODE = "IAM"  # "IAM" or "API_KEY"
COMPARTMENT_ID = (
    "ocid1.compartment.oc1..your_compartment_id"
)
PROFILE_NAME = "oc1"
CONFIG_FILE = "~/.oci/config"
API_KEY = "<YOUR_API_KEY>"

CHUNK_SIZE = 3200
CHUNK_DELAY = 0.05
RESPONSE_TIMEOUT = 30
OUTPUT_WAV = "response.wav"
SAMPLE_RATE = 24000
WAV_HEADER_SIZE = 44
SESSION_INIT_EVENTS = {"session.created"}


class RealtimeState:
    def __init__(self):
        self.events_received = set()
        self.transcript_fragments = []
        self.audio_fragments = []
        self.input_transcript = None


def generate_signed_headers(signer, uri):
    """Sign a GET request and return the headers."""
    https_url = uri.replace("wss://", "https://").replace("ws://", "http://")
    req = requests.Request("GET", https_url)
    prepared = req.prepare()
    signer.do_request_sign(prepared)
    return dict(prepared.headers)


def build_auth_headers(ws_url):
    auth_mode = AUTH_MODE.upper()

    if auth_mode == "IAM":
        config = oci.config.from_file(CONFIG_FILE, PROFILE_NAME)
        token_file = config["security_token_file"]
        with open(token_file) as f:
            token = f.read().strip()
        private_key = oci.signer.load_private_key_from_file(config["key_file"])
        signer = oci.auth.signers.SecurityTokenSigner(token, private_key)

        headers = generate_signed_headers(signer, ws_url)
        headers["opc-compartment-id"] = COMPARTMENT_ID
        return headers

    if auth_mode == "API_KEY":
        if not API_KEY or API_KEY == "<YOUR_API_KEY>":
            raise ValueError("Set API_KEY before using API_KEY auth mode")
        return {"Authorization": f"Bearer {API_KEY}"}

    raise ValueError(f"Unsupported AUTH_MODE: {AUTH_MODE}")


def write_response_audio(audio_fragments):
    """Write base64 audio fragments to a WAV file."""
    pcm_data = b"".join(base64.b64decode(f) for f in audio_fragments)
    with open(OUTPUT_WAV, "wb") as f:
        header = struct.pack(
            "<4sI4s4sIHHIIHH4sI",
            b"RIFF",
            36 + len(pcm_data),
            b"WAVE",
            b"fmt ",
            16,
            1,
            1,
            SAMPLE_RATE,
            SAMPLE_RATE * 2,
            2,
            16,
            b"data",
            len(pcm_data),
        )
        f.write(header)
        f.write(pcm_data)
    print(f"Saved response audio to {OUTPUT_WAV} ({len(pcm_data)} bytes)")


def handle_message(raw, state):
    msg = json.loads(raw)
    event_type = msg.get("type", "unknown")
    state.events_received.add(event_type)

    if event_type == "conversation.item.input_audio_transcription.completed":
        state.input_transcript = msg.get("transcript", "")

    elif event_type == "response.output_audio_transcript.delta":
        state.transcript_fragments.append(msg.get("delta", ""))

    elif event_type == "response.output_audio.delta":
        state.audio_fragments.append(msg.get("delta", ""))

    elif event_type == "error":
        raise RuntimeError(f"Server error: {msg}")

    return event_type


async def wait_for_message(ws, state, event_matches, timeout, timeout_name):
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout

    while True:
        remaining = deadline - loop.time()
        if remaining <= 0:
            raise TimeoutError(f"Timed out waiting for '{timeout_name}'")

        try:
            raw = await asyncio.wait_for(ws.recv(), timeout=remaining)
        except asyncio.TimeoutError as exc:
            raise TimeoutError(f"Timed out waiting for '{timeout_name}'") from exc

        event_type = handle_message(raw, state)
        if event_matches(event_type):
            return event_type


async def wait_for_session_init(ws, state, timeout):
    if state.events_received.intersection(SESSION_INIT_EVENTS):
        return

    await wait_for_message(
        ws,
        state,
        lambda event_type: event_type in SESSION_INIT_EVENTS,
        timeout,
        "session init",
    )


async def wait_for_event(ws, state, event_type, timeout):
    if event_type in state.events_received:
        return

    await wait_for_message(
        ws,
        state,
        lambda received_event_type: received_event_type == event_type,
        timeout,
        event_type,
    )


async def run(wav_path):
    print(f"Realtime Voice Agent — {AUTH_MODE.upper()} Auth")

    ws_url = f"{ENDPOINT}/openai/v1/realtime?model={MODEL}"
    print(f"Connecting to: {ws_url}")

    headers = build_auth_headers(ws_url)

    with open(wav_path, "rb") as f:
        wav_bytes = f.read()
    pcm_bytes = wav_bytes[WAV_HEADER_SIZE:]
    audio_base64 = base64.b64encode(pcm_bytes).decode()

    state = RealtimeState()

    async with websockets.connect(ws_url, additional_headers=headers) as ws:
        print("WebSocket connected")

        await wait_for_session_init(ws, state, 10)
        print("Session created")

        if MODEL.startswith("openai."):
            session_update = {
                "type": "session.update",
                "session": {
                    "type": "realtime",
                    "audio": {
                        "input": {
                            "transcription": {
                                "model": "gpt-4o-transcribe",
                            }
                        }
                    },
                },
            }
            await ws.send(json.dumps(session_update))
            print("Sent session.update to enable input audio transcription for OpenAI")

        offset = 0
        chunk_count = 0
        while offset < len(audio_base64):
            end = min(offset + CHUNK_SIZE, len(audio_base64))
            chunk = audio_base64[offset:end]
            print(f"Streamed {chunk_count} audio chunk length {end - offset}")
            await ws.send(json.dumps({"type": "input_audio_buffer.append", "audio": chunk}))
            offset = end
            chunk_count += 1
            await asyncio.sleep(CHUNK_DELAY)
        print(f"Streamed {chunk_count} audio chunks ({len(pcm_bytes)} bytes)")

        await asyncio.sleep(0.5)
        print("Finished streaming audio; waiting for server-side VAD response")

        await wait_for_event(
            ws,
            state,
            "conversation.item.input_audio_transcription.completed",
            RESPONSE_TIMEOUT,
        )
        print(f"Input transcription: {state.input_transcript}")

        await wait_for_event(ws, state, "response.output_audio_transcript.delta", RESPONSE_TIMEOUT)
        await wait_for_event(ws, state, "response.output_audio.delta", RESPONSE_TIMEOUT)
        await wait_for_event(ws, state, "response.done", RESPONSE_TIMEOUT)

        print(f"Voice response: {''.join(state.transcript_fragments)}")
        print(f"Received {len(state.audio_fragments)} audio fragments")
        write_response_audio(state.audio_fragments)

        await ws.close(code=1000, reason="done")
        print("Connection closed")


def main():
    if len(sys.argv) < 2:
        print("Usage: python realtime_openai.py <path-to-wav-file>", file=sys.stderr)
        sys.exit(1)
    asyncio.run(run(sys.argv[1]))


if __name__ == "__main__":
    main()
