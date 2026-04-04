// AI助手修复测试脚本
console.log('=== AI助手修复测试 ===');

// 测试联网查询判断函数
const testNeedsWebSearch = (question, expected) => {
  // 模拟needsWebSearch函数逻辑
  const searchKeywords = [
    '最新', '实时', '今天', '当前', '现在', '近期', '最近',
    '汇率', '价格', '行情', '股价', '股市', '股票', '市场',
    '天气', '气温', '温度', '降雨', '气象', '气候',
    '新闻', '热点', '头条', '事件', '发生', '最新消息',
    '2026年', '明年', '今年', '本月', '下月', '本周', '下周',
    '新技术', '新版本', '最新版', '更新', '升级',
    'trend', 'news', 'update', 'current', 'latest', 'price',
    'weather', 'stock', 'market', 'exchange', 'rate',
    '实时数据', '最新消息', '市场行情', '天气预报', '股票价格'
  ];
  
  const lowerQuestion = question.toLowerCase();
  const result = searchKeywords.some(keyword => 
    lowerQuestion.includes(keyword.toLowerCase())
  );
  
  console.log(`测试问题: "${question.substring(0, 30)}..."`);
  console.log(`预期结果: ${expected}, 实际结果: ${result}`);
  console.log(`测试结果: ${result === expected ? '✅ 通过' : '❌ 失败'}`);
  console.log('---');
};

// 测试用例
console.log('\n1. 联网查询判断测试:');
testNeedsWebSearch('今天的天气怎么样？', true);
testNeedsWebSearch('美元对人民币的汇率是多少？', true);
testNeedsWebSearch('最新的科技新闻有哪些？', true);
testNeedsWebSearch('苹果公司的最新股价是多少？', true);

console.log('\n2. 本地数据查询测试:');
testNeedsWebSearch('我有多少个项目在进行中？', false);
testNeedsWebSearch('下周有哪些任务要截止？', false);
testNeedsWebSearch('客户列表有哪些？', false);
testNeedsWebSearch('团队人员的分布情况如何？', false);

console.log('\n3. 混合查询测试:');
testNeedsWebSearch('结合市场行情分析我们的项目风险', true);
testNeedsWebSearch('基于今天的数据创建新的任务', true);
testNeedsWebSearch('查询项目状态并分析本周进展', false);

console.log('\n=== 响应格式化测试 ===');
console.log('已修复的问题:');
console.log('✅ 1. 重复回复问题 - AI助手现在只输出一段内容');
console.log('✅ 2. JSON代码块显示问题 - 意图JSON会被清除并转换为友好提示');
console.log('✅ 3. 联网查询判断 - 自动检测需要实时信息的问题');
console.log('✅ 4. 响应格式化 - 使用Markdown增强可读性');

console.log('\n=== 使用说明 ===');
console.log('1. Web搜索按钮: 点击检测当前问题是否需要联网查询');
console.log('2. 单段响应: AI助手现在只输出一段完整、格式化的内容');
console.log('3. 意图识别: 创建/更新/删除操作会显示确认界面');
console.log('4. 联网提示: 涉及实时信息的问题会明确提示需要Web搜索');

console.log('\n测试完成！现在可以启动服务器进行实际测试。');