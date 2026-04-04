@echo off
chcp 65001 > nul
echo 📦 准备部署 PM-OS 项目...
echo.

echo 🔍 检查项目文件...
if not exist "index.html" (
    echo ❌ 错误：index.html 文件不存在
    pause
    exit /b 1
)

if not exist "lucide.min.js" (
    echo ⚠️ 警告：lucide.min.js 不存在，图标功能可能受影响
)

echo ✅ 项目文件检查完成
echo.

echo 🌐 部署选项：
echo 1. Vercel ^(推荐^) - https://vercel.com
echo 2. Netlify - https://netlify.com
echo 3. GitHub Pages - https://pages.github.com
echo 4. 本地测试
echo.

set /p choice="请选择部署方式 (1-4): "

if "%choice%"=="1" (
    echo 🚀 选择 Vercel 部署
    echo.
    echo 步骤：
    echo 1. 访问 https://vercel.com
    echo 2. 使用 GitHub 账号登录
    echo 3. 点击 'New Project'
    echo 4. 导入你的仓库
    echo 5. 自动部署完成
    echo.
    echo ✅ 配置已准备：vercel.json
) else if "%choice%"=="2" (
    echo 🚀 选择 Netlify 部署
    echo.
    echo 步骤：
    echo 1. 访问 https://netlify.com
    echo 2. 拖拽此文件夹到页面
    echo 3. 自动部署完成
    echo.
    echo ✅ 配置已准备：netlify.toml
) else if "%choice%"=="3" (
    echo 🚀 选择 GitHub Pages 部署
    echo.
    echo 步骤：
    echo 1. 上传到 GitHub 仓库
    echo 2. 进入仓库 Settings → Pages
    echo 3. 选择 Source: 'Deploy from a branch'
    echo 4. 选择 Branch: 'main'，Folder: '/'
    echo 5. 保存，等待部署完成
) else if "%choice%"=="4" (
    echo 🚀 本地测试
    echo.
    echo 启动本地服务器...
    
    rem 检测是否安装了 Python
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        echo 使用 Python 启动服务器...
        start python -m http.server 8000
        echo ✅ 服务器启动在 http://localhost:8000
    ) else (
        echo ❌ Python 未安装，无法启动服务器
        echo 请安装 Python 或使用其他 HTTP 服务器
    )
    
    echo 在浏览器中访问 http://localhost:8000
) else (
    echo ❌ 无效选择
    pause
    exit /b 1
)

echo.
echo 📋 部署前确认：
echo 1. 确保所有文件已提交到 Git
echo 2. 确认 API 密钥已正确配置（如果需要）
echo 3. 测试本地功能正常
echo.
echo 🎉 部署准备完成！
pause