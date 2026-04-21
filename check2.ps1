$l = Get-Content 'C:\Users\haizhi\Projects\my-test\index.html' -Encoding UTF8
$m = $l | Where-Object { $_ -match 'const isInputFocused' }
if ($m) {
  $idx = [array]::IndexOf($l, $m) + 1
  Write-Host "isInputFocused 定义: line $idx"
  Write-Host "  $_"
} else {
  Write-Host "isInputFocused NOT FOUND"
}
