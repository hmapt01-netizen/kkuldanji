param(
    [int]$Port = 8080
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$webRoot = $PSScriptRoot
Set-Location $webRoot

# Wi-Fi IP 자동 감지
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { 
    $_.IPAddress -notmatch '^169\.' -and $_.IPAddress -ne '127.0.0.1' -and $_.InterfaceAlias -notmatch 'Loopback|vEthernet|WSL' 
} | Select-Object -ExpandProperty IPAddress -First 1)

if (-not $localIP) { $localIP = "127.0.0.1" }

$listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Any, $Port)
$listener.Start()

Clear-Host
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "   [꿀단지] 스마트폰 & PC 실시간 미리보기 서버" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host " [PC 브라우저 접속]" -ForegroundColor Green
Write-Host "   -> http://localhost:$Port" -ForegroundColor White
Write-Host ""
Write-Host " [스마트폰(모바일) 접속]  *PC와 같은 Wi-Fi 연결 필수*" -ForegroundColor Green
Write-Host "   -> http://$($localIP):$Port" -ForegroundColor Yellow -BackgroundColor DarkBlue
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "   서버가 정상 실행 중입니다. (종료하려면 이 창을 닫으세요)" -ForegroundColor Gray
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Start-Process "http://localhost:$Port"

$mimeTypes = @{
    ".html" = "text/html; charset=utf-8"
    ".htm"  = "text/html; charset=utf-8"
    ".css"  = "text/css; charset=utf-8"
    ".js"   = "application/javascript; charset=utf-8"
    ".json" = "application/json; charset=utf-8"
    ".png"  = "image/png"
    ".jpg"  = "image/jpeg"
    ".jpeg" = "image/jpeg"
    ".gif"  = "image/gif"
    ".svg"  = "image/svg+xml"
    ".ico"  = "image/x-icon"
    ".webp" = "image/webp"
    ".woff" = "font/woff"
    ".woff2"= "font/woff2"
    ".ttf"  = "font/ttf"
}

try {
    while ($true) {
        $client = $listener.AcceptTcpClient()
        $stream = $client.GetStream()
        $reader = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::UTF8)

        $requestLine = $reader.ReadLine()
        if ([string]::IsNullOrEmpty($requestLine)) {
            $client.Close()
            continue
        }

        $tokens = $requestLine.Split(' ')
        if ($tokens.Length -lt 2) {
            $client.Close()
            continue
        }

        $rawPath = $tokens[1].Split('?')[0]
        $relPath = [System.Uri]::UnescapeDataString($rawPath.TrimStart('/'))
        if ([string]::IsNullOrWhiteSpace($relPath)) {
            $relPath = "index.html"
        }

        $filePath = Join-Path $webRoot $relPath
        if (Test-Path $filePath -PathType Container) {
            $filePath = Join-Path $filePath "index.html"
        }

        if (Test-Path $filePath -PathType Leaf) {
            $ext = [System.IO.Path]::GetExtension($filePath).ToLower()
            $mime = if ($mimeTypes.ContainsKey($ext)) { $mimeTypes[$ext] } else { "application/octet-stream" }
            $bytes = [System.IO.File]::ReadAllBytes($filePath)

            $header = "HTTP/1.1 200 OK`r`n" +
                      "Content-Type: $mime`r`n" +
                      "Content-Length: $($bytes.Length)`r`n" +
                      "Connection: close`r`n" +
                      "Cache-Control: no-cache, no-store, must-revalidate`r`n`r`n"
            $headerBytes = [System.Text.Encoding]::UTF8.GetBytes($header)

            $stream.Write($headerBytes, 0, $headerBytes.Length)
            $stream.Write($bytes, 0, $bytes.Length)
        } else {
            $errMsg = "<html><body><h1>404 Not Found</h1><p>$relPath</p></body></html>"
            $errBytes = [System.Text.Encoding]::UTF8.GetBytes($errMsg)
            $header = "HTTP/1.1 404 Not Found`r`n" +
                      "Content-Type: text/html; charset=utf-8`r`n" +
                      "Content-Length: $($errBytes.Length)`r`n" +
                      "Connection: close`r`n`r`n"
            $headerBytes = [System.Text.Encoding]::UTF8.GetBytes($header)
            $stream.Write($headerBytes, 0, $headerBytes.Length)
            $stream.Write($errBytes, 0, $errBytes.Length)
        }

        $stream.Flush()
        $client.Close()
    }
} finally {
    $listener.Stop()
}
