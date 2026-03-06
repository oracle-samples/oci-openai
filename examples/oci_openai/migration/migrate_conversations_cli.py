#!/usr/bin/env python3

import time
import argparse
from oci_openai import OciOpenAI, OciSessionAuth

# --------------------------------------------------
# Fetch ALL messages from one conversation (with pagination)
# --------------------------------------------------
def get_all_items(client, conv_id):
    all_items = []
    start = None

    while True:
        params = {"limit": 100}
        if start:
            params["start"] = start

        resp = client.conversations.items.list(conv_id, **params)

        items = getattr(resp, "data", [])
        has_more = getattr(resp, "has_more", False)
        last_id = getattr(resp, "last_id", None)

        all_items.extend(items)

        if not has_more:
            break
        if not last_id:
            print("⚠️ Warning: has_more=True but no last_id. Stop paging.")
            break

        start = last_id
        time.sleep(0.1)

    return all_items


# --------------------------------------------------
# Main Migration Function
# --------------------------------------------------
def migrate_conversations(conv_ids, project_id, store_id, region, profile, compartment_id, chunk_size=20, dry_run=False):
    # --------------------------------------------------
    # Source Client (Conversation Store)
    # --------------------------------------------------
    client_src = OciOpenAI(
        service_endpoint=f"https://inference.generativeai.{region}.oci.oraclecloud.com",
        auth=OciSessionAuth(profile_name=profile),
        compartment_id=compartment_id,
        default_headers={
            "opc-conversation-store-id": store_id,
            "opc-compartment-id": compartment_id
        },
    )

    # --------------------------------------------------
    # Destination Client (Project)
    # --------------------------------------------------
    client_dst = OciOpenAI(
        service_endpoint=f"https://inference.generativeai.{region}.oci.oraclecloud.com",
        auth=OciSessionAuth(profile_name=profile),
        compartment_id=compartment_id,
        default_headers={
            "OpenAI-Project": project_id
        },
    )

    results = {}

    for conv_id in conv_ids:
        print(f"🔄 Migrating: {conv_id}")

        try:
            # 1. Fetch source messages
            source_items = get_all_items(client_src, conv_id)
            print(f"   → Fetched {len(source_items)} items")

            if not source_items:
                print("   ⚠️ No messages, skipping\n")
                results[conv_id] = None
                continue

            if dry_run:
                print("   → Dry run mode: skipping creation/replay")
                results[conv_id] = "dry_run"
                continue

            # 2. Create new conversation
            new_conv = client_dst.conversations.create(
                metadata={"original_conversation_id": conv_id},
                items=[]
            )
            new_id = new_conv.id
            print(f"   → Created new conversation: {new_id}")

            # 3. Append messages in batches
            for i in range(0, len(source_items), chunk_size):
                chunk = source_items[i:i + chunk_size]
                client_dst.conversations.items.create(new_id, items=chunk)
                time.sleep(0.05)

            print(f"   ✅ Success: {conv_id} → {new_id}\n")
            results[conv_id] = new_id

        except Exception as e:
            print(f"   ❌ Failed: {e}\n")
            results[conv_id] = None

    return results


# --------------------------------------------------
# CLI
# --------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="OCI GenAI Conversation Store → Project Migration CLI"
    )
    parser.add_argument("--region", required=True, help="OCI region, e.g., us-chicago-1")
    parser.add_argument("--profile", default="BoatOc1", help="OCI config profile")
    parser.add_argument("--compartment-id", required=True, help="Compartment or tenancy OCID")
    parser.add_argument("--project-id", required=True, help="Target GenAI Project OCID")
    parser.add_argument("--conversation-store-id", required=True, help="Source Conversation Store OCID")
    parser.add_argument("--conversations", help="Comma-separated conversation IDs")
    parser.add_argument("--conv-file", help="File containing conversation IDs (one per line)")
    parser.add_argument("--dry-run", action="store_true", help="Do not actually migrate, just validate")
    return parser.parse_args()


def load_conversation_ids(args):
    conv_ids = []

    if args.conversations:
        conv_ids.extend([c.strip() for c in args.conversations.split(",") if c.strip()])

    if args.conv_file:
        with open(args.conv_file, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    conv_ids.append(line)

    if not conv_ids:
        raise ValueError("No conversation IDs provided via --conversations or --conv-file")

    return list(set(conv_ids))  # remove duplicates


if __name__ == "__main__":
    args = parse_args()
    conv_ids = load_conversation_ids(args)

    print("🚀 Starting conversation migration...\n")
    results = migrate_conversations(
        conv_ids=conv_ids,
        project_id=args.project_id,
        store_id=args.conversation_store_id,
        region=args.region,
        profile=args.profile,
        compartment_id=args.compartment_id,
        chunk_size=20,
        dry_run=args.dry_run
    )

    print("\n===================================")
    print("🎉 Migration Finished")
    print("===================================")
    for old_id, new_id in results.items():
        print(f"{old_id} → {new_id}")