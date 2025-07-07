# GitHub Actions Workflow 对比

## 两种 Issue 创建方式的对比

### 方式一：使用 `actions/github-script` (当前方式)
**文件**: `.github/workflows/ticket-monitor.yml`

**优点**:
- ✅ 完全控制 Issue 创建逻辑
- ✅ 可以检查并更新现有的 open issues
- ✅ 可以动态决定是否创建新 Issue 或更新现有 Issue
- ✅ 可以自定义复杂的 Issue 标题和内容逻辑
- ✅ 错误处理更灵活

**缺点**:
- ❌ 代码较长，嵌入在 workflow 文件中
- ❌ 需要处理多行字符串的复杂性
- ❌ 维护成本较高

### 方式二：使用 `JasonEtco/create-an-issue` (简化方式)
**文件**: `.github/workflows/ticket-monitor-simple.yml`

**优点**:
- ✅ 代码简洁，易于维护
- ✅ 使用模板文件，结构清晰
- ✅ 内置支持检查重复 Issue (`search_existing: open`)
- ✅ 内置支持更新现有 Issue (`update_existing: true`)
- ✅ 自动处理多行字符串

**缺点**:
- ❌ 功能相对固定，自定义空间有限
- ❌ 依赖第三方 Action
- ❌ 模板变量功能有限

## 关键功能对比

| 功能 | github-script | create-an-issue |
|------|---------------|-----------------|
| 创建 Issue | ✅ | ✅ |
| 更新现有 Issue | ✅ | ✅ |
| 检查重复 Issue | ✅ | ✅ |
| 自定义逻辑 | ✅ 完全控制 | ❌ 有限 |
| 模板分离 | ❌ | ✅ |
| 维护成本 | ❌ 高 | ✅ 低 |
| 多行字符串处理 | ❌ 复杂 | ✅ 简单 |

## 推荐方案

### 当前建议: 使用 `JasonEtco/create-an-issue`

**原因**:
1. **简洁性**: 代码量减少约 70%
2. **可维护性**: 模板文件独立，易于修改
3. **稳定性**: 避免多行字符串处理的复杂性
4. **功能完整**: 满足当前所有需求

### 切换步骤:
1. 使用 `ticket-monitor-simple.yml` 替换当前的 `ticket-monitor.yml`
2. 测试新的 workflow
3. 如果工作正常，删除旧的 workflow 文件

## 文件结构

```
.github/
├── ISSUE_TEMPLATE/
│   └── ticket-alert.md          # Issue 模板
└── workflows/
    ├── ticket-monitor.yml       # 当前 workflow (复杂)
    └── ticket-monitor-simple.yml # 简化 workflow (推荐)
```

## 测试建议

1. 先保留两个 workflow 文件
2. 将 `ticket-monitor.yml` 改名为 `ticket-monitor-old.yml.bak`
3. 将 `ticket-monitor-simple.yml` 改名为 `ticket-monitor.yml`
4. 测试新的 workflow
5. 如果工作正常，删除备份文件