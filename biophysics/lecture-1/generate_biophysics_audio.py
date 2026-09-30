import asyncio
import edge_tts
import os

OUTPUT_DIR = "audio"
VOICE = "en-US-JennyNeural"

TERMS = [
    "Biophysics",
    "Biological Processes",
    "Eukaryotes",
    "Prokaryotes",
    "Cell Membrane",
    "Molecular Biophysics",
    "Cellular Biophysics",
    "Systems Biophysics",
    "Femtosecond",
    "Picosecond",
    "Laser Spectroscopy",
    "Biomechanics",
    "Fluid Biophysics",
    "Thermal Biophysics",
    "Macromolecules",
    "Polymers",
    "Monomers",
    "Dalton",
    "Dehydration Synthesis",
    "Hydrolysis",
    "Carbohydrates",
    "Monosaccharides",
    "Disaccharides",
    "Polysaccharides",
    "Phospholipids",
    "Hydrophilic",
    "Hydrophobic",
    "Lipid Bilayer",
    "Steroids",
    "Cholesterol",
    "Passive Transport",
    "Active Transport",
    "Simple Diffusion",
    "Facilitated Diffusion",
    "Osmosis",
    "Voltage-gated Channel",
    "Ligand-gated Channel",
    "Stress-gated Channel",
    "Sodium Potassium Pump",
    "Random Walk",
    "Displacement",
    "Diffusion Coefficient",
    "Fick's Law",
    "Permeability",
    "Flux",
    "Extracellular Fluid",
    "Cytoplasm",
    "Aquaporins",
    "Membrane Potential",
    "Kinetic Energy",
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def generate_audio(term: str):
    safe_name = term.lower().replace(" ", "_").replace("-", "_").replace("'", "")
    safe_name = "".join(c for c in safe_name if c.isalnum() or c == "_")
    out_path = os.path.join(OUTPUT_DIR, f"{safe_name}.mp3")

    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
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
