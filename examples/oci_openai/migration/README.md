
---

## OCI GenAI Conversation Migration – Quick Instructions

### 1 Prepare Conversation IDs

You can provide conversation IDs in **two ways**:

1. **Comma-separated** via CLI:

```text
conv_123,conv_456,conv_789
```

2. **File input** – one conversation ID per line, e.g., `convs.txt`:

```text
conv_123
conv_456
conv_789
```

---

### 2 Run the Migration

**Basic Example:**

```bash
python migrate_conversations.py \
  --region us-chicago-1 \
  --profile BoatOc1 \
  --compartment-id ocid1.compartment.oc1..xxx \
  --project-id ocid1.generativeaiproject.oc1..xxx \
  --conversation-store-id ocid1.conversationstore.oc1..xx \
  --conversations conv_123,conv_456
```

**Or using a file:**

```bash
python migrate_conversations.py \
  --region us-chicago-1 \
  --profile BoatOc1 \
  --compartment-id ocid1.compartment.oc1..xxx \
  --project-id ocid1.generativeaiproject.oc1..xxx \
  --conversation-store-id ocid1.conversationstore.oc1..xx \
  --conv-file convs.txt
```

---

### 3 Dry Run (Optional)

To check inputs without actually migrating:

```bash
python migrate_conversations.py ... --dry-run
```

---

### 4 Output

After running, you will see:

```
conv_123 → new_conv_id_abc
conv_456 → new_conv_id_def
```

✅ Successfully migrated conversations or `None` if migration failed.

---
