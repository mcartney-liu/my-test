with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all occurrences of key markers
edit_form = '<!-- Task Edit Form -->'
add_form = '<!-- Task Add Form -->'
template_panel = '<!-- 模板面板 -->'

edit_pos = content.find(edit_form)
print(f'Task Edit Form at: {edit_pos}')

# Find all template_panel occurrences
positions = []
start = 0
while True:
    pos = content.find(template_panel, start)
    if pos < 0:
        break
    positions.append(pos)
    start = pos + 1
    
print(f'All <!-- 模板面板 --> at: {positions}')

# The correct one should be AFTER the Task Add Form
add_pos = content.find(add_form)
print(f'Task Add Form at: {add_pos}')

# Find the first template_panel AFTER Task Add Form
correct_end = None
for p in positions:
    if p > add_pos:
        correct_end = p
        break
        
print(f'Correct end marker at: {correct_end}')

if correct_end and correct_end > edit_pos:
    new_section = '''<!-- Task Edit Form -->
      <form v-if="modalType==='task' && modalTitle==='编辑任务'" @submit.prevent="saveTask">
        <div class="form-group"><label for="task-name-edit">任务名称*</label><input type="text" v-model="formData.name" class="form-input" required id="task-name-edit" name="taskName"></div>
        <div class="form-row">
          <div class="form-group"><label for="task-type-edit">任务类型</label><select v-model="formData.type" class="form-input" id="task-type-edit" name="taskType"><option value="">请选择</option><option>开发</option><option>需求</option><option>交付</option><option>运维</option><option>会议</option><option>其他</option></select></div>
          <div class="form-group"><label for="task-status-edit">状态</label><select v-model="formData.status" class="form-input" id="task-status-edit" name="taskStatus"><option>待处理</option><option>进行中</option><option>已完成</option></select></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="task-priority-edit">优先级</label><select v-model="formData.priority" class="form-input" id="task-priority-edit" name="taskPriority"><option>紧急</option><option>高</option><option>中</option><option>低</option><option>可延后</option></select></div>
          <div class="form-group"><label for="task-project-edit">关联项目</label><select v-model="formData.projectId" class="form-input" id="task-project-edit" name="taskProject"><option value="">无关联</option><option v-for="p in projects" :key="p.id" :value="p.id">{{p.name}}</option></select></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="task-assignee-edit">负责人</label><input type="text" v-model="formData.assignee" class="form-input" id="task-assignee-edit" name="taskAssignee" list="assignee-list-edit"><datalist id="assignee-list-edit"><option v-for="m in teamMembers" :key="m.id" :value="m.name"/></datalist></div>
          <div class="form-group"><label for="task-due-date-edit">截止日期</label><input type="date" v-model="formData.dueDate" class="form-input" id="task-due-date-edit" name="taskDueDate"></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="task-start-date-edit">开始日期</label><input type="date" v-model="formData.startDate" class="form-input" id="task-start-date-edit" name="taskStartDate"></div>
          <div class="form-group"><label for="task-progress-edit">进度 (%)</label><input type="number" v-model="formData.progress" class="form-input" id="task-progress-edit" name="taskProgress" min="0" max="100"></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="task-est-hours-edit">预估工时（h）</label><input type="number" v-model="formData.estimatedHours" class="form-input" id="task-est-hours-edit" name="taskEstHours" min="0" placeholder="0"></div>
          <div class="form-group"><label for="task-act-hours-edit">实际工时（h）</label><input type="number" v-model="formData.actualHours" class="form-input" id="task-act-hours-edit" name="taskActHours" min="0" placeholder="0"></div>
        </div>
        <div class="form-group"><label for="task-tags-edit">标签（逗号分隔）</label><input type="text" v-model="formData.tags" class="form-input" id="task-tags-edit" name="taskTags" placeholder="例如：前端,登录模块,bug"></div>
        <div class="form-group"><label for="task-description-edit">任务描述</label><textarea v-model="formData.description" class="form-input" id="task-description-edit" name="taskDescription" rows="3" placeholder="详细描述任务内容、背景、目标..."></textarea></div>
        <div class="form-group"><label for="task-checkitems-edit">检查清单（每行一项）</label><textarea v-model="formData.checkItems" class="form-input" id="task-checkitems-edit" name="taskCheckItems" rows="3" placeholder="检查项1&#10;检查项2&#10;检查项3"></textarea></div>
        <div class="modal-footer"><button type="button" class="btn btn-secondary" @click="closeModal">取消</button><button type="submit" class="btn btn-primary">保存修改</button></div>
      </form>

      <!-- Task Add Form -->
      <form v-if="modalType==='task' && modalTitle==='新建任务'" @submit.prevent="saveTask">
        <div class="form-group"><label for="task-name-add">任务名称*</label><input type="text" v-model="formData.name" class="form-input" required id="task-name-add" name="taskName"></div>
        <div class="form-row">
          <div class="form-group"><label for="task-type-add">任务类型</label><select v-model="formData.type" class="form-input" id="task-type-add" name="taskType"><option value="">请选择</option><option>开发</option><option>需求</option><option>交付</option><option>运维</option><option>会议</option><option>其他</option></select></div>
          <div class="form-group"><label for="task-priority-add">优先级</label><select v-model="formData.priority" class="form-input" id="task-priority-add" name="taskPriority"><option>紧急</option><option>高</option><option>中</option><option>低</option><option>可延后</option></select></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="task-assignee-add">负责人</label><input type="text" v-model="formData.assignee" class="form-input" id="task-assignee-add" name="taskAssignee" list="assignee-list-add"><datalist id="assignee-list-add"><option v-for="m in teamMembers" :key="m.id" :value="m.name"/></datalist></div>
          <div class="form-group"><label for="task-due-date-add">截止日期</label><input type="date" v-model="formData.dueDate" class="form-input" id="task-due-date-add" name="taskDueDate"></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="task-project-add">关联项目</label><select v-model="formData.projectId" class="form-input" id="task-project-add" name="taskProject"><option value="">无关联</option><option v-for="p in projects" :key="p.id" :value="p.id">{{p.name}}</option></select></div>
          <div class="form-group"><label for="task-start-date-add">开始日期</label><input type="date" v-model="formData.startDate" class="form-input" id="task-start-date-add" name="taskStartDate"></div>
        </div>
        <div class="form-group"><label for="task-tags-add">标签（逗号分隔）</label><input type="text" v-model="formData.tags" class="form-input" id="task-tags-add" name="taskTags" placeholder="例如：前端,登录模块"></div>
        <div class="form-group"><label for="task-description-add">任务描述</label><textarea v-model="formData.description" class="form-input" id="task-description-add" name="taskDescription" rows="3" placeholder="详细描述任务内容、背景、目标..."></textarea></div>
        <div class="form-group"><label for="task-checkitems-add">检查清单（每行一项）</label><textarea v-model="formData.checkItems" class="form-input" id="task-checkitems-add" name="taskCheckItems" rows="3" placeholder="检查项1&#10;检查项2&#10;检查项3"></textarea></div>
        <div class="modal-footer"><button type="button" class="btn btn-secondary" @click="closeModal">取消</button><button type="submit" class="btn btn-primary">提交任务</button></div>
      </form>

      <!-- 模板面板 -->'''

    new_content = content[:edit_pos] + new_section + content[correct_end:]
    
    with open('C:/Users/haizhi/Projects/my-test/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f'Done! Replaced {correct_end - edit_pos} chars with {len(new_section)} chars')
    print(f'New file length: {len(new_content)}')
else:
    print('ERROR: Could not find correct boundaries')
