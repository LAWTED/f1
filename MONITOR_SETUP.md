# Singapore GP Ticket Monitor Setup Guide

## 🎯 监控条件

这个系统会监控以下票务并通过 GitHub Issues 通知你：

1. **周日的 grandstand 票** (高优先级)
2. **三日票价格 ≤ $1500** (高优先级)
3. **周五 premier walkabout 票** (中优先级)
4. **grandstand 票价格 ≤ $300** (中优先级)

## 📱 GitHub 通知设置（推荐）

### 🆓 完全免费的通知方式
- **GitHub Issues**: 自动创建 Issue 记录发现的票务
- **手机推送**: 通过 GitHub 手机 App 接收即时通知
- **无需配置**: 不需要设置任何 secrets 或密码

### 📲 启用手机通知
1. 下载 GitHub 手机 App (iOS/Android)
2. 登录你的 GitHub 账户
3. 在 App 设置中启用 Issues 通知
4. 当发现目标票务时，会自动推送到手机

## 🔧 邮件通知配置（可选）

如果你想额外接收邮件提醒，可以配置以下设置：

### 启用邮件功能
1. 在 GitHub 仓库中设置变量: Settings → Secrets and variables → Actions → Variables
2. 创建变量 `ENABLE_EMAIL` 并设置值为 `true`

### 邮件 Secrets（仅在启用邮件时需要）

1. **EMAIL_USERNAME**: 发送邮件的Gmail账户
   ```
   example@gmail.com
   ```

2. **EMAIL_PASSWORD**: Gmail应用密码 (不是普通密码)
   - 去 Google Account → Security → App passwords
   - 生成一个应用密码用于邮件发送
   ```
   abcd efgh ijkl mnop
   ```

3. **EMAIL_TO**: 接收提醒的邮箱地址
   ```
   your-email@example.com
   ```

## 📋 快速设置步骤

### 1. 上传到 GitHub
```bash
cd /path/to/your/repo
git init
git add .
git commit -m "Add Singapore GP ticket monitor"
git remote add origin https://github.com/yourusername/singapore-gp-monitor.git
git push -u origin main
```

### 2. 启用 GitHub Actions
1. 进入仓库的 Actions 页面
2. 如果需要，启用 GitHub Actions
3. 监控会自动每10分钟运行一次

### 3. 设置手机通知（推荐）
1. 下载并登录 GitHub 手机 App
2. 进入 App 设置 → Notifications
3. 确保 "Issues" 通知已开启
4. 完成！当发现目标票务时会自动推送到手机

### 4. 可选：启用邮件通知
仅在你需要邮件通知时：
1. 在仓库 Settings → Secrets and variables → Actions → Variables
2. 创建变量 `ENABLE_EMAIL` = `true`
3. 配置上述邮件相关的 secrets

## 🚀 手动测试

你可以手动触发监控来测试：

### 本地测试
```bash
python monitor_tickets.py
```

### GitHub Actions 手动触发
1. 进入 Actions 页面
2. 选择 "Singapore GP Ticket Monitor" workflow
3. 点击 "Run workflow"

## 📱 通知示例

### GitHub Issue 通知
当发现目标票务时，会自动创建这样的 Issue：

```
Title: 🎫 Ticket Alert: 2 target tickets found!

🎫 Singapore GP Ticket Alert!

Found the following target tickets:

1. Chicane @ Turn 2 Grandstand[SUN]
   Price: $288
   Category: Grandstands
   Days: sunday
   Reason: Sunday Grandstand available
   Priority: HIGH
   Status: AVAILABLE

2. Premier Walkabout[FRI]
   Price: $188
   Category: Walkabouts
   Days: friday
   Reason: Friday Premier Walkabout available
   Priority: MEDIUM
   Status: AVAILABLE

## 🚀 Quick Actions
- [🎫 Buy Tickets](https://singaporegp.sg/en/tickets/general-tickets/grandstands/)
- [📊 View Run Details](https://github.com/user/repo/actions/runs/123)
- [⚙️ Monitor Settings](https://github.com/user/repo/blob/main/MONITOR_SETUP.md)

## 📱 Mobile Notification
If you have the GitHub mobile app installed, you should receive a push notification for this issue.
```

### 手机推送通知
在 GitHub App 中会显示：
```
🎫 Ticket Alert: 2 target tickets found!
singapore-gp-monitor • Issues
```

## 🔄 监控频率

- **自动运行**: 每10分钟检查一次
- **运行时间**: 24/7 持续监控
- **超时设置**: 每次运行最多5分钟

## 📊 监控功能

### ✅ 功能特性
- 自动票务检查
- 邮件即时通知
- GitHub Issues 记录
- 运行日志保存
- 手动触发选项

### 🛡️ 安全特性
- 使用 GitHub Secrets 保护敏感信息
- 应用密码而非主密码
- 超时保护防止无限运行

## 🚨 故障排除

### 邮件发送失败
1. 检查 Gmail 应用密码是否正确
2. 确认已启用两步验证
3. 验证邮箱地址格式

### 监控不运行
1. 检查 GitHub Actions 是否启用
2. 查看 Actions 日志排查错误
3. 确认 cron 表达式语法

### 无法访问网站
1. 检查网络连接
2. 查看是否有反爬虫限制
3. 检查 User-Agent 和请求头

## 📈 自定义监控条件

如需修改监控条件，编辑 `monitor_tickets.py` 中的 `check_target_tickets()` 函数：

```python
def check_target_tickets(tickets):
    target_tickets = []
    
    for ticket in tickets:
        # 添加你的自定义条件
        if your_condition:
            target_tickets.append({
                'ticket': ticket,
                'reason': 'Your custom reason',
                'priority': 'HIGH/MEDIUM/LOW'
            })
    
    return target_tickets
```

## 📝 日志和调试

- **GitHub Actions 日志**: 在 Actions 页面查看每次运行的详细日志
- **Issue 跟踪**: 发现票务时自动创建 GitHub Issue
- **Artifacts**: 保存警报消息作为下载文件

祝你成功抢到心仪的票务！🏎️