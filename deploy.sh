#!/bin/bash
# PM-OS 部署脚本

echo "📦 准备部署 PM-OS 项目..."
echo ""

# 检查必要文件
echo "🔍 检查项目文件..."
if [ ! -f "index.html" ]; then
    echo "❌ 错误：index.html 文件不存在"
    exit 1
fi

if [ ! -f "lucide.min.js" ]; then
    echo "⚠️ 警告：lucide.min.js 不存在，图标功能可能受影响"
fi

echo "✅ 项目文件检查完成"
echo ""

# 显示部署选项
echo "🌐 部署选项："
echo "1. Vercel (推荐) - https://vercel.com"
echo "2. Netlify - https://netlify.com"
echo "3. GitHub Pages - https://pages.github.com"
echo "4. 本地测试"
echo ""

read -p "请选择部署方式 (1-4): " choice

case $choice in
    1)
        echo "🚀 选择 Vercel 部署"
        echo ""
        echo "步骤："
        echo "1. 访问 https://vercel.com"
        echo "2. 使用 GitHub 账号登录"
        echo "3. 点击 'New Project'"
        echo "4. 导入你的仓库"
        echo "5. 自动部署完成"
        echo ""
        echo "✅ 配置已准备：vercel.json"
        ;;
    2)
        echo "🚀 选择 Netlify 部署"
        echo ""
        echo "步骤："
        echo "1. 访问 https://netlify.com"
        echo "2. 拖拽此文件夹到页面"
        echo "3. 自动部署完成"
        echo ""
        echo "✅ 配置已准备：netlify.toml"
        ;;
    3)
        echo "🚀 选择 GitHub Pages 部署"
        echo ""
        echo "步骤："
        echo "1. 上传到 GitHub 仓库"
        echo "2. 进入仓库 Settings → Pages"
        echo "3. 选择 Source: 'Deploy from a branch'"
        echo "4. 选择 Branch: 'main'，Folder: '/'"
        echo "5. 保存，等待部署完成"
        ;;
    4)
        echo "🚀 本地测试"
        echo ""
        echo "启动本地服务器..."
        
        # 检测 Python 版本
        if command -v python3 &> /dev/null; then
            echo "使用 Python3 启动服务器..."
            python3 -m http.server 8000 &
        elif command -v python &> /dev/null; then
            echo "使用 Python 启动服务器..."
            python -m http.server 8000 &
        else
            echo "❌ Python 未安装，无法启动服务器"
            echo "请安装 Python 或使用其他 HTTP 服务器"
        fi
        
        echo "✅ 服务器启动在 http://localhost:8000"
        echo "按 Ctrl+C 停止服务器"
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "📋 部署前确认："
echo "1. 确保所有文件已提交到 Git"
echo "2. 确认 API 密钥已正确配置（如果需要）"
echo "3. 测试本地功能正常"
echo ""
echo "🎉 部署准备完成！"