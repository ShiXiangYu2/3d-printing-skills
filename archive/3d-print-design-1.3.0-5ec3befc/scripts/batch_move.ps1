param([Parameter(Mandatory=$true)][string]$Root,[Parameter(Mandatory=$true)][string]$Plan)
$ErrorActionPreference = 'Stop'
$resolvedRoot = [IO.Path]::GetFullPath($Root).TrimEnd('\') + '\'
$items = @(Get-Content -LiteralPath $Plan -Raw -Encoding UTF8 | ConvertFrom-Json)
foreach ($item in $items) {
    $sourcePath = [IO.Path]::GetFullPath($item.source)
    $destinationPath = [IO.Path]::GetFullPath($item.destination)
    if (-not $sourcePath.StartsWith($resolvedRoot,[StringComparison]::OrdinalIgnoreCase) -or -not $destinationPath.StartsWith($resolvedRoot,[StringComparison]::OrdinalIgnoreCase)) { throw 'Move escapes workspace' }
    $sourceInfo = Get-Item -LiteralPath $sourcePath
    if ($sourceInfo.PSIsContainer -or ($sourceInfo.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Only ordinary declared files can be preserved' }
    if (Test-Path -LiteralPath $destinationPath) { throw 'History target already exists' }
}
foreach ($item in $items) { Move-Item -LiteralPath $item.source -Destination $item.destination }
