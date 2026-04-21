import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
changes = 0

# ---- 1. 修复 viewCustomer - 确保activities数组初始化 ----
old_view = '''const viewCustomer=(c)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(c)));
      editingId.value=c.id;
      modalType.value='customer';
      modalTitle.value='客户详情';
      showModal.value=true;
    };'''
new_view = '''const viewCustomer=(c)=>{
      Object.assign(formData,JSON.parse(JSON.stringify({...c,activities:c.activities||[]})));
      editingId.value=c.id;
      modalType.value='customer';
      modalTitle.value='客户详情';
      showModal.value=true;
    };'''
if old_view in content:
    content = content.replace(old_view, new_view)
    changes += 1
    print('OK: Fixed viewCustomer activities init')
else:
    print('WARN: viewCustomer exact match not found')

# ---- 2. 修复 editCustomer - 保留activities ----
old_edit = '''const editCustomer=(c)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(c)));
      editingId.value=c.id;
      modalType.value='customer';
      modalTitle.value='编辑客户';
      showModal.value=true;
    };'''
new_edit = '''const editCustomer=(c)=>{
      Object.assign(formData,JSON.parse(JSON.stringify({...c,activities:c.activities||[]})));
      editingId.value=c.id;
      modalType.value='customer';
      modalTitle.value='编辑客户';
      showModal.value=true;
    };'''
if old_edit in content:
    content = content.replace(old_edit, new_edit)
    changes += 1
    print('OK: Fixed editCustomer activities init')
else:
    print('WARN: editCustomer exact match not found')

# ---- 3. 确保 saveCustomer 调用save()更新仪表盘 ----
# 在 saveCustomer 的 loadCustomers(); 之前调用 save()
old_save = "loadCustomers();closeModal();showToast('操作成功','success');"
new_save = "loadCustomers();save();closeModal();showToast('操作成功','success');"
if old_save in content:
    content = content.replace(old_save, new_save, 1)
    changes += 1
    print('OK: saveCustomer now calls save()')
else:
    print('WARN: saveCustomer toast not found')

# ---- 4. 在 editCustomer 后添加 getCustomerProjects 和 addCustomerActivity ----
edit_cust_pos = content.find('const editCustomer=(c)=>')
if edit_cust_pos > 0:
    # 找editCustomer函数的结束位置
    # 找下一个函数定义的位置（const xxx= 或 function xxx）
    after_edit = content[edit_cust_pos:]
    # 找函数结束的 };
    end_pos = edit_cust_pos + after_edit.find('    };') + 5
    insert_code = '''
    // 获取客户关联项目列表
    const getCustomerProjects=(customerId)=>{
      const custName=customers.value.find(x=>x.id===customerId)?.name||'';
      return projects.value.filter(p=>p.customerId===customerId||(custName&&p.customerName===custName));
    };
    // 添加客户互动记录
    const addCustomerActivity=()=>{
      const content=prompt('请输入互动内容：');
      if(!content)return;
      const act={type:'沟通',date:new Date().toLocaleDateString('zh-CN'),content};
      const c=customers.value.find(x=>x.id===formData.id);
      if(c){if(!c.activities)c.activities=[];c.activities.push(act);saveCustomer();}
      else{showToast('请先打开客户详情','warning');}
    };'''
    content = content[:end_pos] + insert_code + content[end_pos:]
    changes += 1
    print('OK: Added getCustomerProjects and addCustomerActivity after editCustomer')
else:
    print('WARN: editCustomer not found')

# ---- 5. 更新 return 语句 ----
# 找 return 语句块中的 customer 相关导出
# 找 return { ... } 块
return_match = re.search(r'return\s*\{[^}]*saveTeamMembers[^}]*\}', content)
if return_match:
    old_ret = return_match.group()
    new_ret = old_ret.replace('saveTeamMembers,', 'saveTeamMembers,\n      customerSearchKey,customerFilterStatus,customerFilterLevel,filteredCustomers,\n      getCustomerProjects,addCustomerActivity,')
    content = content.replace(old_ret, new_ret, 1)
    changes += 1
    print('OK: Updated return statement')
else:
    print('WARN: return statement not found')

with open('C:/Users/haizhi/Projects/my-test/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nTotal JS changes: {changes}')
print(f'File size: {len(content)} chars')
