# PowerShell Remove-Item: Recycle Bin Workaround

**Last Updated**: 2026-02-08

## Problem

`Remove-Item -Recurse -Force` permanently deletes files. It does **not** use the Windows Recycle Bin. Similar to the `rm -rf` trope—irreversible, no undo.

This is a poor default for interactive use when you might want to recover deleted items.

## Workaround: Recycle Bin Alias

Add to your PowerShell profile (`$PROFILE`):

```powershell
Add-Type -AssemblyName Microsoft.VisualBasic

function Remove-ToRecycleBin {
    param([Parameter(Mandatory, ValueFromPipeline)]$Path)
    process {
        foreach ($p in $Path) {
            $item = Get-Item $p -ErrorAction SilentlyContinue
            if (-not $item) { continue }
            if ($item.PSIsContainer) {
                [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory($item.FullName, 'OnlyErrorDialogs', 'SendToRecycleBin')
            } else {
                [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile($item.FullName, 'OnlyErrorDialogs', 'SendToRecycleBin')
            }
        }
    }
}

Set-Alias trash Remove-ToRecycleBin
```

## Usage

```powershell
trash "D:\Dev\repos\some\folder"
trash "D:\path\to\file.txt"
Get-ChildItem *.tmp | trash
```

## When to Use Which

| Use Case | Command |
|----------|---------|
| Recoverable delete (interactive) | `trash` |
| Permanent delete (scripts, intentional) | `Remove-Item -Recurse -Force` |
| Clone you're about to replace | Either; `Remove-Item` is fine |

## Create Profile If Missing

```powershell
if (-not (Test-Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force
}
notepad $PROFILE
```

## References

- [Microsoft.VisualBasic.FileIO.FileSystem](https://learn.microsoft.com/en-us/dotnet/api/microsoft.visualbasic.fileio.filesystem) — `DeleteFile`, `DeleteDirectory` with `SendToRecycleBin`
