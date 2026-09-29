import asyncio
import edge_tts
import os

OUTPUT_DIR = "audio"
VOICE = "en-US-JennyNeural"

# New terms specific to Lecture 2 (ANS)
TERMS = [
    "Autonomic Ganglia",
    "Preganglionic fiber",
    "Postganglionic fiber",
    "Varicosity",
    "Effector organ",
    "Paravertebral Ganglia",
    "Collateral Ganglia",
    "Terminal Ganglia",
    "Sympathetic Nervous System",
    "Parasympathetic Nervous System",
    "Thoracolumbar",
    "Sympathetic Chain",
    "Sympathetic Trunk",
    "Mydriasis",
    "Miosis",
    "Dilator Pupillae Muscle",
    "Palpebral Fissure",
    "Lacrimal Gland",
    "Salivary Glands",
    "Inotropic Effect",
    "Chronotropic Effect",
    "Coronary Vessels",
    "Vasodilatation",
    "Vasoconstriction",
    "Bronchodilatation",
    "Bronchoconstriction",
    "Pulmonary Vessels",
    "Fight or Flight",
    "Rest and Digest",
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def generate_audio(term: str):
    safe_name = term.lower().replace(" ", "_")
    safe_name = "".join(c for c in safe_name if c.isalnum() or c == "_")
    out_path = os.path.join(OUTPUT_DIR, f"{safe_name}.mp3")

    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        print(f"[SKIP] {term} (already exists)")
        return

    try:
        communicate = edge_tts.Communicate(term, VOICE, rate="-10%")
        await communicate.save(out_path)
        size = os.path.getsize(out_path)
        print(f"[OK]   {term} ({size:,} bytes)")
    except Exception as e:
        print(f"[FAIL] {term}: {e}")

async def main():
    for term in TERMS:
        await generate_audio(term)
    print(f"\nDone! Generated audio files in ./{OUTPUT_DIR}/")

if __name__ == "__main__":
    asyncio.run(main())
