import asyncio
import edge_tts
import os

OUTPUT_DIR = r"c:\Users\Administrator\Desktop\stady\dental-biomaterials\lecture-1\audio"
VOICE = "en-US-JennyNeural"

TERMS = [
    "Dentistry",
    "Esthetics",
    "Mastication",
    "Masticatory efficiency",
    "Oral Biology",
    "Oral Pathology",
    "Oral Radiology",
    "Dental Anatomy",
    "Prosthetic Dentistry",
    "Conservative Dentistry",
    "Operative Dentistry",
    "Endodontics",
    "Orthodontics",
    "Pedodontics",
    "Oral and Maxillofacial Surgery",
    "Oral Medicine",
    "Periodontology",
    "Dental Plaque",
    "Gum Recession",
    "Biomaterials",
    "Dental Biomaterials",
    "Prosthesis",
    "Fixed Prosthodontics",
    "Crown",
    "Bridge",
    "Dental Implants",
    "All Ceramic",
    "All Metallic",
    "Ceramo Metallic",
    "Removable Prosthodontics",
    "Complete Denture",
    "Partial Denture",
    "Denture Base",
    "Artificial Teeth",
    "Acrylic Resin",
    "Cobalt Chromium Alloy",
    "Gold Alloy",
    "Porcelain",
    "Direct Restoration",
    "Indirect Restoration",
    "Dental Amalgam",
    "Composite Resin",
    "Glass Ionomer",
    "Inlay",
    "Onlay",
    "Dental Caries",
    "Dentulous",
    "Edentulous",
    "Anterior Teeth",
    "Posterior Teeth",
    "Class I Caries",
    "Class II Caries",
    "Class III Caries",
    "Class IV Caries",
    "Class V Caries",
    "Manipulation",
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def generate_audio(term: str):
    safe_name = term.lower().replace(" ", "_")
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
