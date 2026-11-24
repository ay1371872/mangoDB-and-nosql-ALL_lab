import sys
sys.path.insert(0, "llm")
from rag_engine import generate_chat_response

queries = [
    "is antigravity installed ?",
    "is claude installed ?",
    "is ollama installed ?",
    "is python installed ?",
    "is vscode installed ?",
    "is git installed ?",
    "is docker installed ?",
    "is mongodb installed ?",
    "is chrome installed ?",
    "tell me about my cpu",
    "how much ram do i have ?",
    "what is my battery percentage ?",
    "what is my operating system ?",
    "what is my gpu ?",
    "what is my disk space ?",
    "what processes are running ?",
    "who made this project ?"
]

print("=" * 60)
print("RUNNING BATCH VERIFICATION SUITE")
print("=" * 60)

for q in queries:
    res = generate_chat_response(q, session_id="test-session")
    model_tag = res.get("model_used")
    resp_text = res.get("response", "")
    print(f"\nQUERY: {q}")
    print(f"ENGINE: {model_tag}")
    print("RESPONSE:")
    print(resp_text)
    print("-" * 50)

print("\nALL QUERIES EVALUATED SUCCESSFULLY!")
