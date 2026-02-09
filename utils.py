CHUNK_SIZE = 4096   # 4KB
PADDING = 256

def chunk_text(text: str) -> list[str]:
    data = text.encode("utf-8")
    chunks = []

    start = 0
    n = len(data)

    while start < n:
        end = min(start + CHUNK_SIZE, n)

        # ensure valid UTF-8, avoid breaking characters in half.
        while end > start:
            try:
                piece = data[start:end].decode("utf-8")
                break
            except UnicodeDecodeError:
                end -= 1

        chunks.append(piece)
        start += CHUNK_SIZE - PADDING

    return chunks

def merge_parts(parts: list[dict], schema: dict[str, str] | list[str]):
    """
    Merge chunk-level GLiNER2 outputs into a single result.

    Confidence is aggregated using a running average.
    """
    if isinstance(schema, dict):
        entity_types = schema.keys()
    else:
        entity_types = schema 

    # Internal accumulator:
    # { entity_type: { text: {"avg_conf": float, "count": int} } }
    acc = {
        etype: {} for etype in entity_types
    }

    for part in parts:
        entities = part["entities"]

        for etype in entity_types:
            for item in entities.get(etype, []):
                text = item["text"]
                conf = item["confidence"]

                if text not in acc[etype]:
                    acc[etype][text] = {
                        "avg_conf": conf,
                        "count": 1,
                    }
                else:
                    prev = acc[etype][text]
                    new_count = prev["count"] + 1
                    prev["avg_conf"] = (
                        (prev["avg_conf"] * prev["count"] + conf) / new_count
                    )
                    prev["count"] = new_count

    # Reconstruct final output shape from accumulator
    merged_entities = {}

    for etype, texts in acc.items():
        merged_entities[etype] = [
            {
                "text": text,
                "confidence": data["avg_conf"],
            }
            for text, data in texts.items()
        ]

    return {"entities": merged_entities}
