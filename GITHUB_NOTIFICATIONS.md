# GitHub 通知设置详细指南

## 📱 GitHub 手机 App 设置

### 1. 下载 GitHub App
- **iOS**: App Store 搜索 "GitHub"
- **Android**: Google Play 搜索 "GitHub"

### 2. 登录并配置通知
1. 打开 GitHub App
2. 登录你的 GitHub 账户
3. 点击右下角的 "Profile" 头像
4. 选择 "Settings" 
5. 选择 "Notifications"

### 3. 启用 Issues 通知
在通知设置中确保以下选项已开启：
- ✅ **Issues** - 当创建新 Issue 时通知
- ✅ **Issue comments** - 当 Issue 有新评论时通知  
- ✅ **Push notifications** - 启用推送通知
- ✅ **Participating** - 当你被分配或提及时通知

### 4. 仓库级别通知
1. 在 GitHub App 中进入你的监控仓库
2. 点击右上角的 "..." 菜单
3. 选择 "Notifications" 
4. 设置为 "Watching" 或 "All Activity"

## 🔔 通知效果

### 即时推送
当监控发现目标票务时：
1. **手机锁屏通知**: 显示票务提醒
2. **App 内通知**: 在 GitHub App 通知页面显示
3. **邮件通知**: (如果启用) 发送到邮箱

### 通知内容
```
🎫 Ticket Alert: 1 target tickets found!
singapore-gp-monitor • Issues • now

Premier Walkabout[FRI] - $188 available
Tap to view details and purchase
```

## 💻 桌面端通知

### GitHub.com 网页通知
1. 登录 GitHub.com
2. 点击右上角铃铛图标查看通知
3. 当有新 Issue 时会显示红点提醒

### 浏览器推送通知
1. 在 GitHub.com 允许浏览器通知
2. Settings → Notifications → Web notifications
3. 启用相关通知类型

## 🎯 智能过滤

### Issue 标签系统
监控创建的 Issue 会自动添加标签：
- `ticket-alert` - 票务提醒
- `automated` - 自动生成
- `high-priority` - 高优先级

### 自动分配
- Issue 会自动分配给仓库所有者
- 确保你能第一时间收到通知

## ⚙️ 高级设置

### 通知频率控制
如果同样的票务持续可用，系统会：
1. 更新现有 Issue 而不是创建新的
2. 在现有 Issue 中添加评论
3. 避免通知疲劳

### 关闭提醒
当你不再需要某个票务的提醒时：
1. 进入对应的 Issue
2. 点击 "Close issue"
3. 系统会在下次发现新票务时创建新 Issue

## 🔧 故障排除

### 没有收到推送通知？
1. 检查手机系统通知权限
2. 确认 GitHub App 通知权限已开启
3. 检查仓库通知设置是否为 "Watching"
4. 确认账户邮箱验证状态

### 通知太频繁？
1. 调整监控频率 (修改 cron 表达式)
2. 关闭不需要的 Issue
3. 修改监控条件，只关注最重要的票务

### 只想要特定类型通知？
1. 在仓库设置中自定义通知类型
2. 使用 GitHub 的通知过滤功能
3. 设置邮件规则自动分类

## 📊 监控状态查看

### 在 GitHub App 中查看
1. 进入仓库页面
2. 选择 "Actions" 选项卡
3. 查看最新的监控运行状态

### 监控历史
1. 所有提醒都保存在 Issues 中
2. 可以查看历史票务变化
3. 分析票务释放规律

这样设置后，你就能通过手机第一时间收到票务提醒，无需复杂的邮件配置！🎯