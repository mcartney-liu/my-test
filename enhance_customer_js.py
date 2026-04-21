import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

changes = 0

# ---- 1. 添加客户搜索筛选相关的ref和computed ----
# 在 customers=ref([]) 附近添加
old_data = 'const customers=ref([]);'
new_data = '''const customers=ref([]);
    // 客户搜索与筛选
    const customerSearchKey=ref('');
    const customerFilterStatus=ref('');
    const customerFilterLevel=ref('');
    const filteredCustomers=computed(()=>{
      return customers.value.filter(c=>{
        const matchSearch=!customerSearchKey.value || c.name?.includes(customerSearchKey.value) || c.industry?.includes(customerSearchKey.value) || c.contactPerson?.includes(customerSearchKey.value);
        const matchStatus=!customerFilterStatus.value || c.status===customerFilterStatus.value;
        const matchLevel=!customerFilterLevel.value || c.level===customerFilterLevel.value;
        return matchSearch && matchStatus && matchLevel;
      });
    });'''

if old_data in content:
    content = content.replace(old_data, new_data)
    changes += 1
    print('OK: Added customer search/filter refs and computed')
else:
    print('WARN: customers=ref([]) not found')

# ---- 2. 添加 getCustomerProjects 和 addCustomerActivity 函数 ----
# 找 editCustomer 函数，在其后添加
# 先找到 editCustomer 函数的位置
edit_customer_match = re.search(r'const editCustomer=(c)=>', content)
if edit_customer_match:
    pos = edit_customer_match.start()
    # 在 editCustomer 函数后插入新函数
    insert_point = content.find('\n  };', pos + 200) + 4
    new_funcs = '''
    // 获取客户关联项目
    const getCustomerProjects=(customerId)=>{
      return projects.value.filter(p=>p.customerId===customerId||p.customerName===customers.value.find(c=>c.id===customerId)?.name);
    };
    // 添加客户互动记录
    const addCustomerActivity=()=>{
      const act={type:'沟通',date:new Date().toLocaleDateString('zh-CN'),content:prompt('请输入互动内容：')||''};
      if(!act.content)return;
      const c=customers.value.find(x=>x.id===formData.value.id);
      if(c){if(!c.activities)c.activities=[];c.activities.push(act);saveCustomers();}
    };'''
    content = content[:insert_point] + new_funcs + content[insert_point:]
    changes += 1
    print('OK: Added getCustomerProjects and addCustomerActivity')
else:
    print('WARN: editCustomer function not found')

# ---- 3. 添加 saveCustomers 函数（如果不存在）----
if 'const saveCustomers' not in content:
    save_funcs_match = re.search(r'const saveCustomers=', content)
    if save_funcs_match:
        print('WARN: saveCustomers already exists')
    else:
        # 找 saveTeamMembers 的位置，在其后添加
        save_tm = re.search(r'const saveTeamMembers=\(\)=>', content)
        if save_tm:
            pos = save_tm.start()
            end = content.find('\n  };', pos + 100) + 4
            new_save = '''
    const saveCustomers=()=>{localStorage.setItem('pm-os-customers',JSON.stringify(customers.value));};'''
            content = content[:end] + new_save + content[end:]
            changes += 1
            print('OK: Added saveCustomers function')
        else:
            print('WARN: saveTeamMembers not found')
else:
    print('saveCustomers already exists')

# ---- 4. 确保 saveCustomer 调用 saveCustomers ----
# 在 saveCustomer 函数中添加 saveCustomers() 调用
old_save_cust = "const saveCustomer=()=>{const d={...formData.value,id:d.id||generateId(),updatedAt:new Date().toISOString()};const idx=customers.value.findIndex(x=>x.id===d.id);if(idx>-1){customers.value[idx]=d;}else{customers.value.push(d);}save();closeModal();};"
new_save_cust = "const saveCustomer=()=>{const d={...formData.value,id:d.id||generateId(),updatedAt:new Date().toISOString()};const idx=customers.value.findIndex(x=>x.id===d.id);if(idx>-1){customers.value[idx]=d;}else{customers.value.push(d);}save();saveCustomers();closeModal();};"
if old_save_cust in content:
    content = content.replace(old_save_cust, new_save_cust)
    changes += 1
    print('OK: Updated saveCustomer to call saveCustomers')
else:
    print('WARN: saveCustomer body not found, trying alternative search')
    # 尝试模糊搜索
    if 'const saveCustomer=()=>{const d={...formData.value' in content:
        m = re.search(r"const saveCustomer=\(\)=>\{const d=\{...formData\.value[^}]{0,300}save\(\);closeModal\(\);\}[^}]*\}", content)
        if m:
            old = m.group()
            # 找到 save();closeModal() 改为 save();saveCustomers();closeModal()
            new_s = old.replace('save();', 'save();saveCustomers();')
            content = content.replace(old, new_s, 1)
            changes += 1
            print('OK: Updated saveCustomer (alt)')

# ---- 5. 确保 viewCustomer 设置 activities ----
old_view_cust = "const viewCustomer=(c)=>{formData.value={...c};modalTitle.value='客户详情';modalType.value='customer';openModal();};"
new_view_cust = "const viewCustomer=(c)=>{formData.value={...c,activities:c.activities||[]};modalTitle.value='客户详情';modalType.value='customer';openModal();};"
if old_view_cust in content:
    content = content.replace(old_view_cust, new_view_cust)
    changes += 1
    print('OK: Updated viewCustomer to init activities')
else:
    print('WARN: viewCustomer not found exactly')
    # 模糊找
    if 'const viewCustomer=(c)=>{formData.value={...c}' in content:
        m = re.search(r'const viewCustomer=\(c\)=>\{formData\.value=\{[^}]+\};modalTitle\.value=\'客户详情\'', content)
        if m:
            old = m.group()
            new_v = "const viewCustomer=(c)=>{formData.value={...c,activities:c.activities||[]};modalTitle.value='客户详情'"
            content = content.replace(old, new_v, 1)
            changes += 1
            print('OK: Updated viewCustomer (alt)')

# ---- 6. 添加 return 语句中的导出 ----
old_return_end = 'saveTeamMembers,'
new_return_end = '''saveTeamMembers,
      customerSearchKey,customerFilterStatus,customerFilterLevel,filteredCustomers,
      getCustomerProjects,addCustomerActivity,'''

if old_return_end in content:
    content = content.replace(old_return_end, new_return_end)
    changes += 1
    print('OK: Updated return statement with customer functions')
else:
    print('WARN: saveTeamMembers in return not found')

with open('C:/Users/haizhi/Projects/my-test/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nJS changes: {changes}')
print(f'File size: {len(content)} chars')
