// 修复版PM-OS系统测试服务器
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = 9999;
const WEB_DIR = __dirname;

// 创建HTTP服务器
const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url);
    let filePath = path.join(WEB_DIR, parsedUrl.pathname === '/' ? 'index.html' : parsedUrl.pathname);
    
    // 确保文件路径安全
    if (!filePath.startsWith(WEB_DIR)) {
        res.writeHead(403, { 'Content-Type': 'text/plain' });
        res.end('Forbidden');
        return;
    }
    
    // 默认文件
    if (filePath.endsWith('/')) {
        filePath = path.join(filePath, 'index.html');
    }
    
    // 检查文件是否存在
    fs.stat(filePath, (err, stats) => {
        if (err || !stats.isFile()) {
            // 返回404页面或重定向到index.html
            if (parsedUrl.pathname === '/') {
                res.writeHead(404, { 'Content-Type': 'text/plain' });
                res.end('File not found: ' + filePath);
            } else {
                // 对于API请求，返回404
                res.writeHead(404, { 'Content-Type': 'text/plain' });
                res.end('Not Found');
            }
            return;
        }
        
        // 根据文件扩展名设置Content-Type
        const ext = path.extname(filePath).toLowerCase();
        const mimeTypes = {
            '.html': 'text/html; charset=utf-8',
            '.js': 'application/javascript',
            '.css': 'text/css',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon'
        };
        
        const contentType = mimeTypes[ext] || 'text/plain';
        
        // 读取并发送文件
        fs.readFile(filePath, (err, content) => {
            if (err) {
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end('Internal Server Error');
                return;
            }
            
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content);
        });
    });
});

// 启动服务器
server.listen(PORT, 'localhost', () => {
    console.log('='.repeat(60));
    console.log('🎯 修复版PM-OS系统测试服务器');
    console.log('='.repeat(60));
    console.log(`📂 服务目录: ${WEB_DIR}`);
    console.log(`🌐 访问地址: http://localhost:${PORT}`);
    console.log(`\n📋 测试文件列表:`);
    console.log(`  1. 完整系统: http://localhost:${PORT}/`);
    console.log(`  2. 语音功能测试: http://localhost:${PORT}/test_voice_fixed.html`);
    console.log(`  3. 极简语音测试: http://localhost:${PORT}/../voice_simple.html`);
    console.log(`\n🔧 修复说明:`);
    console.log(`  ✅ 修复了语音识别初始化逻辑`);
    console.log(`  ✅ 简化了toggleVoice函数`);
    console.log(`  ✅ 移除了复杂的错误处理`);
    console.log(`  ✅ 确保变量在正确的作用域`);
    console.log(`\n🧪 测试步骤:`);
    console.log(`  1. 访问完整系统: http://localhost:${PORT}/`);
    console.log(`  2. 使用 admin / admin123 登录`);
    console.log(`  3. 点击左侧菜单的"语音输入"`);
    console.log(`  4. 测试麦克风按钮`);
    console.log(`  5. 测试文本输入框`);
    console.log(`\n📝 注意事项:`);
    console.log(`  • 语音功能需要浏览器支持Web Speech API`);
    console.log(`  • 首次使用需要允许麦克风权限`);
    console.log(`  • 如果语音不可用，文本输入仍然正常工作`);
    console.log('='.repeat(60));
    
    // 检查关键文件是否存在
    const checkFiles = [
        { path: 'index.html', desc: '完整PM-OS系统' },
        { path: 'test_voice_fixed.html', desc: '语音功能测试页面' },
        { path: '../voice_simple.html', desc: '极简语音测试' }
    ];
    
    console.log('\n🔍 文件检查:');
    checkFiles.forEach(file => {
        const fullPath = path.join(WEB_DIR, file.path);
        if (fs.existsSync(fullPath)) {
            const stats = fs.statSync(fullPath);
            console.log(`  ✅ ${file.desc}: ${(stats.size / 1024).toFixed(1)} KB`);
        } else {
            console.log(`  ❌ ${file.desc}: 文件不存在`);
        }
    });
});

// 处理关闭信号
process.on('SIGINT', () => {
    console.log('\n\n👋 服务器正在关闭...');
    server.close(() => {
        console.log('✅ 服务器已关闭');
        process.exit(0);
    });
});

console.log('\n按 Ctrl+C 停止服务器\n');