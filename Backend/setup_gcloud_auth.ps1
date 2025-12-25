# ============================================
# Google Cloud Authentication Setup Script
# ============================================
# This script helps you authenticate with Google Cloud
# using Application Default Credentials (ADC)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Google Cloud Authentication Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Check if gcloud is installed
Write-Host "[Step 1/4] Checking gcloud installation..." -ForegroundColor Yellow
try {
    $gcloudVersion = gcloud --version 2>&1 | Select-Object -First 1
    Write-Host "✅ gcloud is installed: $gcloudVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ gcloud CLI is not installed!" -ForegroundColor Red
    Write-Host "`nPlease install gcloud CLI from:" -ForegroundColor Yellow
    Write-Host "https://cloud.google.com/sdk/docs/install`n" -ForegroundColor Cyan
    exit 1
}

# Step 2: Set the project
Write-Host "`n[Step 2/4] Setting GCP project..." -ForegroundColor Yellow
$projectId = "aarogya-genai-hackathon"
gcloud config set project $projectId
Write-Host "✅ Project set to: $projectId" -ForegroundColor Green

# Step 3: Authenticate with Application Default Credentials
Write-Host "`n[Step 3/4] Authenticating with Application Default Credentials..." -ForegroundColor Yellow
Write-Host "This will open a browser window for authentication.`n" -ForegroundColor Cyan
gcloud auth application-default login

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Authentication successful!" -ForegroundColor Green
} else {
    Write-Host "❌ Authentication failed!" -ForegroundColor Red
    exit 1
}

# Step 4: Verify authentication
Write-Host "`n[Step 4/4] Verifying authentication..." -ForegroundColor Yellow
try {
    $token = gcloud auth application-default print-access-token 2>&1
    if ($token -match "^ya29\.") {
        Write-Host "✅ Authentication verified! Access token obtained." -ForegroundColor Green
    } else {
        Write-Host "⚠️ Warning: Could not verify access token" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ Warning: Could not verify authentication" -ForegroundColor Yellow
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Your backend server should automatically reload" -ForegroundColor White
Write-Host "2. Check the terminal for these success messages:" -ForegroundColor White
Write-Host "   ✅ Vertex AI initialized: aarogya-genai-hackathon" -ForegroundColor Gray
Write-Host "   ✅ BigQuery initialized: aarogya-genai-hackathon.aarogya_healthcare" -ForegroundColor Gray
Write-Host "`nIf you still see warnings, restart the backend server.`n" -ForegroundColor White
