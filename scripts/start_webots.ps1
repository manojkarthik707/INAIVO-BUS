# This script disables HTTP/2 in Qt to bypass the network proxy bug (error code: 399)
# so Webots can actually download the 3D assets (Bus, Pedestrian, Roads).

Write-Host "Disabling Qt HTTP/2 to fix 3D asset downloads..."
$env:QT_NETWORK_DISABLE_HTTP2 = "1"

# Kill anything still holding port 2345 or shared memory handles
Get-Process | Where-Object { $_.Name -like "webots*" } | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "Starting Webots on dedicated port 2345..."
$WebotsExe = "C:\Users\Moghul Kannan N\AppData\Local\Programs\Webots\msys64\mingw64\bin\webotsw.exe"
$WorldFile = "f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

Start-Process -FilePath $WebotsExe -ArgumentList "--port=2345 `"$WorldFile`""


