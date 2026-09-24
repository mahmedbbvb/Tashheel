$apiKey = "YOUR_ELEVENLABS_API_KEY"
$voiceId = "21m00Tcm4TlvDq8ikWAM"
$outputDir = ".\audio"

$terms = @(
    "Somatic Nervous System",
    "Voluntary",
    "Skeletal Muscle",
    "Central Nervous System",
    "Motor Neuron",
    "Somatic Motor System",
    "Autonomic Nervous System",
    "Preganglionic Neuron",
    "Ganglion",
    "Postganglionic Neuron",
    "Afferent",
    "Efferent",
    "Action Potential",
    "Nerve",
    "Sensory fibers",
    "Motor fibers",
    "Mixed nerve",
    "Spinal Cord",
    "Gray Matter",
    "White Matter",
    "Horns",
    "Anterior Horn",
    "Posterior Horn",
    "Lateral Horn",
    "Involuntary"
)

$headers = @{
    "Content-Type" = "application/json"
    "xi-api-key"   = $apiKey
    "Accept"       = "audio/mpeg"
}

foreach ($term in $terms) {
    $safeName = $term.ToLower() -replace '\s+', '_' -replace '[^a-z0-9_]', ''
    $outFile = Join-Path $outputDir "$safeName.mp3"

    if (Test-Path $outFile) {
        Write-Host "[SKIP] $term  (already exists)" -ForegroundColor Yellow
        continue
    }

    Write-Host "[GEN]  $term ..." -NoNewline

    $body = @{
        text           = $term
        model_id       = "eleven_multilingual_v2"
        voice_settings = @{
            stability        = 0.5
            similarity_boost = 0.75
            style            = 0.0
            use_speaker_boost = $true
        }
    } | ConvertTo-Json -Depth 3

    try {
        Invoke-RestMethod `
            -Uri "https://api.elevenlabs.io/v1/text-to-speech/$voiceId" `
            -Method Post `
            -Headers $headers `
            -Body $body `
            -OutFile $outFile `
            -ErrorAction Stop

        $size = (Get-Item $outFile).Length
        Write-Host " OK ($size bytes)" -ForegroundColor Green
    }
    catch {
        Write-Host " FAILED: $_" -ForegroundColor Red
    }

    # small delay to respect rate limits
    Start-Sleep -Milliseconds 500
}

Write-Host "`nDone! Generated audio files in $outputDir" -ForegroundColor Cyan
