import asyncio
import edge_tts
import os

OUTPUT_DIR = "audio"
VOICE = "en-US-JennyNeural"

TERMS = [
    "Macroanatomy",
    "Microanatomy",
    "Crown",
    "Neck",
    "Cervix",
    "Cervical line",
    "Root",
    "Roots",
    "Enamel",
    "Dentin",
    "Pulp",
    "Cementum",
    "Pulp cavity",
    "Pulp chamber",
    "Pulp horns",
    "Pulp canal",
    "Root canal",
    "Anatomical crown",
    "Clinical crown",
    "Anatomical root",
    "Clinical root",
    "Gingiva",
    "Gingival sulcus",
    "Periodontal ligament",
    "Crypt",
    "Unerupted tooth",
    "Posterior tooth",
    "Anterior tooth",
    "Calcified tissues",
    "Soft tissue",
    "Connective tissue",
    "Sensory system",
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def generate_audio(term: str):
    safe_name = term.lower().replace(" ", "_").replace("-", "_")
    safe_name = "".join(c for c in safe_name if c.isalnum() or c == "_")
    out_path = os.path.join(OUTPUT_DIR, f"{safe_name}.mp3")

    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        print(f"[SKIP] {term}")
        return

    try:
        communicate = edge_tts.Communicate(term, VOICE, rate="-10%")
        await communicate.save(out_path)
        size = os.path.getsize(out_path)
        print(f"[OK] {term} ({size:,} bytes)")
    except Exception as e:
        print(f"[FAIL] {term}: {e}")

async def main():
    for term in TERMS:
        await generate_audio(term)
    print(f"\nDone! Generated all audio files in {OUTPUT_DIR}")

if __name__ == "__main__":
    asyncio.run(main())
