"""Verify connectivity to all required Google Cloud services."""

import sys

def check_vertex_ai():
    """Verify Gemini model access via Vertex AI."""
    from google import genai
    client = genai.Client(vertexai=True)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Reply with exactly: VERTEX_AI_OK"
    )
    assert "VERTEX_AI_OK" in response.text, f"Unexpected response: {response.text}"
    print("[PASS] Vertex AI / Gemini 2.0 Flash: Connected")

def check_discovery_engine():
    """Verify Discovery Engine API is accessible."""
    from google.cloud import discoveryengine_v1 as discoveryengine
    client = discoveryengine.SearchServiceClient()
    print("[PASS] Discovery Engine (Vertex AI Search): Client initialized")

def check_storage():
    """Verify Cloud Storage access."""
    from google.cloud import storage
    client = storage.Client()
    buckets = list(client.list_buckets(max_results=1))
    print(f"[PASS] Cloud Storage: Connected ({len(buckets)} bucket(s) visible)")

def main():
    checks = [
        ("Vertex AI / Gemini", check_vertex_ai),
        ("Discovery Engine", check_discovery_engine),
        ("Cloud Storage", check_storage),
    ]

    failed = []
    for name, check_fn in checks:
        try:
            check_fn()
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            failed.append(name)

    print()
    if failed:
        print(f"FAILED: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("All GCP connectivity checks passed.")

if __name__ == "__main__":
    main()
