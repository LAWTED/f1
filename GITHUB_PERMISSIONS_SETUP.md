# GitHub Actions 权限配置

## 🔧 修复权限问题

### 问题描述
```
RequestError [HttpError]: Resource not accessible by integration
status: 403
```

### 解决方案

#### 1. Workflow 文件已更新
已在 `.github/workflows/ticket-monitor-simple.yml` 中添加必要权限：

```yaml
permissions:
  contents: read
  issues: write
```

#### 2. 仓库设置检查

确保你的 GitHub 仓库设置正确：

1. **进入仓库设置**：
   - 打开 https://github.com/LAWTED/f1
   - 点击 "Settings" 标签

2. **检查 Actions 权限**：
   - 左侧菜单选择 "Actions" → "General"
   - 确保选择 "Allow all actions and reusable workflows"

3. **检查 Workflow 权限**：
   - 在 "Actions" → "General" 页面下滚到 "Workflow permissions"
   - 选择 "Read and write permissions"
   - 勾选 "Allow GitHub Actions to create and approve pull requests"

#### 3. 具体设置步骤

**Step 1: Actions 权限**
```
Settings → Actions → General → Actions permissions
选择：Allow all actions and reusable workflows
```

**Step 2: Workflow 权限**
```
Settings → Actions → General → Workflow permissions
选择：Read and write permissions
勾选：Allow GitHub Actions to create and approve pull requests
```

**Step 3: Issues 功能**
```
Settings → Features
确保：Issues 功能已启用
```

### 验证设置

设置完成后，重新运行 GitHub Actions workflow：

1. 进入 Actions 页面
2. 选择 "Singapore GP Ticket Monitor (Simple)"
3. 点击 "Run workflow"
4. 等待运行完成

### 预期结果

设置正确后，workflow 应该能够：
- ✅ 成功创建 GitHub Issue
- ✅ 发送移动端推送通知
- ✅ 每 10 分钟自动监控

## 🎯 权限说明

### 需要的权限

| 权限 | 用途 |
|------|------|
| `contents: read` | 读取代码和文件 |
| `issues: write` | 创建和更新 Issues |

### 可选权限

| 权限 | 用途 |
|------|------|
| `actions: read` | 读取 Actions 运行信息 |
| `metadata: read` | 读取仓库元数据 |

## 📱 通知设置

### GitHub 移动端通知

1. **下载 GitHub 移动应用**
2. **登录你的账户**
3. **启用推送通知**：
   - 设置 → 通知 → 推送通知
   - 确保 "Issues" 通知已启用

### 通知流程

1. **监控检测到目标票务**
2. **GitHub Actions 创建 Issue**
3. **GitHub 发送推送通知到手机**
4. **点击通知直接跳转到 Issue**
5. **点击链接购买票务**

## 🚀 完成状态

- ✅ 多行字符串问题已解决
- ✅ Workflow 权限已配置
- ✅ 监控脚本正常运行
- ✅ 票务检测功能正常

只需要在 GitHub 仓库中配置权限，整个系统就可以正常工作了！