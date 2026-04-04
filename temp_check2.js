
// 全局错误捕获 - 防止界面变黑
window.addEventListener('error', function(event) {
  console.error('全局捕获的JavaScript错误:', event.error);
  // 只记录错误，不阻止浏览器默认处理，避免资源加载失败导致页面异常
  // 显示友好错误消息
  try {
    const toastElement = document.createElement('div');
    toastElement.style.cssText = `
      position: fixed; top: 20px; right: 20px; z-index: 99999;
      background: rgba(239, 68, 68, 0.9); color: white; padding: 12px 20px;
      border-radius: 10px; max-width: 400px; box-shadow: 0 5px 20px rgba(0,0,0,0.2);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    `;
    toastElement.textContent = '发现JS错误，但系统已保护，请刷新重试';
    document.body.appendChild(toastElement);
    setTimeout(() => toastElement.remove(), 5000);
  } catch (e) {
    // 如果显示toast失败，静默处理
  }
});

// 检测语音输入页面是否正常工作
function testVoicePage() {
  try {
    console.log('语音输入页面诊断...');
    // 测试Vue是否正常工作
    if (!window.Vue) throw new Error('Vue未加载');
    console.log('✅ Vue加载正常');
    
    // 测试语音识别API是否可用
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
      console.warn('⚠️ 浏览器不支持语音识别API');
    } else {
      console.log('✅ 浏览器支持语音识别API');
    }
    
    return true;
  } catch (error) {
    console.error('语音输入页面诊断失败:', error);
    return false;
  }
}

const{createApp,ref,reactive,computed,onMounted,nextTick,watch}=Vue;

const app=createApp({
  setup(){
    // State
    const isLoggedIn=ref(false);
    const user=ref({});
    const currentPage=ref('dashboard');
    const projects=ref([]);
    const customers=ref([]);
    const tasks=ref([]);
    const issues=ref([]);
    const experiences=ref([]);
    const capabilities=ref([]);
    const diaries=ref([]);
    const teamMembers=ref([]);
    const files=ref([]);
    const meetings=ref([]);
    const searchKeyword=ref('');
    const searchTaskKeyword=ref('');
    const statusFilter=ref('');
    const positionFilter=ref('');
    const showModal=ref(false);
    const modalType=ref('');
    const modalTitle=ref('');
    const formData=reactive({
      // 项目相关字段
      name: '', clientName: '', projectType: '', status: '', startDate: '', planEndDate: '', 
      budget: '', progress: 0, description: '',
      // 任务相关字段
      priority: '', dueDate: '', assignee: '', 
      // 客户相关字段
      industry: '', contactPerson: '', contactPhone: '', contactEmail: '', companyAddress: '',
      // 问题相关字段
      issueType: '', severity: '', reporter: '', 
      // 经验相关字段
      category: '', context: '', conclusion: '',
      // 能力相关字段
      capabilityName: '', currentLevel: '', targetLevel: '', selfAssessment: '', improvementPlan: '',
      // 日记相关字段
      title: '', date: '', mood: '', content: '', tags: '', tomorrow: '',
      // 会议相关字段
      time: '', type: '', location: '', participants: '', summary: '', actionItems: '',
      // 人员相关字段
      gender: '', phone: '', email: '', position: '', nature: '', joinYear: '', department: '',
      dailyRate: '', costType: '', workStatus: '', remark: '', projectHistory: []
    });
    const editingId=ref(null);
    const toast=reactive({show:false,message:'',type:'info'});
    const loginForm=reactive({username:'',password:''});
    const aiConfig=reactive({apiKey:''});
    
    // Voice state
    const voiceRecording=ref(false);
    const voiceStatus=ref('正在聆听，请说话...');
    const voiceText=ref('');
    const aiResult=ref(null);
    const savingToTable=ref(false);
    const selectedEntities=ref([]); // 存储选中的实体索引
    let recognition=null;
    let finalTranscript='';
    
    // Chat state
    const chatInput=ref('');
    const chatMessages=ref([]);
    const chatHistory=ref(JSON.parse(localStorage.getItem('chatHistory') || '[]'));
    const currentSessionId=ref(null);
    const chatLoading=ref(false);
    const chatVoiceRecording=ref(false);
    const chatVoiceStatus=ref('正在录音');
    let chatRecognition=null;
    let chatFinalTranscript='';

    // AI 意图识别状态
    const pendingCommand=ref(null);  // 待执行的命令
    const intentType=ref('');  // 意图类型: query, create, update, delete, summary, analyze

    // 流式输出状态
    const streamingContent=ref('');  // 当前流式输出的内容
    const isStreaming=ref(false);  // 是否正在流式输出
    let streamingAbortController=null;  // 用于取消流式请求

    // Computed
    const stats=computed(()=>({
      totalProjects:projects.value.length,
      activeProjects:projects.value.filter(p=>p.status==='进行中').length,
      pendingTasks:tasks.value.filter(t=>t.status!=='已完成').length,
      openIssues:issues.value.filter(i=>i.status==='待处理'||i.status==='进行中').length,
      experienceCount:experiences.value.length
    }));

    const activeProjects=computed(()=>projects.value.filter(p=>p.status==='进行中').slice(0,4));
    const filteredProjects=computed(()=>{
      let data=projects.value;
      if(searchKeyword.value)data=data.filter(p=>p.name.includes(searchKeyword.value));
      if(statusFilter.value)data=data.filter(p=>p.status===statusFilter.value);
      return data;
    });
    const filteredTasks=computed(()=>{
      let data=tasks.value;
      if(searchTaskKeyword.value)data=data.filter(t=>t.name.includes(searchTaskKeyword.value));
      return data;
    });
    const filteredMeetings=computed(()=>{
      let data=meetings.value;
      if(searchKeyword.value)data=data.filter(m=>(m.title||'').includes(searchKeyword.value)||(m.summary||'').includes(searchKeyword.value));
      return data;
    });
    const memberProjectHistoryStr=ref('');
    const filteredDiaries=computed(()=>{
      let data=diaries.value;
      if(searchKeyword.value)data=data.filter(d=>(d.title||'').includes(searchKeyword.value)||(d.content||'').includes(searchKeyword.value));
      return data.sort((a,b)=>new Date(b.date)-new Date(a.date));
    });
    const filteredTeamMembers=computed(()=>{
      let data=teamMembers.value;
      if(searchKeyword.value)data=data.filter(m=>(m.name||'').includes(searchKeyword.value)||(m.email||'').includes(searchKeyword.value));
      if(statusFilter.value)data=data.filter(m=>m.workStatus===statusFilter.value);
      if(positionFilter.value)data=data.filter(m=>m.position===positionFilter.value);
      return data;
    });

    // AI Configuration
    const saveAiConfig=()=>{
      localStorage.setItem('pmos_ai_config',JSON.stringify(aiConfig));
      showToast('操作成功','success');
    };

    // Voice Recognition
    const initVoiceRecognition=()=>{
      try {
        if(!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)){
          console.warn('浏览器不支持语音识别API');
          showToast('您的浏览器不支持语音识别功能，请使用文本输入','warning');
          return false;
        }
        
        const SpeechRecognition=window.SpeechRecognition||window.webkitSpeechRecognition;
        recognition=new SpeechRecognition();
        recognition.continuous=true;
        recognition.interimResults=true;
        recognition.lang='zh-CN';
        
        recognition.onstart=()=>{
          voiceRecording.value=true;
          voiceStatus.value='🎤 正在聆听，请说话...';
          finalTranscript='';
          showToast('语音识别已启动','info');
        };
        
        recognition.onresult=(event)=>{
          let interim='';
          for(let i=event.resultIndex;i<event.results.length;i++){
            const transcript=event.results[i][0].transcript;
            if(event.results[i].isFinal){
              finalTranscript+=transcript;
            }else{
              interim+=transcript;
            }
          }
          voiceText.value=finalTranscript+interim;
          voiceStatus.value='🎤 正在聆听，请说话...';
        };
        
        recognition.onend=()=>{
          voiceRecording.value=false;
          if(finalTranscript && finalTranscript.trim()){
            voiceStatus.value='正在分析语音内容...';
            showToast('语音识别完成，正在分析...','info');
            analyzeWithAI(finalTranscript);
          }else{
            voiceStatus.value='未检测到语音，请重试';
            showToast('未检测到语音，请重试','warning');
          }
        };
        
        recognition.onerror=(event)=>{
          voiceRecording.value=false;
          console.error('语音识别错误:', event.error);
          
          let errorMessage='语音识别错误: ';
          switch(event.error){
            case 'not-allowed':
              errorMessage+='用户拒绝了麦克风权限';
              break;
            case 'service-not-allowed':
              errorMessage+='浏览器不支持语音识别服务';
              break;
            case 'network':
              errorMessage+='网络连接问题';
              break;
            case 'no-speech':
              errorMessage+='未检测到语音';
              break;
            default:
              errorMessage+=event.error;
          }
          
          voiceStatus.value=errorMessage;
          showToast(errorMessage,'error');
        };
        
        return true;
      }catch(error){
        console.error('语音识别初始化失败:', error);
        showToast('语音识别初始化失败: ' + error.message,'error');
        voiceStatus.value='语音识别初始化失败';
        return false;
      }
    };

    const toggleVoice=()=>{
      // 安全检查：确保页面没有崩溃
      if (!document.getElementById('app')) {
        console.error('页面元素丢失，可能已崩溃');
        showToast('页面遇到问题，请刷新重试', 'error');
        return;
      }
      
      try {
        console.log('开始语音识别操作，当前recognition状态:', recognition ? '已初始化' : '未初始化');
        
        if(!recognition){
          // 尝试初始化语音识别，但设置安全超时
          const initResult = initVoiceRecognition();
          if(!initResult || !recognition){
            console.log('语音识别初始化失败，使用文本输入模式');
            showToast('语音识别不可用，请使用文本输入', 'warning');
            
            // 切换到文本输入状态
            voiceStatus.value = '语音识别不可用，请使用文本输入';
            
            // 如果文本输入区域不存在，创建一个简单的文本输入
            const voicePanel = document.querySelector('.voice-panel');
            if (voicePanel && !voicePanel.querySelector('textarea')) {
              console.log('创建应急文本输入框');
              const textarea = document.createElement('textarea');
              textarea.placeholder = '请在此输入文本...';
              textarea.style.cssText = 'width:100%;min-height:80px;padding:10px;margin-top:20px;';
              voicePanel.appendChild(textarea);
            }
            return;
          }
        }
        
        if(voiceRecording.value){
          console.log('停止录音');
          try {
            recognition.stop();
          } catch (stopError) {
            console.warn('停止录音时出错:', stopError);
            voiceRecording.value = false;
            voiceStatus.value = '录音已停止';
          }
        }else{
          console.log('开始录音');
          aiResult.value=null;
          voiceText.value='';
          voiceStatus.value='正在启动语音识别...';
          
          // 使用更安全的方式启动语音识别
          setTimeout(()=>{
            try {
              if (!recognition) {
                throw new Error('语音识别对象不存在');
              }
              recognition.start();
              console.log('语音识别已启动');
            }catch(error){
              console.error('语音识别启动失败:', error);
              voiceRecording.value=false;
              voiceStatus.value='语音识别启动失败，请使用文本输入';
              
              // 提供友好的错误信息和替代方案
              let errorMsg = '语音识别启动失败';
              if (error.message.includes('permission') || error.message.includes('权限')) {
                errorMsg += '，请检查麦克风权限';
              } else if (error.message.includes('not-supported')) {
                errorMsg += '，浏览器不支持语音识别';
              }
              showToast(errorMsg + '，请使用文本输入', 'warning');
            }
          },500); // 增加延迟，确保UI已更新
        }
      }catch(error){
        console.error('语音识别操作错误:', error);
        voiceRecording.value=false;
        voiceStatus.value='语音识别异常，请使用文本输入';
        
        // 不显示详细错误给用户，避免界面变黑
        showToast('语音功能暂时不可用，请使用文本输入', 'warning');
        
        // 确保页面不崩溃
        if (window.testVoicePage) {
          window.testVoicePage();
        }
      }
    };

    // 文本输入处理函数
    const analyzeTextInput=()=>{
      if(!voiceText.value || voiceText.value.trim()===''){
        showToast('请输入文本内容','warning');
        return;
      }
      
      if(!recognition){
        showToast('请先登录并配置智谱AI API Key','error');
        return;
      }
      
      // 清除之前的AI结果
      aiResult.value=null;
      selectedEntities.value=[];
      
      // 显示分析状态
      voiceStatus.value='正在分析文本...';
      showToast('开始分析文本内容','info');
      
      // 调用AI分析
      analyzeWithAI(voiceText.value);
    };

    const clearTextInput=()=>{
      voiceText.value='';
      aiResult.value=null;
      selectedEntities.value=[];
      voiceStatus.value='请输入文本或使用语音输入';
      showToast('已清空文本输入','info');
    };

    // AI Analysis with Zhipu - 增强版，支持多实体识别
    const analyzeWithAI=async(text)=>{
      const config=JSON.parse(localStorage.getItem('pmos_ai_config')||'{}');
      if(!config.apiKey){
        showToast('请先在设置页面配置智谱AI API Key','error');
        return;
      }
      
      // Prepare data context
      const projectList=projects.value.map(p=>p.name+' | 客户:'+(p.clientName||'无')+' | 状态:'+p.status+' | 进度:'+(p.progress||0)+'%').join('\n');
      const taskList=tasks.value.map(t=>t.name+' | 优先级:'+(t.priority||'无')+' | 截止期:'+(t.dueDate||'无')+' | 负责人:'+(t.assignee||'无')).join('\n');
      const customerList=customers.value.map(c=>c.name+' | 行业:'+(c.industry||'暂无')+' | 联系人:'+(c.contactPerson||'无')).join('\n');
      const issueList=issues.value.map(i=>i.title+' | 类型:'+(i.issueType==='risk'?'风险':'缺陷')+' | 状态:'+i.status).join('\n');
      const experienceList=experiences.value.map(e=>e.title+' | 分类:'+(e.category||'无')).join('\n');
      const capabilityList=capabilities.value.map(c=>c.capabilityName+' | '+c.category).join('\n');
      const memberList=teamMembers.value.map(m=>m.name+' | 岗位:'+(m.position||'无')+' | 状态:'+(m.workStatus||'在职')+' | 性质:'+(m.nature||'自有')).join('\n');
      
      const dataContext=`当前系统已有数据：
项目信息: ${projects.value.length}个
${projectList}

任务信息: ${tasks.value.length}个  
${taskList}

客户信息: ${customers.value.length}个
${customerList}

人员信息: ${teamMembers.value.length}个
${memberList}

问题信息: ${issues.value.length}个
${issueList}

经验信息: ${experiences.value.length}个
${experienceList}

能力信息: ${capabilities.value.length}个
${capabilityList}`;

      const userPrompt=`请仔细分析以下语音输入，识别其中可能包含的多个实体信息（人员、项目、客户、任务、问题、经验、能力等），并提取关键信息。

语音内容: "${text}"

重要提示：
1. 一段话可能包含多个不同类型的实体，例如："我有一个同事张三，我们一起做过湖北电力数字化审计项目" 这句话包含了人员（张三）、项目（湖北电力数字化审计项目）和客户（湖北电力）
2. 特别注意客户实体的识别：当语音中提到公司名称、企业、集团、机构等，特别是与项目相关的，应识别为客户实体
3. 实体可能属于当前系统，也可能是过去或未来的信息
4. 请尽可能提取完整信息，缺失的字段可以留空
5. 对于客户实体，至少需要提供name字段，尽可能推断行业(industry)信息

请按照以下JSON数组格式返回，每个元素是一个实体：
[
  {
    "type": "实体类型", // 可选值: "member"（人员）, "project"（项目）, "customer"（客户）, "task"（任务）, "issue"（问题）, "experience"（经验）, "capability"（能力）, "diary"（日记）
    "data": {
      // 根据类型填充对应字段，以下为各类型字段示例：
      // member: name, gender, phone, email, position, nature, joinYear, department, dailyRate, costType, workStatus, remark
      // project: name, clientName, projectType, status, startDate, planEndDate, budget, progress, description
      // customer: name, industry, contactPerson, contactPhone, contactEmail, companyAddress
      // task: name, priority, dueDate, assignee, description, status, progress
      // issue: title, issueType, severity, reporter, description, status
      // experience: title, category, context, conclusion, effectiveness
      // capability: capabilityName, category, currentLevel, targetLevel, selfAssessment, improvementPlan
      // diary: title, date, mood, content, tags, tomorrow
    },
    "confidence": 0.9, // 识别置信度 0-1
    "description": "简要描述这个实体" // 如：这是一个新同事，需要添加到人员管理
  }
]

示例：对于"我有一个同事张三，我们一起做过湖北电力数字化审计项目"，应返回：
[
  {
    "type": "member",
    "data": {"name": "张三", "position": "开发", "workStatus": "在职", "nature": "自有", "remark": "曾参与湖北电力数字化审计项目"},
    "confidence": 0.95,
    "description": "新同事，需要添加到人员管理"
  },
  {
    "type": "project",
    "data": {"name": "湖北电力数字化审计项目", "projectType": "企业服务", "status": "已完成", "clientName": "湖北电力"},
    "confidence": 0.9,
    "description": "已完成的项目，可以添加到项目历史"
  },
  {
    "type": "customer",
    "data": {"name": "湖北电力", "industry": "电力"},
    "confidence": 0.8,
    "description": "潜在客户，可以添加到客户管理"
  }
]

请直接返回JSON数组，不要其他文字。`;

      

    // AI 意图识别 - 执行命令
    const executeAiCommand=async()=>{
      if(!pendingCommand.value) return;

      const cmd=pendingCommand.value;
      const params=cmd.params || {};

      // 将自然语言日期转换为标准格式
      const parseDate=(dateStr)=>{
        if(!dateStr) return '';
        const today=new Date();
        if(dateStr.includes('今天')){
          return today.toISOString().split('T')[0];
        }
        if(dateStr.includes('明天')){
          today.setDate(today.getDate()+1);
          return today.toISOString().split('T')[0];
        }
        if(dateStr.includes('后天')){
          today.setDate(today.getDate()+2);
          return today.toISOString().split('T')[0];
        }
        if(dateStr.includes('下周')){
          today.setDate(today.getDate()+7);
          return today.toISOString().split('T')[0];
        }
        return dateStr;
      };

      try{
        switch(cmd.action){
          case 'task':
            const newTask={
              id:Date.now(),
              name:params.name || params.taskName || '新任务',
              dueDate:parseDate(params.dueDate),
              priority:params.priority || '中',
              assignee:params.assignee || '',
              status:params.status || '待处理',
              progress:0,
              description:params.description || ''
            };
            tasks.value.unshift(newTask);
            localStorage.setItem('pmos_tasks',JSON.stringify(tasks.value));
            showToast('任务创建成功！','success');
            break;

          case 'project':
            const newProject={
              id:Date.now(),
              name:params.name || params.projectName || '新项目',
              clientName:params.clientName || params.customer || '',
              status:params.status || '计划中',
              progress:0,
              startDate:parseDate(params.startDate),
              planEndDate:parseDate(params.dueDate),
              budget:params.budget || 0,
              description:params.description || ''
            };
            projects.value.unshift(newProject);
            localStorage.setItem('pmos_projects',JSON.stringify(projects.value));
            showToast('项目创建成功！','success');
            break;

          case 'customer':
            const newCustomer={
              id:Date.now(),
              name:params.name || params.customerName || '新客户',
              industry:params.industry || '',
              contactPerson:params.contactPerson || '',
              contactPhone:params.contactPhone || '',
              status:params.status || '潜在客户'
            };
            customers.value.unshift(newCustomer);
            localStorage.setItem('pmos_customers',JSON.stringify(customers.value));
            showToast('客户创建成功！','success');
            break;

          case 'meeting':
            const newMeeting={
              id:Date.now(),
              title:params.name || params.meetingTitle || '新会议',
              date:parseDate(params.date || params.dueDate),
              time:params.time || '10:00',
              participants:params.participants || '',
              type:params.type || '项目例会',
              summary:params.summary || '',
              todos:params.todos || ''
            };
            meetings.value.unshift(newMeeting);
            localStorage.setItem('pmos_meetings',JSON.stringify(meetings.value));
            showToast('会议创建成功！','success');
            break;

          case 'diary':
            const newDiary={
              id:Date.now(),
              title:params.title || params.name || '工作日记',
              date:parseDate(params.date) || new Date().toISOString().split('T')[0],
              content:params.content || params.description || '',
              mood:params.mood || '普通',
              tags:params.tags || ''
            };
            diaries.value.unshift(newDiary);
            saveDiaries();
            showToast('日记创建成功！','success');
            break;

          case 'issue':
            const newIssue={
              id:Date.now(),
              title:params.name || params.title || '新问题',
              issueType:params.issueType || 'defect',
              status:params.status || '待处理',
              priority:params.priority || '中',
              assignee:params.assignee || '',
              description:params.description || ''
            };
            issues.value.unshift(newIssue);
            localStorage.setItem('pmos_issues',JSON.stringify(issues.value));
            showToast('问题创建成功！','success');
            break;

          case 'experience':
            const newExperience={
              id:Date.now(),
              title:params.name || params.title || '新经验',
              category:params.category || '项目管理',
              summary:params.summary || params.description || '',
              solution:params.solution || ''
            };
            experiences.value.unshift(newExperience);
            localStorage.setItem('pmos_experiences',JSON.stringify(experiences.value));
            showToast('经验创建成功！','success');
            break;

          case 'member':
            const newMember={
              id:Date.now(),
              name:params.name || params.memberName || '新成员',
              position:params.position || '',
              email:params.email || '',
              phone:params.phone || '',
              workStatus:params.workStatus || '在职',
              nature:params.nature || '自有'
            };
            teamMembers.value.unshift(newMember);
            saveTeamMembers();
            showToast('成员创建成功！','success');
            break;

          default:
            showToast('暂不支持此操作类型','warning');
            return;
        }

        // 添加成功消息到聊天
        chatMessages.value.push({
          role:'assistant',
          content:'✅ **'+(cmd.title || '操作')+'** 已成功执行！\n\n您可以在对应的管理模块中查看和编辑。'
        });

        // 清除待执行命令
        pendingCommand.value=null;

        // 保存会话
        if(currentSessionId.value){
          const session=chatHistory.value.find(s=>s.id===currentSessionId.value);
          if(session){
            session.messages=JSON.parse(JSON.stringify(chatMessages.value));
            saveChatHistory();
          }
        }

      }catch(e){
        showToast('执行失败: '+e.message,'error');
      }
    };

    // AI 意图识别 - 取消命令
    const cancelAiCommand=()=>{
      if(pendingCommand.value){
        chatMessages.value.push({
          role:'assistant',
          content:'好的，已取消操作。如果您有其他需求，请继续告诉我。'
        });
        pendingCommand.value=null;
      }
    };

    // AI Chat about all data
    const sendToAI=async()=>{
      if(!chatInput.value || !chatInput.value.trim()) return;
      if(chatLoading.value || isStreaming.value) return;

      const config=JSON.parse(localStorage.getItem('pmos_ai_config')||'{}');
      if(!config.apiKey){
        showToast('请先在设置页面配置智谱AI API Key','error');
        return;
      }

      const userQuestion=chatInput.value.trim();
      chatMessages.value.push({role:'user',content:userQuestion});

      // Create new session if needed
      if(!currentSessionId.value){
        const newSession={
          id:Date.now(),
          title:userQuestion.substring(0,20),
          messages:[],
          createdAt:new Date().toISOString()
        };
        chatHistory.value.unshift(newSession);
        currentSessionId.value=newSession.id;
        saveChatHistory();
      }

      chatInput.value='';
      chatLoading.value=true;

      // Prepare data context
const projectList=projects.value.map(p=>p.name+' | 客户:'+(p.clientName||'无')+' | 负责人:'+p.status+' | 进度:'+(p.progress||0)+'%').join('\n');
const taskList=tasks.value.map(t=>t.name+' | 优先级:'+(t.priority||'无')+' | 截止期:'+(t.dueDate||'无')+' | 负责人:'+(t.assignee||'无')).join('\n');
const customerList=customers.value.map(c=>c.name+' | 行业:'+(c.industry||'暂无')+' | 联系人:'+(c.contactPerson||'无')).join('\n');
const issueList=issues.value.map(i=>i.title+' | 类型:'+(i.issueType==='risk'?'风险':'缺陷')+' | 状态:'+i.status).join('\n');
const experienceList=experiences.value.map(e=>e.title+' | 分类:'+(e.category||'无')).join('\n');
const capabilityList=capabilities.value.map(c=>c.capabilityName+' | '+c.category).join('\n');
const memberList=teamMembers.value.map(m=>m.name+' | 岗位:'+(m.position||'无')+' | 状态:'+(m.workStatus||'在职')+' | 性质:'+(m.nature||'自有')).join('\n');
const meetingList=meetings.value.map(m=>(m.title||'无标题')+' | 日期:'+(m.date||'无')+' | 参与人:'+(m.participants||'无')).join('\n');
const diaryList=diaries.value.map(d=>d.title+' | 日期:'+(d.date||'无')+' | 标签:'+(d.tags||'无')).join('\n');
const dataContext='项目信息:\n'+projectList+'\n\n任务信息:\n'+taskList+'\n\n客户信息:\n'+customerList+'\n\n问题信息:\n'+issueList+'\n\n经验信息:\n'+experienceList+'\n\n能力配置:\n'+capabilityList+'\n\n人员信息:\n'+memberList+'\n\n会议记录:\n'+meetingList+'\n\n工作日记:\n'+diaryList;

      // 意图识别系统提示词
      const intentSystemPrompt=`你是一个专业的项目管理助手，擅长理解用户意图并提供帮助。

用户可能想要：
1. 查询信息 - 问项目、任务、客户等数据
2. 创建内容 - 创建任务、项目、会议、日记等
3. 更新内容 - 修改任务状态、项目进度等
4. 删除内容 - 删除某个项目或任务
5. 分析总结 - 汇总工作情况、分析趋势
6. 闲聊问答 - 回答关于系统使用的问题

当用户想要创建、更新或删除内容时，请分析用户意图并提取关键参数。

**重要格式要求**：
- 如果是查询、闲聊或分析类问题，直接回答用户问题
- 如果是要创建/更新/删除内容，请按以下JSON格式回复（不要有其他文字）：

【意图识别格式 - 仅用于创建/更新/删除操作】：
\`\`\`json
{
  "intent": "create|update|delete",
  "action": "task|project|customer|meeting|diary|issue|experience|member",
  "params": {
    "name/taskName/projectName": "提取到的名称",
    "dueDate/startDate": "提取到的日期",
    "priority": "提取到的优先级",
    "assignee": "提取到的负责人",
    "description": "提取到的描述",
    ...其他参数
  },
  "summary": "一句话总结要执行的操作"
}
\`\`\`

**示例**：
用户说："创建一个新任务，明天截止，负责人是张三"
你应该回复：
\`\`\`json
{
  "intent": "create",
  "action": "task",
  "params": {
    "taskName": "新任务",
    "dueDate": "明天",
    "assignee": "张三",
    "status": "待处理"
  },
  "summary": "创建任务【新任务】，截止日期明天，负责人张三"
}
\`\`\`

用户说："我有多少个项目？"
直接回答即可。

请开始处理用户请求：`;

      try{
        // ========== 多轮对话上下文管理 ==========
        // 构建多轮对话历史（排除最后一条用户消息，因为会单独发送）
        const conversationHistory=chatMessages.value.slice(0,-1).map(m=>({
          role:m.role,
          content:m.content
        }));

        // 构建消息数组 - 系统提示 + 历史 + 数据上下文 + 当前问题
        const messages=[
          {role:'system',content:intentSystemPrompt}
        ];

        // 如果有历史对话，添加简短的上下文摘要
        if(conversationHistory.length>0){
          // 最近6轮对话作为上下文（节省token）
          const recentHistory=conversationHistory.slice(-12);
          messages.push(...recentHistory);
        }

        // 添加数据上下文和当前问题
        messages.push({
          role:'user',
          content:'【系统数据】\n'+dataContext+'\n\n【当前问题】\n'+userQuestion
        });

        // ========== 流式输出实现 ==========
        // 创建 abort controller 用于取消
        streamingAbortController=new AbortController();

        // 先添加一个空的助手消息用于流式更新
        const assistantMsg={role:'assistant',content:''};
        chatMessages.value.push(assistantMsg);
        const msgIndex=chatMessages.value.length-1;

        isStreaming.value=true;
        streamingContent.value='';

        const response=await fetch('https://open.bigmodel.cn/api/paas/v4/chat/completions',{
          method:'POST',
          headers:{
            'Content-Type':'application/json',
            'Authorization':'Bearer '+config.apiKey
          },
          body:JSON.stringify({
            model:'glm-4-flash',
            messages:messages,
            temperature:0.3,
            stream:true  // 启用流式输出
          }),
          signal:streamingAbortController.signal
        });

        // 处理流式响应
        const reader=response.body.getReader();
        const decoder=new TextDecoder();
        let fullContent='';
        let buffer='';

        while(true){
          const {done,value}=await reader.read();
          if(done) break;

          buffer+=decoder.decode(value,{stream:true});
          const lines=buffer.split('\n');
          buffer=lines.pop()||'';

          for(const line of lines){
            if(line.startsWith('data: ')){
              const data=line.slice(6);
              if(data==='[DONE]') continue;

              try{
                const json=JSON.parse(data);
                const content=json.choices?.[0]?.delta?.content||'';
                if(content){
                  fullContent+=content;
                  streamingContent.value=fullContent;
                  chatMessages.value[msgIndex].content=fullContent;
                }
              }catch(e){
                // 忽略解析错误
              }
            }
          }
        }

        // 处理剩余buffer
        if(buffer.startsWith('data: ')&&buffer.slice(6)!=='[DONE]'){
          try{
            const json=JSON.parse(buffer.slice(6));
            const content=json.choices?.[0]?.delta?.content||'';
            if(content){
              fullContent+=content;
              chatMessages.value[msgIndex].content=fullContent;
            }
          }catch(e){}
        }

        isStreaming.value=false;
        streamingContent.value='';
        chatLoading.value=false;

        // ========== 意图识别处理 ==========
        const aiResponse=fullContent.trim();

        // 尝试解析意图识别结果
        const intentMatch=aiResponse.match(/```json\s*([\s\S]*?)\s*```/);
        if(intentMatch){
          try{
            const intentResult=JSON.parse(intentMatch[1]);

            // 如果识别到创建/更新/删除意图，显示命令预览
            if(intentResult.intent && ['create','update','delete'].includes(intentResult.intent)){
              const iconMap={
                task: '📋', project: '📁', customer: '👤', meeting: '📅',
                diary: '📓', issue: '⚠️', experience: '💡', member: '👥'
              };
              pendingCommand.value={
                type: intentResult.intent,
                action: intentResult.action,
                params: intentResult.params || {},
                title: intentResult.summary || '待执行操作',
                icon: iconMap[intentResult.action] || '⚡'
              };
              // 更新助手消息
              chatMessages.value[msgIndex]={
                role:'assistant',
                content:'我已经理解您的意图，正在准备执行...\n\n📝 **'+(intentResult.summary || '操作')+'**\n\n请确认以下信息是否正确，然后点击「确认执行」。'
              };
            }
          }catch(e){
            console.log('意图解析失败',e);
          }
        }

        // 保存会话
        if(currentSessionId.value){
          const session=chatHistory.value.find(s=>s.id===currentSessionId.value);
          if(session){
            session.messages=JSON.parse(JSON.stringify(chatMessages.value));
            saveChatHistory();
          }
        }

      }catch(e){
        isStreaming.value=false;
        chatLoading.value=false;
        if(e.name==='AbortError'){
          chatMessages.value.push({role:'assistant',content:'已停止生成'});
        }else{
          chatMessages.value.push({role:'assistant',content:'网络错误: '+e.message});
        }
      }
    };

    // 停止流式输出
    const stopStreaming=()=>{
      if(streamingAbortController){
        streamingAbortController.abort();
        isStreaming.value=false;
        chatLoading.value=false;
      }
    };

      try{
        const response=await fetch('https://open.bigmodel.cn/api/paas/v4/chat/completions',{
          method:'POST',
          headers:{
            'Content-Type':'application/json',
            'Authorization':'Bearer '+config.apiKey
          },
          body:JSON.stringify({
            model:'glm-4-flash',
            messages:[
              {role:'system',content:intentSystemPrompt},
              {role:'user',content:'上下文数据:\n'+dataContext+'\n\n用户问题: '+userQuestion}
            ],
            temperature:0.3
          })
        });

        const data=await response.json();
        chatLoading.value=false;

        if(data.choices&&data.choices[0]&&data.choices[0].message){
          const aiResponse=data.choices[0].message.content.trim();

          // 尝试解析意图识别结果
          const intentMatch=aiResponse.match(/```json\s*([\s\S]*?)\s*```/);
          if(intentMatch){
            try{
              const intentResult=JSON.parse(intentMatch[1]);

              // 如果识别到创建/更新/删除意图，显示命令预览
              if(intentResult.intent && ['create','update','delete'].includes(intentResult.intent)){
                const iconMap={
                  task: '📋', project: '📁', customer: '👤', meeting: '📅',
                  diary: '📓', issue: '⚠️', experience: '💡', member: '👥'
                };
                pendingCommand.value={
                  type: intentResult.intent,
                  action: intentResult.action,
                  params: intentResult.params || {},
                  title: intentResult.summary || '待执行操作',
                  icon: iconMap[intentResult.action] || '⚡'
                };
                // 添加助手消息说明
                chatMessages.value.push({
                  role:'assistant',
                  content:'我已经理解您的意图，正在准备执行...\n\n📝 **'+(intentResult.summary || '操作')+'**\n\n请确认以下信息是否正确，然后点击「确认执行」。'
                });
                return; // 不添加普通回复
              }
            }catch(e){
              // JSON解析失败，当作普通回答处理
              console.log('意图解析失败',e);
            }
          }

          // 普通回答
          chatMessages.value.push({role:'assistant',content:aiResponse});
        }else{
          chatMessages.value.push({role:'assistant',content:'AI生成失败: '+(data.error?.message||'未知错误')});
        }

        // Save session messages
        if(currentSessionId.value){
          const session=chatHistory.value.find(s=>s.id===currentSessionId.value);
          if(session){
            session.messages=JSON.parse(JSON.stringify(chatMessages.value));
            saveChatHistory();
          }
        }
      }catch(e){
        chatLoading.value=false;
        chatMessages.value.push({role:'assistant',content:'网络错误: '+e.message});
      }
    };

    // Chat Voice Recognition
    const initChatVoice=()=>{
      if('webkitSpeechRecognition' in window || 'SpeechRecognition' in window){
        const SpeechRecognition=window.SpeechRecognition||window.webkitSpeechRecognition;
        chatRecognition=new SpeechRecognition();
        chatRecognition.continuous=true;
        chatRecognition.interimResults=true;
        chatRecognition.lang='zh-CN';
        
        chatRecognition.onstart=()=>{
          chatVoiceRecording.value=true;
          chatVoiceStatus.value='正在录音，请说话...';
          chatFinalTranscript='';
        };
        
        chatRecognition.onresult=(event)=>{
          let interim='';
          for(let i=event.resultIndex;i<event.results.length;i++){
            const transcript=event.results[i][0].transcript;
            if(event.results[i].isFinal){
              chatFinalTranscript+=transcript;
            }else{
              interim+=transcript;
            }
          }
          chatInput.value=chatFinalTranscript+interim;
          chatVoiceStatus.value='正在处理...';
        };
        
        chatRecognition.onend=()=>{
          chatVoiceRecording.value=false;
          if(chatFinalTranscript.trim()){
            chatVoiceStatus.value='正在识别中';
            // 初始化失败
            setTimeout(()=>{
              if(chatInput.value.trim()){
                sendToAI();
              }
            },300);
          }else{
            chatVoiceStatus.value='未检测到语音';
          }
        };
        
        chatRecognition.onerror=(event)=>{
          chatVoiceRecording.value=false;
          chatVoiceStatus.value='录音状态: '+event.error;
        };
      }
    };

    const toggleChatVoice=()=>{
      if(!chatRecognition){
        initChatVoice();
      }
      if(!chatRecognition){
        showToast('请先登录并配置智谱AI API Key','error');
        return;
      }
      if(chatVoiceRecording.value){
        chatRecognition.stop();
      }else{
        chatInput.value='';
        chatFinalTranscript='';
        chatRecognition.start();
      }
    };

    const getTypeName=(type)=>{
      const names={task:'任务',project:'项目',customer:'客户',issue:'问题',experience:'经验',capability:'能力',member:'人员',diary:'日记'};
      return names[type]||type;
    };

    const getFieldName=(key)=>{
      const names={
        name:'名称',title:'标题',priority:'优先级',dueDate:'截止期',assignee:'负责人',
        description:'描述',clientName:'客户名称',projectType:'项目类型',startDate:'开始期',
        planEndDate:'计划结束期',status:'状态',budget:'预算',industry:'行业',
        contactPerson:'联系人',contactPhone:'联系电话',issueType:'问题类型',
        category:'分类',summary:'摘要',solution:'解决方案',capabilityName:'能力名称',
        currentLevel:'当前等级',targetLevel:'目标等级',selfAssessment:'自我评估',improvementPlan:'改进计划'
      };
      return names[key]||key;
    };

    // 切换实体选择状态
    const toggleEntitySelection=(index)=>{
      const idx=selectedEntities.value.indexOf(index);
      if(idx===-1){
        selectedEntities.value.push(index);
      }else{
        selectedEntities.value.splice(idx,1);
      }
    };

    // 当AI结果更新时，初始化选中所有实体
    watch(aiResult,(newVal)=>{
      if(newVal&&newVal.multi){
        selectedEntities.value=newVal.entities.map((_,index)=>index);
      }else{
        selectedEntities.value=[];
      }
    });

    // 保存单个实体
    const saveSingleEntity=(entity)=>{
      const{type,data}=entity;
      
      const saveMap={
        task:()=>{const list=[...tasks.value];list.unshift({...data,id:Date.now(),progress:0,status:'待处理'});tasks.value=list;localStorage.setItem('pmos_tasks',JSON.stringify(list));},
        project:()=>{const list=[...projects.value];list.unshift({...data,id:Date.now(),progress:0});projects.value=list;localStorage.setItem('pmos_projects',JSON.stringify(list));},
        customer:()=>{const list=[...customers.value];list.unshift({...data,id:Date.now()});customers.value=list;localStorage.setItem('pmos_customers',JSON.stringify(list));},
        issue:()=>{const list=[...issues.value];list.unshift({...data,id:Date.now(),status:'open'});issues.value=list;localStorage.setItem('pmos_issues',JSON.stringify(list));},
        experience:()=>{const list=[...experiences.value];list.unshift({...data,id:Date.now()});experiences.value=list;localStorage.setItem('pmos_experiences',JSON.stringify(list));},
        capability:()=>{const list=[...capabilities.value];list.unshift({...data,id:Date.now()});capabilities.value=list;localStorage.setItem('pmos_capabilities',JSON.stringify(list));},
        member:()=>{const list=[...teamMembers.value];list.unshift({...data,id:Date.now()});teamMembers.value=list;saveTeamMembers();},
        diary:()=>{const list=[...diaries.value];list.unshift({...data,id:Date.now(),createdAt:new Date().toISOString()});diaries.value=list;saveDiaries();},
      };
      
      if(saveMap[type]){
        saveMap[type]();
        return true;
      }
      return false;
    };

    // 保存选中的多个实体
    const saveSelectedEntities=(selectedIndices)=>{
      if(!aiResult.value||!aiResult.value.multi)return;
      
      savingToTable.value=true;
      const entities=aiResult.value.entities;
      let savedCount=0;
      
      // 如果没有传入参数，使用当前选中的实体
      const indicesToSave=selectedIndices||selectedEntities.value;
      
      indicesToSave.forEach(index=>{
        if(index>=0&&index<entities.length){
          if(saveSingleEntity(entities[index])){
            savedCount++;
          }
        }
      });
      
      if(savedCount>0){
        showToast(`成功保存${savedCount}个实体`,'success');
      }
      
      // 重置AI结果
      aiResult.value=null;
      voiceText.value='';
      voiceStatus.value='正在聆听，请说话...';
      savingToTable.value=false;
    };

    // 保存单个实体（兼容旧版本）
    const saveAiResult=()=>{
      if(!aiResult.value)return;
      
      // 处理多实体情况
      if(aiResult.value.multi){
        // 默认保存所有实体
        const indices=aiResult.value.entities.map((_,index)=>index);
        saveSelectedEntities(indices);
        return;
      }
      
      // 处理单实体情况（兼容旧版本）
      savingToTable.value=true;
      const{type,data}=aiResult.value.entity;
      
      if(saveSingleEntity({type,data})){
        showToast(getTypeName(type)+'已保存','success');
      }
      
      // 重置AI结果
      aiResult.value=null;
      voiceText.value='';
      voiceStatus.value='正在聆听，请说话...';
      savingToTable.value=false;
    };

    const cancelAiResult=()=>{
      aiResult.value=null;
      voiceStatus.value='正在聆听，请说话...';
    };

    // File Upload with Parse Option
    const pendingFile=ref(null);
    const showFileModeModal=ref(false);
    const fileModeLoading=ref(false);
    
    const uploadFile=async(event)=>{
      const file=event.target.files[0];
      if(!file)return;
      
      // Store file for later processing
      pendingFile.value={file,id:Date.now()};
      showFileModeModal.value=true;
      event.target.value='';
    };
    
    const handleFileMode=(mode)=>{
      if(!pendingFile.value)return;
      showFileModeModal.value=false;
      
      if(mode==='source'){
        // Source file storage
        const file=pendingFile.value.file;
        const reader=new FileReader();
        reader.onload=(e)=>{
          const fileData={
            id:pendingFile.value.id,
            name:file.name,
            size:file.size,
            type:file.type,
            data:e.target.result,
            uploadTime:new Date().toISOString(),
            mode:'source'
          };
          const list=[...files.value];
          list.unshift(fileData);
          localStorage.setItem('pmos_files',JSON.stringify(list));
          loadFiles();
          showToast('文件上传成功','success');        };
        reader.readAsDataURL(file);
      }else{
        // AI parse and save to table
        const file=pendingFile.value.file;
        const config=JSON.parse(localStorage.getItem('pmos_ai_config')||'{}');
        if(!config.apiKey){
          showToast('请先在设置页面配置智谱AI API Key','error');
          return;
        }
        
        fileModeLoading.value=true;
        const reader=new FileReader();
        reader.onload=async(e)=>{
          try{
            const ext=file.name.split('.').pop().toLowerCase();
            let content=e.target.result;
            if(ext==='txt'||ext==='md'){
              content=await new Promise(res=>{
                const r=new FileReader();
                r.onload=ev=>res(ev.target.result);
                r.readAsText(file);
              });
            }
            
            const filePromptContent = content.substring(0, 5000);
            const prompt='请分析以下文件内容，提取结构化数据。\n\n文件名: '+file.name+'\n文件类型: '+(file.type||ext)+'\n\n文件内容:\n'+filePromptContent+'\n\n请将文件内容智能分类并提取为JSON格式，可选类型：\n1. task - 任务：包含名称、优先级、截止期、负责人等字段\n2. project - 项目：包含名称、客户、负责人、状态、进度等字段\n3. customer - 客户：包含公司名称、行业、联系人、联系电话等字段\n4. issue - 问题：包含标题、类型（risk/bug）、状态等字段\n5. experience - 经验：包含标题、分类、内容、解决方案等字段\n6. meeting - 会议：包含标题、时间、参与者、会议纪要等字段\n\n请返回JSON格式：\n{\n  "type": "task/project/customer/issue/experience/meeting",\n  "data": { // 根据type选择对应字段}\n}\n\n请确保返回的JSON格式正确可解析';

            const response=await fetch('https://open.bigmodel.cn/api/paas/v4/chat/completions',{
              method:'POST',
              headers:{'Content-Type':'application/json','Authorization':'Bearer '+config.apiKey},
              body:JSON.stringify({model:'glm-4-flash',messages:[{role:'user',content:dataContext+'\n\n'+userPrompt}],temperature:0.1})
            });
            
            const data=await response.json();
            fileModeLoading.value=false;
            
            if(data.choices&&data.choices[0]&&data.choices[0].message){
              const content2=data.choices[0].message.content;
              const jsonMatch=content2.match(/\{[\s\S]*\}/);
              if(jsonMatch){
                const result=JSON.parse(jsonMatch[0]);
                const saveMap={
                  task:()=>{const list=[...tasks.value];list.unshift({...result.data,id:Date.now(),progress:0,status:'待处理'});localStorage.setItem('pmos_tasks',JSON.stringify(list));loadTasks();},
                  project:()=>{const list=[...projects.value];list.unshift({...result.data,id:Date.now(),progress:0});localStorage.setItem('pmos_projects',JSON.stringify(list));loadProjects();},
                  customer:()=>{const list=[...customers.value];list.unshift({...result.data,id:Date.now()});localStorage.setItem('pmos_customers',JSON.stringify(list));loadCustomers();},
                  issue:()=>{const list=[...issues.value];list.unshift({...result.data,id:Date.now(),status:'open'});localStorage.setItem('pmos_issues',JSON.stringify(list));loadIssues();},
                  experience:()=>{const list=[...experiences.value];list.unshift({...result.data,id:Date.now()});localStorage.setItem('pmos_experiences',JSON.stringify(list));loadExperiences();},
                  meeting:()=>{const list=[...meetings.value];list.unshift({...result.data,id:Date.now()});localStorage.setItem('pmos_meetings',JSON.stringify(list));loadMeetings();},
                  member:()=>{const list=[...teamMembers.value];list.unshift({...result.data,id:Date.now()});saveTeamMembers();loadTeamMembers();},
                };
                if(saveMap[result.type]){
                  saveMap[result.type]();
                  showToast('文件解析并保存成功','success');                  pendingFile.value=null;
                  return;
                }
              }
            }
            showToast('保存失败','error');
          }catch(err){
            fileModeLoading.value=false;
            showToast('录音状态: '+err.message,'error');
          }
          pendingFile.value=null;
        };
        reader.readAsDataURL(file);
      }
    };
    
    const downloadFile=(file)=>{
      const a=document.createElement('a');
      a.href=file.data;
      a.download=file.name;
      a.click();
    };
    
    const deleteFile=(id)=>{
      if(!confirm('确定要删除这个文件吗'))return;
      const list=files.value.filter(f=>f.id!==id);
      localStorage.setItem('pmos_files',JSON.stringify(list));
      loadFiles();
      showToast('文件删除成功','success');    };
    
    const formatFileSize=(bytes)=>{
      if(bytes<1024)return bytes+' B';
      if(bytes<1024*1024)return (bytes/1024).toFixed(1)+' KB';
      return (bytes/1024/1024).toFixed(1)+' MB';
    };

    // Meeting functions
    const saveMeeting=(data,id)=>{
      if(id){
        const list=meetings.value.map(m=>m.id===id?{...m,...data}:m);
        localStorage.setItem('pmos_meetings',JSON.stringify(list));
      }else{
        const list=[...meetings.value];
        list.unshift({...data,id:Date.now()});
        localStorage.setItem('pmos_meetings',JSON.stringify(list));
      }
      loadMeetings();
    };
    
    const editMeeting=(m)=>{
      modalType.value='meeting';
      editingId.value=m.id;
      Object.assign(formData,JSON.parse(JSON.stringify(m)));
      modalTitle.value='编辑会议';
      showModal.value=true;
    };
    
    const deleteMeeting=(id)=>{
      if(!confirm('确定要删除此会议吗？'))return;
      const list=meetings.value.filter(m=>m.id!==id);
      localStorage.setItem('pmos_meetings',JSON.stringify(list));
      loadMeetings();
      showToast('操作成功','success');
    };

    // Demo Data
    const generateDemoData=()=>{
      const demoProjects=[
        {id:Date.now(),name:'企业数字化转型项目',clientName:'科技集团',projectType:'软件开发',startDate:'2024-01-15',planEndDate:'2024-12-31',status:'进行中',budget:5000000,progress:65,description:'企业数字化转型项目整体规划'},
        {id:Date.now()+1,name:'ERP系统升级项目',clientName:'工业制造集团',projectType:'企业服务',startDate:'2024-03-01',planEndDate:'2024-09-30',status:'进行中',budget:2000000,progress:40,description:'企业资源计划系统升级改造'},
      ];
      const demoTasks=[
        {id:Date.now()+10,name:'企业数字化转型项目',priority:'紧急',dueDate:'2024-04-15',assignee:'张三',progress:80,status:'进行中',description:'项目即将进入测试阶段'},
        {id:Date.now()+11,name:'客户需求变更评审会议',priority:'高',dueDate:'2024-04-20',assignee:'李四',progress:50,status:'进行中',description:'需要安排项目启动会议'}
      ];
      const demoCustomers=[
{id:Date.now()+20,name:'科技集团',industry:'科技行业',contactPerson:'王经理',contactPhone:'138****1234'},
        {id:Date.now()+21,name:'工业制造集团',industry:'制造业',contactPerson:'张经理',contactPhone:'139****5678'},
      ];
      const demoIssues=[
{id:Date.now()+30,title:'系统登录异常问题',issueType:'issue',status:'open',description:'系统登录异常问题需要修复'},
{id:Date.now()+31,title:'预算超支风险',issueType:'risk',status:'待处理',description:'当前预算超支风险10%'},
      ];
      const demoExperiences=[
{id:Date.now()+40,title:'敏捷开发实践经验分享',category:'项目管理',effectiveness:'优秀',summary:'采用敏捷开发方法提高团队效率',solution:'1.采用每站会追踪进度\n2.使用看板管理任务流程'}
      ];
      
      localStorage.setItem('pmos_projects',JSON.stringify(demoProjects));
      localStorage.setItem('pmos_tasks',JSON.stringify(demoTasks));
      localStorage.setItem('pmos_customers',JSON.stringify(demoCustomers));
      localStorage.setItem('pmos_issues',JSON.stringify(demoIssues));
      localStorage.setItem('pmos_experiences',JSON.stringify(demoExperiences));
      localStorage.setItem('pmos_capabilities',JSON.stringify([]));
      
      loadAll();
      showToast('操作成功','success');
    };

    const clearAllData=()=>{
      if(!confirm('确定要清除所有数据吗？此操作不可恢复！'))return;
      ['pmos_projects','pmos_tasks','pmos_customers','pmos_issues','pmos_experiences','pmos_capabilities','pmos_team_members','pmos_user'].forEach(k=>localStorage.removeItem(k));
      loadAll();
      showToast('数据已清除','success');    };

    // Methods
    const handleLogin=()=>{
      if(loginForm.username==='admin'&&loginForm.password==='admin123'){
        user.value={id:1,username:'admin',nickname:'系统管理员',yearsOfExperience:8,certifications:'PMP,ACP'};
        isLoggedIn.value=true;
        currentPage.value='dashboard';
        loadAll();
        initVoiceRecognition();
        
        // Load AI config
        const config=JSON.parse(localStorage.getItem('pmos_ai_config')||'{}');
        aiConfig.apiKey=config.apiKey||'';
        
        // Auto generate demo data if empty
        if(projects.value.length===0){
          generateDemoData();
        }
        showToast('操作成功','success');
      }else{
        showToast('用户名或密码错误','error');
      }
    };

    const handleLogout=()=>{
      isLoggedIn.value=false;
      user.value={};
      showToast('已退出登录','info');    };

    const startNewChat=()=>{
      // Save current session before starting new one
      if(currentSessionId.value && chatMessages.value.length>0){
        const session=chatHistory.value.find(s=>s.id===currentSessionId.value);
        if(session){
          session.messages=JSON.parse(JSON.stringify(chatMessages.value));
          saveChatHistory();
        }
      }
      currentSessionId.value=null;
      chatMessages.value=[];
      chatInput.value='';
    };
    
    const switchSession=(sessionId)=>{
      currentSessionId.value=sessionId;
      const session=chatHistory.value.find(s=>s.id===sessionId);
      if(session){
        chatMessages.value=JSON.parse(JSON.stringify(session.messages||[]));
        chatInput.value='';
      }
    };
    
    const deleteSession=(sessionId)=>{
      chatHistory.value=chatHistory.value.filter(s=>s.id!==sessionId);
      saveChatHistory();
      if(currentSessionId.value===sessionId){
        startNewChat();
      }
    };
    
    const saveChatHistory=()=>{
      localStorage.setItem('chatHistory',JSON.stringify(chatHistory.value));
    };
    
    const loadAll=()=>{
      loadProjects();loadCustomers();loadTasks();loadIssues();loadExperiences();loadCapabilities();loadDiaries();loadFiles();loadMeetings();loadTeamMembers();
    };

    const loadProjects=()=>{try{const data=localStorage.getItem('pmos_projects');projects.value=data?JSON.parse(data):[];}catch(e){projects.value=[];}};
    const loadCustomers=()=>{try{const data=localStorage.getItem('pmos_customers');customers.value=data?JSON.parse(data):[];}catch(e){customers.value=[];}};
    const loadTasks=()=>{try{const data=localStorage.getItem('pmos_tasks');tasks.value=data?JSON.parse(data):[];}catch(e){tasks.value=[];}};
    const loadIssues=()=>{try{const data=localStorage.getItem('pmos_issues');issues.value=data?JSON.parse(data):[];}catch(e){issues.value=[];}};
    const loadExperiences=()=>{try{const data=localStorage.getItem('pmos_experiences');experiences.value=data?JSON.parse(data):[];}catch(e){experiences.value=[];}};
    const loadCapabilities=()=>{try{const data=localStorage.getItem('pmos_capabilities');capabilities.value=data?JSON.parse(data):[];}catch(e){capabilities.value=[];}};
    const loadDiaries=()=>{try{const data=localStorage.getItem('pmos_diaries');diaries.value=data?JSON.parse(data):[];}catch(e){diaries.value=[];}};
    const saveDiaries=()=>{localStorage.setItem('pmos_diaries',JSON.stringify(diaries.value));};
    const loadFiles=()=>{try{const data=localStorage.getItem('pmos_files');files.value=data?JSON.parse(data):[];}catch(e){files.value=[];}};
    const loadMeetings=()=>{try{const data=localStorage.getItem('pmos_meetings');meetings.value=data?JSON.parse(data):[];}catch(e){meetings.value=[];}};
    const loadTeamMembers=()=>{try{const data=localStorage.getItem('pmos_team_members');teamMembers.value=data?JSON.parse(data):[];}catch(e){teamMembers.value=[];}};
    const saveTeamMembers=()=>{localStorage.setItem('pmos_team_members',JSON.stringify(teamMembers.value));};
    
    const saveDiary=()=>{
      const data=[...diaries.value];
      if(editingId.value){const i=data.findIndex(d=>d.id===editingId.value);if(i>-1)data[i]={...data[i],...formData,updatedAt:new Date().toISOString()};}
      else{data.unshift({...formData,id:Date.now(),createdAt:new Date().toISOString()});}
      saveDiaries();loadDiaries();closeModal();showToast('操作成功','success');
    };
    
    const editDiary=(d)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(d)));
      editingId.value=d.id;
      modalType.value='diary';
      modalTitle.value='编辑日记';
      showModal.value=true;
    };

    const formatMoney=(n)=>n?parseFloat(n).toLocaleString():'0';
    const truncate=(str,len)=>str?str.slice(0,len):'';
    const getStatusBadge=(s)=>({'待处理':'badge-gray','进行中':'badge-info','暂停中':'badge-warning','已完成':'badge-success'}[s]||'badge-gray');
    const getPriorityBadge=(p)=>({'紧急':'badge-danger','高':'badge-danger','中':'badge-warning','低':'badge-gray'}[p]||'badge-gray');

    const openModal=(type)=>{
      modalType.value=type;
      editingId.value=null;
      
      // 根据类型重置formData的特定字段
      const resetMap={
        project:()=>{Object.assign(formData,{name:'',clientName:'',projectType:'',status:'',startDate:'',planEndDate:'',budget:'',progress:0,description:''});},
        task:()=>{Object.assign(formData,{name:'',priority:'',dueDate:'',assignee:'',description:'',status:'待处理',progress:0});},
        customer:()=>{Object.assign(formData,{name:'',industry:'',contactPerson:'',contactPhone:'',contactEmail:'',companyAddress:''});},
        issue:()=>{Object.assign(formData,{title:'',issueType:'',severity:'',reporter:'',description:'',status:'open'});},
        experience:()=>{Object.assign(formData,{title:'',category:'',context:'',conclusion:'',effectiveness:''});},
        capability:()=>{Object.assign(formData,{capabilityName:'',category:'',currentLevel:'',targetLevel:'',selfAssessment:'',improvementPlan:''});},
        diary:()=>{Object.assign(formData,{title:'',date:'',mood:'',content:'',tags:'',tomorrow:''});},
        meeting:()=>{Object.assign(formData,{title:'',date:'',time:'',type:'',location:'',participants:'',summary:'',actionItems:''});},
        member:()=>{Object.assign(formData,{name:'',gender:'',phone:'',email:'',position:'',nature:'',joinYear:'',department:'',dailyRate:'',costType:'',workStatus:'',remark:'',projectHistory:[]});}
      };
      
      if(resetMap[type]){
        resetMap[type]();
      }
      
      memberProjectHistoryStr.value='[]';
      const titles={project:'新建项目',task:'新建任务',customer:'新建客户',issue:'新建问题',experience:'新建经验',capability:'新建能力',meeting:'新建会议',diary:'新建日记'};
      modalTitle.value=titles[type]||'编辑';
      showModal.value=true;
    };

    const closeModal=()=>{showModal.value=false;};

    const saveProject=()=>{
      const data=[...projects.value];
      if(editingId.value){const i=data.findIndex(p=>p.id===editingId.value);if(i>-1)data[i]={...data[i],...formData};}
      else{data.unshift({...formData,id:Date.now(),progress:0});}
      localStorage.setItem('pmos_projects',JSON.stringify(data));
      loadProjects();closeModal();showToast('操作成功','success');
    };

    const editProject=(p)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(p)));
      editingId.value=p.id;
      modalType.value='project';
      modalTitle.value='编辑项目';
      showModal.value=true;
    };

    const saveTask=()=>{
      const data=[...tasks.value];
      if(editingId.value){const i=data.findIndex(t=>t.id===editingId.value);if(i>-1)data[i]={...data[i],...formData};}
      else{data.unshift({...formData,id:Date.now(),progress:0,status:'待处理'});}
      localStorage.setItem('pmos_tasks',JSON.stringify(data));
      loadTasks();closeModal();showToast('操作成功','success');
    };

    const editTask=(t)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(t)));
      editingId.value=t.id;
      modalType.value='task';
      modalTitle.value='编辑任务';
      showModal.value=true;
    };

    const saveCustomer=()=>{
      const data=[...customers.value];
      if(editingId.value){const i=data.findIndex(c=>c.id===editingId.value);if(i>-1)data[i]={...data[i],...formData};}
      else{data.unshift({...formData,id:Date.now()});}
      localStorage.setItem('pmos_customers',JSON.stringify(data));
      loadCustomers();closeModal();showToast('操作成功','success');
    };

    const viewCustomer=(c)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(c)));
      editingId.value=c.id;
      modalType.value='customer';
      modalTitle.value='客户详情';
      showModal.value=true;
    };

    // View functions
    const viewProject=(p)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(p)));
      editingId.value=p.id;
      modalType.value='project';
      modalTitle.value='编辑项目';
      showModal.value=true;
    };

    const viewTask=(t)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(t)));
      editingId.value=t.id;
      modalType.value='task';
      modalTitle.value='编辑任务';
      showModal.value=true;
    };

    const viewIssue=(i)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(i)));
      editingId.value=i.id;
      modalType.value='issue';
      modalTitle.value='问题详情';
      showModal.value=true;
    };

    const viewExperience=(e)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(e)));
      editingId.value=e.id;
      modalType.value='experience';
      modalTitle.value='知识详情';
      showModal.value=true;
    };

    const viewCapability=(c)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(c)));
      editingId.value=c.id;
      modalType.value='capability';
      modalTitle.value='编辑能力条目';
      showModal.value=true;
    };

    const viewMeeting=(m)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(m)));
      editingId.value=m.id;
      modalType.value='meeting';
      modalTitle.value='会议纪要详情';
      showModal.value=true;
    };

    const viewFile=(f)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(f)));
      editingId.value=f.id;
      modalType.value='file';
      modalTitle.value='上传文件';
      showModal.value=true;
    };

    const editCustomer=(c)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(c)));
      editingId.value=c.id;
      modalType.value='customer';
      modalTitle.value='编辑客户';
      showModal.value=true;
    };

    const saveIssue=()=>{
      const data=[...issues.value];
      if(editingId.value){const i=data.findIndex(x=>x.id===editingId.value);if(i>-1)data[i]={...data[i],...formData};}
      else{data.unshift({...formData,id:Date.now(),status:'open'});}
      localStorage.setItem('pmos_issues',JSON.stringify(data));
      loadIssues();closeModal();showToast('操作成功','success');
    };

    const editIssue=(i)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(i)));
      editingId.value=i.id;
      modalType.value='issue';
      modalTitle.value='编辑问题';
      showModal.value=true;
    };

    const saveExperience=()=>{
      const data=[...experiences.value];
      if(editingId.value){const i=data.findIndex(e=>e.id===editingId.value);if(i>-1)data[i]={...data[i],...formData};}
      else{data.unshift({...formData,id:Date.now()});}
      localStorage.setItem('pmos_experiences',JSON.stringify(data));
      loadExperiences();closeModal();showToast('操作成功','success');
    };

    const editExperience=(e)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(e)));
      editingId.value=e.id;
      modalType.value='experience';
      modalTitle.value='编辑经验';
      showModal.value=true;
    };

    const saveCapability=()=>{
      const data=[...capabilities.value];
      if(editingId.value){const i=data.findIndex(c=>c.id===editingId.value);if(i>-1)data[i]={...data[i],...formData};}
      else{data.unshift({...formData,id:Date.now()});}
      localStorage.setItem('pmos_capabilities',JSON.stringify(data));
      loadCapabilities();closeModal();showToast('操作成功','success');
    };

    const editCapability=(c)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(c)));
      editingId.value=c.id;
      modalType.value='capability';
      modalTitle.value='编辑能力条目';
      showModal.value=true;
    };

    const editMember=(m)=>{
      Object.assign(formData,JSON.parse(JSON.stringify(m)));
      memberProjectHistoryStr.value=m.projectHistory?JSON.stringify(m.projectHistory,null,2):'[]';
      editingId.value=m.id;
      modalType.value='member';
      modalTitle.value='编辑人员';
      showModal.value=true;
    };

    const addMember=()=>{
      // 清空所有数据
      editingId.value=null;
      modalType.value='member';
      modalTitle.value='添加人员';
      // 使用Object.assign正确设置reactive对象的属性
      Object.assign(formData,{
        name: '',
        gender: '',
        phone: '',
        email: '',
        position: '',
        nature: '',
        joinYear: '',
        department: '',
        dailyRate: '',
        costType: '',
        workStatus: '',
        remark: ''
      });
      memberProjectHistoryStr.value = '[]';
      showModal.value = true;
    };

    const submitMemberForm=()=>{
      try{
        if(memberProjectHistoryStr.value){
          formData.projectHistory=JSON.parse(memberProjectHistoryStr.value);
        }else{
          formData.projectHistory=[];
        }
      }catch(e){
        showToast('项目履历JSON格式错误，请检查','error');
        return;
      }
      const data=[...teamMembers.value];
      if(editingId.value){
        const i=data.findIndex(m=>m.id===editingId.value);
        if(i>-1)data[i]={...data[i],...formData,updatedAt:new Date().toISOString()};
      }else{
        data.unshift({...formData,id:Date.now(),createdAt:new Date().toISOString()});
      }
      saveTeamMembers();
      loadTeamMembers();
      closeModal();
      showToast('操作成功','success');
    };

    const submitMeetingForm=()=>{
      const data=[...meetings.value];
      if(editingId.value){const i=data.findIndex(m=>m.id===editingId.value);if(i>-1)data[i]={...data[i],...formData,updatedAt:new Date().toISOString()};}
      else{data.unshift({...formData,id:Date.now(),createdAt:new Date().toISOString()});}
      localStorage.setItem('pmos_meetings',JSON.stringify(data));
      loadMeetings();closeModal();showToast('操作成功','success');
    };

    const deleteItem=(type,id)=>{
      if(!confirm('确定要删除此项吗？'))return;
      const keyMap={project:'pmos_projects',customer:'pmos_customers',task:'pmos_tasks',issue:'pmos_issues',experience:'pmos_experiences',capability:'pmos_capabilities',diary:'pmos_diaries',member:'pmos_team_members'};
      const data=JSON.parse(localStorage.getItem(keyMap[type])||'[]');
      localStorage.setItem(keyMap[type],JSON.stringify(data.filter(x=>x.id!==id)));
      const loaders={project:loadProjects,customer:loadCustomers,task:loadTasks,issue:loadIssues,experience:loadExperiences,capability:loadCapabilities,diary:loadDiaries,member:loadTeamMembers};
      loaders[type]();
      showToast('操作成功','success');
    };

    const showToast=(message,type='info')=>{
      toast.message=message;toast.type=type;toast.show=true;
      setTimeout(()=>toast.show=false,2500);
    };

    // 页面加载时初始化
    onMounted(()=>{
      console.log('PM-OS 系统初始化完成');
      
      // 运行页面诊断
      const diagnostic = window.testVoicePage && window.testVoicePage();
      console.log('页面诊断结果:', diagnostic ? '正常' : '有异常');
      
      // 显示友好的状态信息
      voiceStatus.value = '正在检查语音功能...';
      
      // 延迟初始化语音识别，确保页面已完全加载
      setTimeout(() => {
        try {
          console.log('开始初始化语音识别...');
          
          // 安全检查：确保页面元素存在
          const voicePanel = document.querySelector('.voice-panel');
          if (!voicePanel) {
            console.warn('语音输入面板未找到，但系统会继续工作');
          }
          
          const config = JSON.parse(localStorage.getItem('pmos_ai_config') || '{}');
          console.log('AI配置状态:', config.apiKey ? '已配置' : '未配置');
          
          if (config.apiKey) {
            // 使用更安全的初始化方式
            setTimeout(() => {
              try {
                const success = initVoiceRecognition();
                if (success) {
                  console.log('✅ 语音识别初始化成功');
                  voiceStatus.value = '语音识别已就绪，请点击麦克风按钮开始';
                  showToast('语音功能已就绪', 'success');
                } else {
                  console.log('⚠️ 语音识别初始化失败');
                  voiceStatus.value = '语音识别不可用，请使用文本输入';
                  showToast('语音识别不可用，请使用文本输入', 'warning');
                }
              } catch (error) {
                console.error('语音识别初始化异常:', error);
                voiceStatus.value = '语音识别初始化异常，请使用文本输入';
                showToast('语音识别初始化异常: ' + error.message, 'error');
              }
            }, 1000);
          } else {
            voiceStatus.value = '请先配置智谱AI API Key，或使用文本输入';
            console.log('未配置API Key，跳过语音识别初始化');
          }
        } catch (error) {
          console.error('页面初始化错误:', error);
          voiceStatus.value = '页面初始化异常，但文本输入仍然可用';
          
          // 显示友好错误提示
          showToast('页面初始化遇到问题，但核心功能正常', 'warning');
        }
      }, 1000);
    });

    return {
      isLoggedIn,user,currentPage,projects,customers,tasks,issues,experiences,capabilities,diaries,teamMembers,files,meetings,pendingFile,showFileModeModal,fileModeLoading,
      stats,activeProjects,filteredProjects,filteredTasks,filteredMeetings,filteredDiaries,filteredTeamMembers,searchKeyword,searchTaskKeyword,statusFilter,positionFilter,
      showModal,modalType,modalTitle,formData,toast,loginForm,aiConfig,
      voiceRecording,voiceStatus,voiceText,aiResult,savingToTable,
      chatInput,chatMessages,chatHistory,currentSessionId,chatLoading,chatVoiceRecording,chatVoiceStatus,startNewChat,switchSession,deleteSession,toggleChatVoice,pendingCommand,executeAiCommand,cancelAiCommand,isStreaming,streamingContent,stopStreaming,
      handleLogin,handleLogout,saveAiConfig,
      toggleVoice,analyzeWithAI,getTypeName,getFieldName,saveAiResult,cancelAiResult,sendToAI,
      generateDemoData,clearAllData,
      loadAll,openModal,closeModal,saveProject,editProject,saveTask,editTask,saveCustomer,editCustomer,
      saveIssue,editIssue,saveExperience,editExperience,saveCapability,editCapability,
      saveDiary,editDiary,saveMeeting,editMeeting,deleteMeeting,submitMeetingForm,
      viewProject,viewTask,viewIssue,viewExperience,viewCapability,viewMeeting,viewCustomer,viewFile,
      uploadFile,downloadFile,deleteFile,formatFileSize,handleFileMode,
      deleteItem,formatMoney,truncate,getStatusBadge,getPriorityBadge,
      memberProjectHistoryStr,editMember,addMember,submitMemberForm,
    }
  }
});
app.mount('#app');
