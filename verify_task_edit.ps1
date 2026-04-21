$lines = Get-Content 'C:\Users\haizhi\Projects\my-test\index.html' -Encoding UTF8
Write-Host "Total lines: $($lines.Count)"
$tests = @(
  @{n='编辑表单-预估工时'; p='task-est-hours-edit'},
  @{n='编辑表单-关联项目'; p='task-project-edit'},
  @{n='编辑表单-开始日期'; p='task-start-date-edit'},
  @{n='编辑表单-标签'; p='task-tags-edit'},
  @{n='编辑表单-检查清单'; p='task-checkitems-edit'},
  @{n='新建表单-任务类型'; p='task-type-add'},
  @{n='新建表单-关联项目'; p='task-project-add'},
  @{n='openModal新字段'; p='estimatedHours'},
  @{n='saveTask审计日志'; p='logAudit.*task'},
  @{n='getProjectName函数'; p='getProjectName'},
  @{n='优先级可延后'; p='可延后'},
  @{n='viewTask详情视图'; p='modalTitle==.编辑任务'},
  @{n='详情视图关联项目'; p='getProjectName(formData.projectId)'},
  @{n='详情视图检查清单'; p='formData.checkItems'},
  @{n='详情视图标签显示'; p='formData.tags.*split'}
)
foreach ($t in $tests) {
  $m = $lines | Where-Object { $_ -match $t.p } | Select-Object -First 1
  if ($m) {
    $idx = [array]::IndexOf($lines, $m) + 1
    Write-Host "OK  $($t.n) -> line $idx"
  } else {
    Write-Host "MISS $($t.n)"
  }
}
