# Raycast Scripts Setup Guide

## 🚀 快速开始

现在你可以在 Raycast 中快速检查新加坡GP票务！

## 📜 可用脚本

### 1. Singapore GP Tickets (`f1.sh`)
**功能**: 显示所有可用票务，按日期分组
**图标**: 🏎️
**命令**: 在 Raycast 中输入 "Singapore GP Tickets" 或 "f1"

**显示内容**:
- 3天票、周五、周六、周日的所有可用票务
- 价格和票务类别
- 购买链接

### 2. F1 Monitor Check (`f1-monitor.sh`)  
**功能**: 检查你关心的特定票务
**图标**: 🎯
**命令**: 在 Raycast 中输入 "F1 Monitor Check"

**监控条件**:
- 🔥 周日的 grandstand 票 (高优先级)
- 🔥 三日票价格 ≤ $1500 (高优先级)
- 🟡 周五 premier walkabout 票 (中优先级)
- 🟡 grandstand 票价格 ≤ $300 (中优先级)

## 🛠️ 安装步骤

### 1. 复制脚本到 Raycast
```bash
# 方法1: 直接拖拽
# 将 f1.sh 和 f1-monitor.sh 拖拽到 Raycast 窗口

# 方法2: 使用 Raycast 导入
# 在 Raycast 中: Settings → Extensions → Script Commands → Add Script Directory
# 选择 /Users/lawtedwu/Documents/f1/
```

### 2. 验证安装
1. 打开 Raycast (⌘ + Space)
2. 输入 "Singapore GP" 或 "f1"
3. 应该看到两个脚本选项

### 3. 首次运行
- 脚本会自动设置 Python 虚拟环境
- 安装必要的依赖包 (requests, beautifulsoup4)
- 只需要等待几秒钟完成设置

## 🎯 使用场景

### 日常快速检查
```
⌘ + Space → 输入 "f1" → 回车
```
立即查看所有可用票务，适合每天快速浏览

### 目标票务监控
```
⌘ + Space → 输入 "monitor" → 回车  
```
专门检查你感兴趣的票务类型，如果有发现会显示详细信息

## 📱 输出示例

### 正常检查输出
```
🏎️  Singapore GP Ticket Checker
==================================
🔍 Checking available tickets...

=== Friday Available Tickets ===
Premier Walkabout[FRI]            $188    AVAILABLE [Walkabouts]
Zone 4 Walkabout[FRI]             $148    AVAILABLE [Walkabouts]

=== Saturday Available Tickets ===
Republic Grandstand[SAT]          $438    AVAILABLE [Grandstands]
Padang Grandstand[SAT]            $328    AVAILABLE [Grandstands]

Summary Across All Days:
Friday: 3 available
Saturday: 5 available
Total available tickets: 11

🔗 Buy tickets: https://singaporegp.sg/...
```

### 监控模式输出
```
🎯 Singapore GP Target Ticket Monitor
======================================
🔍 Monitoring for:
   🔥 Sunday grandstand tickets
   🔥 3-day tickets ≤ $1500
   🟡 Friday premier walkabout
   🟡 Grandstand tickets ≤ $300

🎯 Found 1 target tickets!

Premier Walkabout[FRI]
   Price: $188
   Reason: Friday Premier Walkabout available
   Priority: MEDIUM
   Status: AVAILABLE
```

## ⚡ 性能优化

- **快速启动**: 虚拟环境预建，无需等待
- **智能缓存**: 依赖包一次安装，永久使用
- **错误处理**: 网络问题时显示友好提示

## 🔧 自定义设置

### 修改脚本路径
如果你的项目在不同位置，编辑脚本中的：
```bash
SCRIPT_DIR="/Users/lawtedwu/Documents/f1"
```

### 修改监控条件
编辑 `monitor_tickets.py` 中的 `check_target_tickets()` 函数

### 更改显示格式
修改 `check_tickets.py` 中的输出格式

## 🚨 故障排除

### 脚本不显示在 Raycast 中
1. 检查文件权限: `chmod +x f1.sh f1-monitor.sh`
2. 验证脚本路径是否正确
3. 重启 Raycast

### Python 错误
1. 确认 Python 3 已安装
2. 检查虚拟环境是否创建成功
3. 手动运行测试: `bash f1.sh`

### 网络连接问题
1. 检查网络连接
2. 尝试手动访问新加坡GP官网
3. 确认防火墙设置

## 💡 使用技巧

1. **设置别名**: 在 Raycast 中为脚本设置短别名，如 "f1", "gp"
2. **固定到收藏**: 将常用脚本固定到 Raycast 收藏夹
3. **结合快捷键**: 为脚本设置专门的快捷键
4. **配合通知**: 开启 Raycast 通知，及时了解票务状态

现在你可以随时随地快速检查新加坡GP票务了！🏎️✨