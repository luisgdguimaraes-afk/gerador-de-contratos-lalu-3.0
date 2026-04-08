# Script para ver logs do backend em tempo real
$logFile = "$env:USERPROFILE\.cursor\projects\c-Users-luisg-Downloads-Contratos-LALU-Contratos-LALU\terminals\628256.txt"

Write-Host "Monitorando logs do backend..." -ForegroundColor Green
Write-Host "Pressione Ctrl+C para parar" -ForegroundColor Yellow
Write-Host ""

Get-Content $logFile -Wait -Tail 20
