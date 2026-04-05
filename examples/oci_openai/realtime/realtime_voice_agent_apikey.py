# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""
Realtime Voice Agent example with API key authentication.

Connects via WebSocket, sends a WAV audio file, prints xAI's transcription
and voice response, and saves the response audio to response.wav.

Setup:
    1. pip install websockets
    2. Update ENDPOINT, MODEL, API_KEY below
    3. python realtime_voice_agent_apikey.py path/to/audio.wav
       (WAV must be 24kHz PCM16 mono)
"""

import asyncio
import base64
import json
import struct
import sys

import websockets

ENDPOINT = "wss://inference.generativeai.us-chicago-1.oci.oraclecloud.com"
MODEL = "xai.grok-voice-agent"
API_KEY = "<YOUR_API_KEY>"

CHUNK_SIZE = 3200
CHUNK_DELAY = 0.05
RESPONSE_TIMEOUT = 30
OUTPUT_WAV = "response.wav"
SAMPLE_RATE = 24000
WAV_HEADER_SIZE = 44


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


async def run(wav_path):
    print("Realtime Voice Agent — API Key Auth")

    ws_url = f"{ENDPOINT}/openai/v1/realtime?model={MODEL}"
    print(f"Connecting to: {ws_url}")

    headers = {"Authorization": f"Bearer {API_KEY}"}

    with open(wav_path, "rb") as f:
        wav_bytes = f.read()
    pcm_bytes = wav_bytes[WAV_HEADER_SIZE:]
    audio_base64 = base64.b64encode(pcm_bytes).decode()

    transcript_fragments = []
    audio_fragments = []
    input_transcript = None

    async with websockets.connect(ws_url, additional_headers=headers) as ws:
        print("WebSocket connected")

        msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=10))
        if msg.get("type") != "conversation.created":
            raise RuntimeError(f"Expected conversation.created, got {msg.get('type')}")
        print("Session created")

        offset = 0
        chunk_count = 0
        while offset < len(audio_base64):
            end = min(offset + CHUNK_SIZE, len(audio_base64))
            chunk = audio_base64[offset:end]
            await ws.send(json.dumps({"type": "input_audio_buffer.append", "audio": chunk}))
            offset = end
            chunk_count += 1
            await asyncio.sleep(CHUNK_DELAY)
        print(f"Streamed {chunk_count} audio chunks ({len(pcm_bytes)} bytes)")

        await asyncio.sleep(0.5)
        await ws.send(json.dumps({"type": "input_audio_buffer.commit"}))
        await ws.send(
            json.dumps(
                {
                    "type": "response.create",
                    "response": {"modalities": ["text", "audio"]},
                }
            )
        )
        print("Sent commit + response.create")

        async for raw in ws:
            msg = json.loads(raw)
            event_type = msg.get("type", "unknown")

            if event_type == "conversation.item.input_audio_transcription.completed":
                input_transcript = msg.get("transcript", "")
                print(f"Input transcription: {input_transcript}")

            elif event_type == "response.output_audio_transcript.delta":
                transcript_fragments.append(msg.get("delta", ""))

            elif event_type == "response.output_audio.delta":
                audio_fragments.append(msg.get("delta", ""))

            elif event_type == "response.done":
                break

            elif event_type == "error":
                print(f"Server error: {msg}", file=sys.stderr)
                break

        if transcript_fragments:
            print(f"Voice response: {''.join(transcript_fragments)}")
        if audio_fragments:
            print(f"Received {len(audio_fragments)} audio fragments")
            write_response_audio(audio_fragments)

        print("Connection closed")


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python realtime_voice_agent_apikey.py <path-to-wav-file>",
            file=sys.stderr,
        )
        sys.exit(1)
    asyncio.run(run(sys.argv[1]))


if __name__ == "__main__":
    main()
