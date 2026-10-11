import asyncio
import edge_tts
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "audio")
VOICE = "en-US-JennyNeural"

TERMS = [
    # General Cell & Cytoplasm
    "The Cell",
    "Cytoplasm",
    "Nucleus",
    "Cytoplasmic Matrix",
    "Cytoplasmic Organelles",
    "Cytoplasmic Inclusions",
    "Membranous Organelles",
    "Non-membranous Organelles",
    "Cell Membrane",
    "Mitochondria",
    "Endoplasmic Reticulum",
    "Rough Endoplasmic Reticulum",
    "Smooth Endoplasmic Reticulum",
    "Golgi Apparatus",
    "Ribosomes",
    "Cytoskeleton",
    "Microtubules",
    "Centrioles",
    "Cilia",
    "Filaments",
    
    # Lysosomes
    "Lysosomes",
    "Digestive System of the Cell",
    "Hydrolytic Enzymes",
    "Phospholipases",
    "Proteases",
    "Nucleases",
    "Phagocytic Cells",
    "White Blood Cells",
    "Electron-dense",
    "Primary Lysosomes",
    "Secondary Lysosomes",
    "Homogenous Vesicles",
    "Heterogeneous Vesicles",
    "Heterolysosomes",
    "Multivesicular Bodies",
    "Autolysosomes",
    "Autophagy",
    "Residual Bodies",
    "Phagocytosis",
    "Pinocytosis",
    "Exocytosis",
    "Autolysis",
    "Programmed Cell Death",
    
    # Inclusions & Stored Food
    "Inclusions",
    "Stored Food",
    "Carbohydrates",
    "Glycogen",
    "Bests Carmine",
    "PAS",
    "Alpha Granules",
    "Beta Granules",
    "Fats",
    "Lipids",
    "Sudan III",
    "Sudan Black",
    "Empty Vacuoles",
    
    # Pigments
    "Pigments",
    "Endogenous Pigments",
    "Exogenous Pigments",
    "Hemoglobin",
    "Melanin",
    "Lipofuscin Granules",
    "Dust Cells",
    "Black Lungs",
    "Carotene",
    "Tattoo Marks",
    
    # The Nucleus
    "Command Center of the Cell",
    "Basophilic Structure",
    "Nuclear Envelope",
    "Perinuclear Space",
    "Nuclear Pores",
    "Diaphragms",
    "Nucleoplasm",
    "Nuclear Sap",
    "Chromatin",
    "Nucleoprotein",
    "Chromosomes",
    "Euchromatin",
    "Heterochromatin",
    "Nucleolus",
    "rRNA",
    "mRNA",
    "tRNA",
    "Light Microscope",
    "Electron Microscope",
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_safe_filename(term: str) -> str:
    safe = term.lower().replace("'", "").replace("&", "and")
    safe = safe.replace(" ", "_").replace("-", "_").replace("[", "").replace("]", "")
    safe = "".join(c for c in safe if c.isalnum() or c == "_")
    while "__" in safe:
        safe = safe.replace("__", "_")
    return safe.strip("_")

async def generate_audio(term: str):
    filename = get_safe_filename(term) + ".mp3"
    out_path = os.path.join(OUTPUT_DIR, filename)

    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        return filename

    try:
        communicate = edge_tts.Communicate(term, VOICE, rate="-5%")
        await communicate.save(out_path)
        print(f"[OK] {term} -> {filename}")
        return filename
    except Exception as e:
        print(f"[FAIL] {term}: {e}")
        return None

async def main():
    print(f"Generating audio files in: {OUTPUT_DIR}")
    for term in TERMS:
        await generate_audio(term)
    print(f"Finished! Total audio files: {len(os.listdir(OUTPUT_DIR))}")

if __name__ == "__main__":
    asyncio.run(main())
