$terms = @{
    "cell" = "The Cell"
    "cytoplasm" = "Cytoplasm"
    "nucleus" = "Nucleus"
    "cytoplasmic_matrix" = "Cytoplasmic Matrix"
    "cytoplasmic_organelles" = "Cytoplasmic Organelles"
    "cytoplasmic_inclusions" = "Cytoplasmic Inclusions"
    "membranous_organelles" = "Membranous Organelles"
    "non_membranous_organelles" = "Non-membranous Organelles"
    "cell_membrane" = "Cell Membrane"
    "mitochondria" = "Mitochondria"
    "endoplasmic_reticulum" = "Endoplasmic Reticulum"
    "rough_endoplasmic_reticulum" = "Rough Endoplasmic Reticulum"
    "smooth_endoplasmic_reticulum" = "Smooth Endoplasmic Reticulum"
    "golgi_apparatus" = "Golgi Apparatus"
    "lysosomes" = "Lysosomes"
    "ribosomes" = "Ribosomes"
    "cytoskeleton" = "Cytoskeleton"
    "microtubules" = "Microtubules"
    "centrioles" = "Centrioles"
    "cilia" = "Cilia"
    "filaments" = "Filaments"
    "digestive_system_of_the_cell" = "Digestive System of the Cell"
    "hydrolytic_enzymes" = "Hydrolytic Enzymes"
    "phospholipases" = "Phospholipases"
    "proteases" = "Proteases"
    "nucleases" = "Nucleases"
    "phagocytic_cells" = "Phagocytic Cells"
    "white_blood_cells" = "White Blood Cells"
    "electron_dense" = "Electron-dense"
    "primary_lysosomes" = "Primary Lysosomes"
    "secondary_lysosomes" = "Secondary Lysosomes"
    "homogenous_vesicles" = "Homogenous Vesicles"
    "heterogeneous_vesicles" = "Heterogeneous Vesicles"
    "heterolysosome" = "Heterolysosome"
    "heterolysosomes" = "Heterolysosomes"
    "multivesicular_body" = "Multivesicular Body"
    "multivesicular_bodies" = "Multivesicular Bodies"
    "autolysosome" = "Autolysosome"
    "autolysosomes" = "Autolysosomes"
    "autophagy" = "Autophagy"
    "residual_body" = "Residual Body"
    "residual_bodies" = "Residual Bodies"
    "phagocytosis" = "Phagocytosis"
    "pinocytosis" = "Pinocytosis"
    "exocytosis" = "Exocytosis"
    "autolysis" = "Autolysis"
    "programmed_cell_death" = "Programmed Cell Death"
    "inclusions" = "Inclusions"
    "stored_food" = "Stored Food"
    "carbohydrates" = "Carbohydrates"
    "glycogen" = "Glycogen"
    "bests_carmine" = "Best's Carmine"
    "pas" = "P A S"
    "alpha_granules" = "Alpha Granules"
    "beta_granules" = "Beta Granules"
    "fats" = "Fats"
    "lipids" = "Lipids"
    "sudan_iii" = "Sudan Three"
    "sudan_black" = "Sudan Black"
    "empty_vacuoles" = "Empty Vacuoles"
    "pigments" = "Pigments"
    "endogenous_pigments" = "Endogenous Pigments"
    "exogenous_pigments" = "Exogenous Pigments"
    "hemoglobin" = "Hemoglobin"
    "melanin" = "Melanin"
    "lipofuscin" = "Lipofuscin"
    "lipofuscin_granules" = "Lipofuscin Granules"
    "dust_cells" = "Dust Cells"
    "black_lungs" = "Black Lungs"
    "carotene" = "Carotene"
    "tattoo_marks" = "Tattoo Marks"
    "india_ink" = "India Ink"
    "command_center" = "Command Center"
    "basophilic" = "Basophilic"
    "basophilic_structure" = "Basophilic Structure"
    "nuclear_envelope" = "Nuclear Envelope"
    "perinuclear_space" = "Perinuclear Space"
    "nuclear_pores" = "Nuclear Pores"
    "diaphragms" = "Diaphragms"
    "nucleoplasm" = "Nucleoplasm"
    "nuclear_sap" = "Nuclear Sap"
    "chromatin" = "Chromatin"
    "nucleoprotein" = "Nucleoprotein"
    "chromosomes" = "Chromosomes"
    "euchromatin" = "Euchromatin"
    "heterochromatin" = "Heterochromatin"
    "nucleolus" = "Nucleolus"
    "rrna" = "Ribosomal R N A"
    "mrna" = "Messenger R N A"
    "trna" = "Transfer R N A"
    "light_microscope" = "Light Microscope"
    "electron_microscope" = "Electron Microscope"
}

$audioDir = "c:\Users\Administrator\Desktop\stady\histology\lecture-2\audio"
if (-not (Test-Path $audioDir)) {
    New-Item -ItemType Directory -Path $audioDir | Out-Null
}

$voice = New-Object -ComObject SAPI.SpVoice
# Select Zira voice if available
foreach ($v in $voice.GetVoices()) {
    if ($v.GetDescription() -like "*Zira*") {
        $voice.Voice = $v
        break
    }
}
$voice.Rate = -1

Write-Host "Using Voice: " $voice.Voice.GetDescription()
$total = $terms.Count
$idx = 0

foreach ($key in $terms.Keys) {
    $idx++
    $text = $terms[$key]
    $wavFile = Join-Path $audioDir "$key.wav"
    $mp3File = Join-Path $audioDir "$key.mp3"

    $fileStream = New-Object -ComObject SAPI.SpFileStream
    $fileStream.Open($wavFile, 3, $false)
    $voice.AudioOutputStream = $fileStream
    $voice.Speak($text) | Out-Null
    $fileStream.Close()

    # Convert to MP3 using ffmpeg
    & ffmpeg -y -loglevel error -i $wavFile -b:a 128k $mp3File
    if (Test-Path $mp3File) {
        Remove-Item $wavFile -Force
        Write-Host "[$idx/$total] OK: $key -> $mp3File"
    } else {
        Write-Host "[$idx/$total] WARN: Kept WAV for $key"
    }
}

Write-Host "Done! Successfully generated audio files in $audioDir"
