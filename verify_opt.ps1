$l = Get-Content 'C:\Users\haizhi\Projects\my-test\index.html' -Encoding UTF8
Write-Host "Total lines: $($l.Count)"
Write-Host ""
Write-Host "=== PM-OS Optimization Status ==="
$tests = @(
  @{name="Keyboard shortcuts ref";      pat="showShortcutHelp=ref"},
  @{name="Keyboard shortcuts array";     pat="shortcuts\s*=\s*\["},
  @{name="handleKeyUp function";         pat="gKeyPending.*ref"},
  @{name="isInputFocused function";      pat="const isInputFocused="},
  @{name="Keyboard CSS";                pat="shortcut-modal.*position"},
  @{name="Keyboard HTML";                pat="shortcut-overlay.*v-if"},
  @{name="Keyboard footer";              pat="shortcut-footer"},
  @{name="Shortcut in return";          pat="showShortcutHelp,shortcuts"},
  @{name="keyup event listener";         pat="addEventListener.*keyup.*handleKeyUp"},
  @{name="notifyPrefs reactive";          pat="notifyPrefs=reactive"},
  @{name="saveNotifyPrefs";              pat="saveNotifyPrefs.*=>"},
  @{name="loadNotifyPrefs in loadAll";   pat="loadNotifyPrefs\(\)"},
  @{name="notify CSS grid";              pat="notify-pref-grid"},
  @{name="toggle switch CSS";            pat="toggle-switch.*on.*toggle-knob"},
  @{name="reminder time selector";        pat="reminder-time-selector"},
  @{name="auto theme";                   pat="prefers-color-scheme"},
  @{name="setTheme auto";                pat="setTheme.*auto.*initTheme"},
  @{name="auto theme option HTML";       pat="currentTheme === .auto."}
)
foreach ($t in $tests) {
  $m = $l | Where-Object { $_ -match $t.pat } | Select-Object -First 1
  if ($m) {
    $idx = [array]::IndexOf($l, $m) + 1
    Write-Host "OK  $($t.name) -> line $idx"
  } else {
    Write-Host "MISS $($t.name)"
  }
}
