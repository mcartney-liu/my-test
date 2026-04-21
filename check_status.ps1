$l = Get-Content 'C:\Users\haizhi\Projects\my-test\index.html' -Encoding UTF8
"$($l.Count) lines"
$results = @()

$patterns = @(
  "showShortcutHelp=ref",
  "shortcut-modal",
  "handleKeyUp,isInputFocused",
  "isInputFocused.*activeElement",
  "shortcut-footer",
  "addEventListener.*keyup.*handleKeyUp"
)

foreach ($p in $patterns) {
  $match = $l | Where-Object { $_ -match $p } | Select-Object -First 1
  if ($match) {
    $idx = [array]::IndexOf($l, $match) + 1
    $results += "  $p -> line $idx"
  } else {
    $results += "  $p -> NOT FOUND"
  }
}

$results | ForEach-Object { Write-Host $_ }
