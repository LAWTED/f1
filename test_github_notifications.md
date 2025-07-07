# GitHub Issues 通知测试

## 🧪 本地测试 Issue 创建逻辑

虽然我们无法在本地直接创建 GitHub Issues，但可以测试监控逻辑：

### 1. 测试监控脚本
```bash
# 测试基本监控功能
python test_monitor.py

# 直接运行监控（会生成 alert_message.txt）
python monitor_tickets.py
```

### 2. 检查输出文件
```bash
# 查看生成的警报消息
cat alert_message.txt
```

### 3. 验证 GitHub Action 配置
```bash
# 检查 workflow 文件语法
cat .github/workflows/ticket-monitor.yml
```

## 🚀 实际测试步骤

### 方法1: 手动触发 GitHub Action
1. 将代码推送到 GitHub 仓库
2. 进入 Actions 页面
3. 选择 "Singapore GP Ticket Monitor" workflow
4. 点击 "Run workflow" 手动触发
5. 查看运行日志和创建的 Issues

### 方法2: 等待自动运行
1. 推送代码后等待最多10分钟
2. GitHub Action 会自动运行
3. 如果发现目标票务，会自动创建 Issue

## 📱 预期结果

### 如果发现目标票务：
1. **GitHub Issue**: 自动创建新 Issue
2. **手机通知**: GitHub App 推送通知
3. **Issue 内容**: 包含票务详情和购买链接
4. **标签**: ticket-alert, automated, high-priority

### 如果没有发现目标票务：
1. **Action 日志**: 显示 "No target tickets found"
2. **无 Issue**: 不会创建新 Issue
3. **下次检查**: 10分钟后自动再次检查

## 🔍 当前监控状态

根据最新测试，系统当前会检测到：
- **Premier Walkabout[FRI] - $188** (符合"周五 premier walkabout"条件)

这意味着一旦部署到 GitHub，会立即创建一个 Issue 通知！

## 📋 Issue 内容预览

期望创建的 Issue 内容：
```
Title: 🎫 Ticket Alert: 1 target tickets found!

🎫 Singapore GP Ticket Alert!

Found the following target tickets:

1. Premier Walkabout[FRI]
   Price: $188
   Category: Walkabouts
   Days: friday
   Reason: Friday Premier Walkabout available
   Priority: MEDIUM
   Status: AVAILABLE

## 🚀 Quick Actions
- [🎫 Buy Tickets](https://singaporegp.sg/en/tickets/general-tickets/grandstands/)
- [📊 View Run Details](GitHub Action运行链接)
- [⚙️ Monitor Settings](仓库设置链接)

## 📱 Mobile Notification
If you have the GitHub mobile app installed, you should receive a push notification for this issue.
```

## ✅ 验证清单

部署前检查：
- [ ] `.github/workflows/ticket-monitor.yml` 文件存在
- [ ] `monitor_tickets.py` 能正常运行
- [ ] GitHub 仓库 Actions 已启用
- [ ] GitHub 手机 App 已安装并登录
- [ ] 手机通知权限已开启

部署后验证：
- [ ] GitHub Action 成功运行
- [ ] 发现目标票务时创建了 Issue
- [ ] 手机收到推送通知
- [ ] Issue 包含正确的票务信息和链接