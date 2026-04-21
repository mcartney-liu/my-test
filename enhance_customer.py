import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 客户管理增强 - 4个模块
# 1. 客户表单增强：状态/等级/邮箱/地址/备注
# 2. 客户详情视图：关联项目+互动记录
# 3. 客户卡片增强：显示状态徽章+等级
# 4. 客户搜索/筛选功能
# ============================================================

changes = 0

# ---- 1. 替换客户编辑表单 ----
old_customer_form = '''      <!-- Customer Edit Form -->
      <form v-if="modalType==='customer' && modalTitle==='编辑客户'" @submit.prevent="saveCustomer">
        <div class="form-group"><label for="customer-name-edit">客户名称</label><input type="text" v-model="formData.name" class="form-input" required id="customer-name-edit" name="customerName"></div>
        <div class="form-row">
          <div class="form-group"><label for="customer-industry-edit">所属行业</label><input type="text" v-model="formData.industry" class="form-input" id="customer-industry-edit" name="customerIndustry"></div>
          <div class="form-group"><label for="customer-contact-person-edit">联系人</label><input type="text" v-model="formData.contactPerson" class="form-input" id="customer-contact-person-edit" name="customerContactPerson"></div>
        </div>
          <div class="form-group"><label for="customer-phone-edit">联系电话</label><input type="text" v-model="formData.contactPhone" class="form-input" id="customer-phone-edit" name="customerPhone"></div>
        <div class="modal-footer"><button type="button" class="btn btn-secondary" @click="closeModal">保存</button><button type="submit" class="btn btn-primary">提交</button></div>
      </form>'''

new_customer_form = '''      <!-- Customer Edit Form -->
      <form v-if="modalType==='customer' && modalTitle==='编辑客户'" @submit.prevent="saveCustomer">
        <div class="form-row">
          <div class="form-group"><label for="customer-name-edit">客户名称</label><input type="text" v-model="formData.name" class="form-input" required id="customer-name-edit" name="customerName"></div>
          <div class="form-group"><label for="customer-status-edit">客户状态</label><select v-model="formData.status" class="form-input" id="customer-status-edit"><option value="active">活跃</option><option value="inactive">休眠</option><option value="prospect">潜在</option><option value="churned">流失</option></select></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="customer-industry-edit">所属行业</label><input type="text" v-model="formData.industry" class="form-input" id="customer-industry-edit" name="customerIndustry"></div>
          <div class="form-group"><label for="customer-level-edit">客户等级</label><select v-model="formData.level" class="form-input" id="customer-level-edit"><option value="A">A类（战略客户）</option><option value="B">B类（重点客户）</option><option value="C">C类（普通客户）</option><option value="D">D类（观察客户）</option></select></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="customer-contact-person-edit">联系人</label><input type="text" v-model="formData.contactPerson" class="form-input" id="customer-contact-person-edit" name="customerContactPerson"></div>
          <div class="form-group"><label for="customer-phone-edit">联系电话</label><input type="text" v-model="formData.contactPhone" class="form-input" id="customer-phone-edit" name="customerPhone"></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="customer-email-edit">电子邮箱</label><input type="email" v-model="formData.email" class="form-input" id="customer-email-edit" placeholder="contact@company.com" name="customerEmail"></div>
          <div class="form-group"><label for="customer-address-edit">客户地址</label><input type="text" v-model="formData.address" class="form-input" id="customer-address-edit" placeholder="北京市朝阳区xxx大厦" name="customerAddress"></div>
        </div>
        <div class="form-group"><label for="customer-notes-edit">备注信息</label><textarea v-model="formData.notes" class="form-input" id="customer-notes-edit" rows="3" placeholder="客户背景、需求特点、注意事项..." name="customerNotes"></textarea></div>
        <div class="modal-footer"><button type="button" class="btn btn-secondary" @click="closeModal">保存</button><button type="submit" class="btn btn-primary">提交</button></div>
      </form>'''

if old_customer_form in content:
    content = content.replace(old_customer_form, new_customer_form)
    changes += 1
    print('OK: Replaced customer edit form')
else:
    print('WARN: Customer edit form not found exactly')

# ---- 2. 替换客户新建表单 ----
old_customer_add = '''      <!-- Customer Add Form -->
      <form v-if="modalType==='customer' && modalTitle==='新建客户'" @submit.prevent="saveCustomer">
        <div class="form-group"><label for="customer-name-add">客户名称</label><input type="text" v-model="formData.name" class="form-input" required id="customer-name-add" name="customerName"></div>
        <div class="form-row">
          <div class="form-group"><label for="customer-industry-add">所属行业</label><input type="text" v-model="formData.industry" class="form-input" id="customer-industry-add" name="customerIndustry"></div>
          <div class="form-group"><label for="customer-contact-person-add">联系人</label><input type="text" v-model="formData.contactPerson" class="form-input" id="customer-contact-person-add" name="customerContactPerson"></div>
        </div>
          <div class="form-group"><label for="customer-phone-add">联系电话</label><input type="text" v-model="formData.contactPhone" class="form-input" id="customer-phone-add" name="customerPhone"></div>
        <div class="modal-footer"><button type="button" class="btn btn-secondary" @click="closeModal">保存</button><button type="submit" class="btn btn-primary">提交</button></div>
      </form>'''

new_customer_add = '''      <!-- Customer Add Form -->
      <form v-if="modalType==='customer' && modalTitle==='新建客户'" @submit.prevent="saveCustomer">
        <div class="form-row">
          <div class="form-group"><label for="customer-name-add">客户名称</label><input type="text" v-model="formData.name" class="form-input" required id="customer-name-add" name="customerName"></div>
          <div class="form-group"><label for="customer-status-add">客户状态</label><select v-model="formData.status" class="form-input" id="customer-status-add"><option value="active">活跃</option><option value="prospect">潜在</option><option value="inactive">休眠</option><option value="churned">流失</option></select></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="customer-industry-add">所属行业</label><input type="text" v-model="formData.industry" class="form-input" id="customer-industry-add" name="customerIndustry" placeholder="电力/金融/政府等"></div>
          <div class="form-group"><label for="customer-level-add">客户等级</label><select v-model="formData.level" class="form-input" id="customer-level-add"><option value="B">B类（重点客户）</option><option value="A">A类（战略客户）</option><option value="C">C类（普通客户）</option><option value="D">D类（观察客户）</option></select></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="customer-contact-person-add">联系人</label><input type="text" v-model="formData.contactPerson" class="form-input" id="customer-contact-person-add" name="customerContactPerson" placeholder="张三"></div>
          <div class="form-group"><label for="customer-phone-add">联系电话</label><input type="text" v-model="formData.contactPhone" class="form-input" id="customer-phone-add" name="customerPhone" placeholder="138xxxx8888"></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="customer-email-add">电子邮箱</label><input type="email" v-model="formData.email" class="form-input" id="customer-email-add" placeholder="contact@company.com" name="customerEmail"></div>
          <div class="form-group"><label for="customer-address-add">客户地址</label><input type="text" v-model="formData.address" class="form-input" id="customer-address-add" placeholder="北京市朝阳区xxx大厦" name="customerAddress"></div>
        </div>
        <div class="form-group"><label for="customer-notes-add">备注信息</label><textarea v-model="formData.notes" class="form-input" id="customer-notes-add" rows="3" placeholder="客户背景、需求特点、注意事项..." name="customerNotes"></textarea></div>
        <div class="modal-footer"><button type="button" class="btn btn-secondary" @click="closeModal">保存</button><button type="submit" class="btn btn-primary">提交</button></div>
      </form>'''

if old_customer_add in content:
    content = content.replace(old_customer_add, new_customer_add)
    changes += 1
    print('OK: Replaced customer add form')
else:
    print('WARN: Customer add form not found exactly')

# ---- 3. 替换客户详情视图 ----
old_customer_detail = '''      <!-- Customer Detail View -->
      <div v-if="modalType==='customer' && modalTitle==='客户详情'" class="customer-detail detail-view">
        <div style="text-align:center;margin-bottom:24px;">
          <div style="width:80px;height:80px;margin:0 auto 16px;background:linear-gradient(135deg,rgba(99,102,241,0.1) 0%,rgba(129,140,248,0.1) 100%);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:36px;">🏢</div>
          <h3 style="font-size:22px;font-weight:700;margin-bottom:10px;">{{formData.name||'暂无名称'}}</h3>
          <span class="badge badge-info">{{formData.industry||'行业'}}</span>
        </div>
        <div class="detail-grid">
          <div class="detail-item hover-lift" style="padding:20px;background:linear-gradient(135deg,rgba(99,102,241,0.05) 0%,rgba(129,140,248,0.05) 100%);border-radius:var(--radius);">
            <div style="display:flex;align-items:center;gap:16px;">
              <div style="width:44px;height:44px;background:var(--bg);border-radius:12px;display:flex;align-items:center;justify-content:center;"><i data-lucide="user" class="icon-lg" style="color:var(--primary);"></i></div>
              <div style="font-size:12px;color:var(--muted);margin-bottom:4px;">联系人</div><div style="font-weight:600;font-size:16px;">{{formData.contactPerson||'无'}}</div>
            </div>
          </div>
          <div class="detail-item hover-lift" style="padding:20px;background:linear-gradient(135deg,rgba(16,185,129,0.05) 0%,rgba(52,239,125,0.05) 100%);border-radius:var(--radius);">
            <div style="display:flex;align-items:center;gap:16px;">
              <div style="width:44px;height:44px;background:var(--bg);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;">📞</div>
              <div style="font-size:12px;color:var(--muted);margin-bottom:4px;">联系电话</div><div style="font-weight:600;font-size:16px;">{{formData.contactPhone||'无'}}</div>
            </div>
          </div>
        </div>
        <div style="margin-top:24px;padding-top:20px;border-top:1px solid var(--border);display:flex;gap:12px;justify-content:flex-end;">
          <button class="btn btn-secondary" @click="closeModal">关闭</button>
          <button class="btn btn-primary" @click="editCustomer(formData)">编辑</button>
        </div>
      </div>'''

new_customer_detail = '''      <!-- Customer Detail View -->
      <div v-if="modalType==='customer' && modalTitle==='客户详情'" class="customer-detail detail-view">
        <!-- 头部信息 -->
        <div style="text-align:center;margin-bottom:20px;">
          <div style="width:80px;height:80px;margin:0 auto 12px;background:var(--gradient-primary);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:36px;color:#fff;font-weight:700;">{{(formData.name||'?').charAt(0)}}</div>
          <h3 style="font-size:22px;font-weight:700;margin-bottom:8px;">{{formData.name||'暂无名称'}}</h3>
          <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap;">
            <span class="badge badge-info">{{formData.industry||'未知行业'}}</span>
            <span v-if="formData.level" class="badge" :class="formData.level==='A'?'badge-warning':formData.level==='B'?'badge-purple':formData.level==='C'?'badge-info':'badge-gray'">
              {{formData.level}}类客户
            </span>
            <span class="badge" :class="formData.status==='active'?'badge-success':formData.status==='prospect'?'badge-info':formData.status==='inactive'?'badge-gray':'badge-danger'">
              {{formData.status==='active'?'活跃':formData.status==='prospect'?'潜在':formData.status==='inactive'?'休眠':'流失'}}
            </span>
          </div>
        </div>

        <!-- 基础信息卡片 -->
        <div class="detail-grid">
          <div class="detail-item hover-lift" style="padding:16px;background:linear-gradient(135deg,rgba(99,102,241,0.05) 0%,rgba(129,140,248,0.05) 100%);border-radius:var(--radius);">
            <div style="font-size:12px;color:var(--muted);margin-bottom:4px;">联系人</div>
            <div style="font-weight:600;font-size:15px;">{{formData.contactPerson||'—'}}</div>
          </div>
          <div class="detail-item hover-lift" style="padding:16px;background:linear-gradient(135deg,rgba(16,185,129,0.05) 0%,rgba(52,239,125,0.05) 100%);border-radius:var(--radius);">
            <div style="font-size:12px;color:var(--muted);margin-bottom:4px;">联系电话</div>
            <div style="font-weight:600;font-size:15px;">{{formData.contactPhone||'—'}}</div>
          </div>
          <div v-if="formData.email" class="detail-item hover-lift" style="padding:16px;background:var(--bg);border-radius:var(--radius);">
            <div style="font-size:12px;color:var(--muted);margin-bottom:4px;">电子邮箱</div>
            <div style="font-weight:600;font-size:14px;word-break:break-all;">{{formData.email}}</div>
          </div>
          <div v-if="formData.address" class="detail-item hover-lift" style="padding:16px;background:var(--bg);border-radius:var(--radius);">
            <div style="font-size:12px;color:var(--muted);margin-bottom:4px;">客户地址</div>
            <div style="font-size:13px;line-height:1.4;">{{formData.address}}</div>
          </div>
        </div>

        <!-- 备注信息 -->
        <div v-if="formData.notes" style="margin-top:16px;padding:14px;background:rgba(245,158,11,0.08);border-radius:12px;border-left:3px solid var(--warning);">
          <div style="font-size:12px;color:var(--warning);margin-bottom:6px;font-weight:600;">备注信息</div>
          <div style="font-size:13px;line-height:1.6;color:var(--text-secondary);">{{formData.notes}}</div>
        </div>

        <!-- 关联项目列表 -->
        <div v-if="getCustomerProjects(formData.id).length" style="margin-top:20px;">
          <div style="font-size:13px;font-weight:600;margin-bottom:10px;color:var(--text);display:flex;align-items:center;gap:6px;">
            <i data-lucide="folder" style="width:14px;height:14px;color:var(--primary);"></i> 关联项目
          </div>
          <div style="display:flex;flex-direction:column;gap:8px;">
            <div v-for="proj in getCustomerProjects(formData.id)" :key="proj.id"
              style="padding:12px 14px;background:var(--bg);border-radius:10px;border:1px solid var(--border);cursor:pointer;"
              @click="viewProject(proj)">
              <div style="font-size:14px;font-weight:600;margin-bottom:4px;">{{proj.name}}</div>
              <div style="display:flex;gap:10px;font-size:12px;color:var(--muted);">
                <span>{{proj.status||'进行中'}}</span>
                <span v-if="proj.budget">¥{{formatMoney(proj.budget)}}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 互动记录 -->
        <div style="margin-top:20px;">
          <div style="font-size:13px;font-weight:600;margin-bottom:10px;color:var(--text);display:flex;align-items:center;gap:6px;justify-content:space-between;">
            <span style="display:flex;align-items:center;gap:6px;">
              <i data-lucide="activity" style="width:14px;height:14px;color:var(--info);"></i> 互动记录
            </span>
            <button class="btn btn-secondary btn-sm" @click="addCustomerActivity">+ 添加记录</button>
          </div>
          <div v-if="formData.activities && formData.activities.length" style="display:flex;flex-direction:column;gap:8px;">
            <div v-for="(act,idx) in (formData.activities||[]).slice().reverse()" :key="idx"
              style="padding:12px 14px;background:var(--bg);border-radius:10px;border-left:3px solid var(--primary);">
              <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:6px;">
                <span class="badge badge-info" style="font-size:10px;">{{act.type||'沟通'}}</span>
                <span style="font-size:11px;color:var(--muted);">{{act.date||''}}</span>
              </div>
              <div style="font-size:13px;line-height:1.5;">{{act.content||''}}</div>
            </div>
          </div>
          <div v-else style="text-align:center;padding:20px;color:var(--muted);font-size:13px;">
            暂无互动记录，点击上方"+ 添加记录"添加首次沟通记录
          </div>
        </div>

        <div style="margin-top:24px;padding-top:20px;border-top:1px solid var(--border);display:flex;gap:12px;justify-content:flex-end;">
          <button class="btn btn-secondary" @click="closeModal">关闭</button>
          <button class="btn btn-primary" @click="editCustomer(formData)">编辑</button>
        </div>
      </div>'''

if old_customer_detail in content:
    content = content.replace(old_customer_detail, new_customer_detail)
    changes += 1
    print('OK: Replaced customer detail view')
else:
    print('WARN: Customer detail view not found exactly')

# ---- 4. 增强客户卡片显示（状态+等级徽章）----
# 找到客户卡片中的"<!-- Paul：客户卡片头部 -->"区域，在联系人信息前加状态/等级徽章
old_card_head = '''            <!-- Paul：客户卡片头部 -->
            <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:12px;">
              <div>
                <div style="font-size:16px;font-weight:600;margin-bottom:4px;color:#f1f5f9;">{{c.name}}</div>
                <div style="font-size:12px;color:#94a3b8;">{{c.industry||'暂无行业'}}</div>
              </div>'''

new_card_head = '''            <!-- 客户卡片头部：状态+等级徽章 -->
            <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:12px;">
              <div>
                <div style="display:flex;gap:6px;margin-bottom:6px;flex-wrap:wrap;">
                  <span class="badge" :class="c.level==='A'?'badge-warning':c.level==='B'?'badge-purple':c.level==='C'?'badge-info':'badge-gray'" style="font-size:10px;">
                    {{c.level||'C'}}类
                  </span>
                  <span class="badge" :class="c.status==='active'?'badge-success':c.status==='prospect'?'badge-info':c.status==='inactive'?'badge-gray':'badge-danger'" style="font-size:10px;">
                    {{c.status==='active'?'活跃':c.status==='prospect'?'潜在':c.status==='inactive'?'休眠':'流失'}}
                  </span>
                </div>
                <div style="font-size:16px;font-weight:600;margin-bottom:2px;color:#f1f5f9;">{{c.name}}</div>
                <div style="font-size:12px;color:#94a3b8;">{{c.industry||'暂无行业'}}</div>
              </div>'''

if old_card_head in content:
    content = content.replace(old_card_head, new_card_head)
    changes += 1
    print('OK: Enhanced customer card with status/level badges')
else:
    print('WARN: Customer card head not found')

# ---- 5. 增强客户列表显示：加筛选搜索栏 ----
# 在客户管理页面的 toolbar 后面加入搜索+筛选
old_toolbar = '''        <div class="toolbar"><button class="btn btn-primary" @click="openModal('customer')">+ 新建客户</button></div>

        <!-- 客户价值排行榜 -->'''

new_toolbar = '''        <div class="toolbar">
          <button class="btn btn-primary" @click="openModal('customer')">+ 新建客户</button>
          <div style="display:flex;gap:8px;margin-left:auto;align-items:center;">
            <input type="text" v-model="customerSearchKey" placeholder="搜索客户..." class="form-input" style="width:180px;padding:6px 12px;font-size:13px;">
            <select v-model="customerFilterStatus" class="form-input" style="width:110px;padding:6px 8px;font-size:13px;">
              <option value="">全部状态</option>
              <option value="active">活跃</option>
              <option value="prospect">潜在</option>
              <option value="inactive">休眠</option>
              <option value="churned">流失</option>
            </select>
            <select v-model="customerFilterLevel" class="form-input" style="width:100px;padding:6px 8px;font-size:13px;">
              <option value="">全部等级</option>
              <option value="A">A类客户</option>
              <option value="B">B类客户</option>
              <option value="C">C类客户</option>
              <option value="D">D类客户</option>
            </select>
          </div>
        </div>

        <!-- 客户价值排行榜 -->'''

if old_toolbar in content:
    content = content.replace(old_toolbar, new_toolbar)
    changes += 1
    print('OK: Added customer search + filter toolbar')
else:
    print('WARN: Customer toolbar not found')

# ---- 6. 更新客户卡片v-for筛选 ----
old_card_for = '''        <div style="display:flex;flex-wrap:wrap;gap:20px;" v-if="customers.length">
          <div v-for="c in customers" :key="c.id" @click="viewCustomer(c)"'''

new_card_for = '''        <div style="display:flex;flex-wrap:wrap;gap:20px;" v-if="filteredCustomers.length">
          <div v-for="c in filteredCustomers" :key="c.id" @click="viewCustomer(c)"'''

if old_card_for in content:
    content = content.replace(old_card_for, new_card_for)
    changes += 1
    print('OK: Updated v-for to filteredCustomers')
else:
    print('WARN: Customer v-for not found')

# 也更新排行榜的v-if
old_ranking_if = '''        <div class="customer-ranking-container" v-if="customerValueRanking.length">'''
new_ranking_if = '''        <div class="customer-ranking-container" v-if="customerValueRanking.length && !customerSearchKey && !customerFilterStatus && !customerFilterLevel">'''
if old_ranking_if in content:
    content = content.replace(old_ranking_if, new_ranking_if)
    changes += 1
    print('OK: Hide ranking when filtering')

with open('C:/Users/haizhi/Projects/my-test/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nTotal changes: {changes}')
print(f'File size: {len(content)} chars')
