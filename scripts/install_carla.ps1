$CarlaUrl = "https://carla-releases.s3-us-west-2.amazonaws.com/Windows/CARLA_0.9.15.zip"
$TargetZip = "F:\VEHDEMO\CARLA_0.9.15.zip"
$ExtractPath = "F:\VEHDEMO\carla_0.9.15"

Write-Host "Starting download of CARLA 0.9.15 (this is ~5.6GB and will take a while)..."
Invoke-WebRequest -Uri $CarlaUrl -OutFile $TargetZip

Write-Host "Download complete. Starting extraction to $ExtractPath ..."
Expand-Archive -LiteralPath $TargetZip -DestinationPath $ExtractPath -Force

Write-Host "Extraction complete! Cleaning up zip file..."
Remove-Item -Path $TargetZip -Force

Write-Host "CARLA Installation Finished. You can launch it at $ExtractPath\CarlaUE4.exe"
