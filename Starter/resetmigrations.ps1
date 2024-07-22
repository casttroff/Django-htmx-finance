# resetmigrations.ps1

Get-ChildItem -Path . -Filter *.py -Recurse | Where-Object { $_.FullName -match '\\migrations\\' -and $_.Name -ne '__init__.py' -and $_.FullName -notmatch '\\venv\\' } | Remove-Item
Get-ChildItem -Path . -Filter *.pyc -Recurse | Where-Object { $_.FullName -match '\\migrations\\' } | Remove-Item
