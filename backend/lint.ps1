$shellPath=[System.IO.Path]::Combine($pwd.Path, "lint.sh")
Copy-Item $shellPath -Destination lint_tmp.ps1
(Get-Content lint_tmp.ps1) -replace "`n", "`r`n" | Set-Content lint_tmp.ps1
& .\lint_tmp.ps1
echo $LASTEXITCODE
Remove-Item lint_tmp.ps1