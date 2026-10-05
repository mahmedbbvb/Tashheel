import asyncio
import edge_tts
import os

OUTPUT_DIR = r"c:\Users\Administrator\Desktop\stady\histology\lecture-1\audio"
VOICE = "en-US-JennyNeural"

TERMS = [
    "Histology",
    "Cytology",
    "Microscopy",
    "Light Microscope",
    "Electron Microscope",
    "Transmission Electron Microscope",
    "Scanning Electron Microscope",
    "Intracellular Organelles",
    "Cytoplasm",
    "Cytoplasmic Matrix",
    "Cytoplasmic Organelles",
    "Cytoplasmic Inclusions",
    "Membranous Organelles",
    "Non-membranous Organelles",
    "Cell Membrane",
    "Trilamellar Membrane",
    "Glycocalyx",
    "Cell Coat",
    "Glycoprotein",
    "Glycolipid",
    "Passive Transport",
    "Active Transport",
    "Facilitated Transport",
    "Mitochondria",
    "Cristae",
    "Mitochondrial Matrix",
    "Adenosine Triphosphate",
    "Endoplasmic Reticulum",
    "Rough Endoplasmic Reticulum",
    "Smooth Endoplasmic Reticulum",
    "Ribosomes",
    "Detoxification",
    "Golgi Apparatus",
    "Camillo Golgi",
    "Negative Golgi Image",
    "Cis Face",
    "Trans Face",
    "Secretory Vesicles",
    "Exocytosis",
    "Lysosomes",
    "Cytoskeleton",
    "Microtubules",
    "Centrioles",
    "Cilia",
    "Filaments",
    "Hematoxylin and Eosin"
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def generate_audio(term: str):
    safe_name = term.lower().replace(" ", "_").replace("-", "_")
    safe_name = "".join(c for c in safe_name if c.isalnum() or c == "_")
    out_path = os.path.join(OUTPUT_DIR, f"{safe_name}.mp3")

    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        return

    try:
        communicate = edge_tts.Communicate(term, VOICE, rate="-10%")
        await communicate.save(out_path)
        print(f"[OK] {term}")
    except Exception as e:
        print(f"[FAIL] {term}: {e}")

async def main():
    tasks = [generate_audio(t) for t in TERMS]
    await asyncio.gather(*tasks)
    print(f"Generated {len(os.listdir(OUTPUT_DIR))} audio files in {OUTPUT_DIR}")

if __name__ == "__main__":
    asyncio.run(main())
