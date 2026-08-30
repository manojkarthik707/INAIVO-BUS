Write-Host "Launching CARLA in Low-VRAM mode..."
$CarlaExe = "F:\VEHDEMO\carla_0.9.16\WindowsNoEditor\CarlaUE4.exe"
if (Test-Path $CarlaExe) {
    Start-Process -FilePath $CarlaExe -ArgumentList "-windowed -ResX=800 -ResY=600 -quality-level=Low -d3d11"
    Write-Host "CARLA started in a visible 800x600 window with DirectX 11."
} else {
    Write-Host "Could not find CARLA at $CarlaExe" -ForegroundColor Red
}
