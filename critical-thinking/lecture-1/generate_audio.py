import asyncio
import edge_tts
import os

OUTPUT_DIR = "audio"
VOICE = "en-US-JennyNeural"

TERMS = [
    "Critical Thinking",
    "Analysis",
    "Evaluation",
    "Inference",
    "Question",
    "Purpose",
    "Point of View",
    "Information",
    "Concepts",
    "Assumptions",
    "Consequences",
    "Critical Thinkers",
    "Uncritical Thinkers",
    "Plausible",
    "Validity",
    "Claim",
    "Fact",
    "Opinion",
    "Argument",
    "Assumption",
    "Snap Decisions",
    "Narrow Thinking",
    "Sprawling Thinking",
    "Fuzzy Thinking",
    "Examine",
    "Explore",
    "Evaluate",
    "Pros and Cons",
    "Objectively",
    "Rationally"
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def generate_audio(term: str):
    safe_name = term.lower().replace(" ", "_")
    safe_name = "".join(c for c in safe_name if c.isalnum() or c == "_")
    out_path = os.path.join(OUTPUT_DIR, f"{safe_name}.mp3")

    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        return

    try:
        communicate = edge_tts.Communicate(term, VOICE)
        await communicate.save(out_path)
        print(f"[OK] {term} -> {safe_name}.mp3")
    except Exception as e:
        print(f"[FAIL] {term}: {e}")

async def main():
    for term in TERMS:
        await generate_audio(term)
    print(f"Generated {len(os.listdir(OUTPUT_DIR))} audio files.")

if __name__ == "__main__":
    asyncio.run(main())
