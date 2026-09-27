import asyncio
import edge_tts
import os

OUTPUT_DIR = "entrepreneurship/lecture-1/audio"
VOICE = "en-US-JennyNeural"  # Clear, professional American female voice

TERMS = [
    "Innovation",
    "Entrepreneurship",
    "Entrepreneur",
    "Manager",
    "Risk-taking",
    "Motivation",
    "Leadership",
    "Decision-making",
    "Management",
    "Planning",
    "Vision",
    "Organization",
    "Vision and Passion",
    "Innovative",
    "Risk Taker",
    "Leader",
    "Persistent",
    "Ethical",
    "Competitive Spirit",
    "Resilient",
    "Idealist",
    "Optimistic",
    "Hard Worker",
    "Improver",
    "Visionary",
    "Analyst",
    "Juggler",
    "Walt Disney",
    "Retail Pharmacy Store",
    "Dental Clinic",
    "Ambulance Services",
    "Sports Center",
    "Herbal Products Manufacturing",
    "Slimming Center",
    "Beauty Clinic",
    "Body Shaping Clinic",
    "Business Model",
    "Economic Value",
    "Market Opportunities",
    "Customer Needs",
    "Mindset"
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_filename(term: str) -> str:
    safe = term.lower().replace("-", "_").replace(" ", "_")
    safe = "".join(c for c in safe if c.isalnum() or c == "_")
    return safe

async def generate_term(term: str):
    fname = get_filename(term)
    out_path = os.path.join(OUTPUT_DIR, f"{fname}.mp3")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
        print(f"[SKIP] {term} ({fname}.mp3 exists)")
        return
    try:
        communicate = edge_tts.Communicate(term, VOICE, rate="-8%")
        await communicate.save(out_path)
        print(f"[OK] {term} -> {fname}.mp3 ({os.path.getsize(out_path)} bytes)")
    except Exception as e:
        print(f"[FAIL] {term}: {e}")

async def main():
    print(f"Generating audio for {len(TERMS)} terms using {VOICE}...")
    for term in TERMS:
        await generate_term(term)
    print("All audio files generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
