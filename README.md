# Singapore GP Ticket Checker & Monitor

A command-line tool to check Singapore Grand Prix ticket availability with automated monitoring and email alerts.

## Features

- **一键查看所有可用票务** - 单次请求获取所有票务，按日期智能分组显示
- **智能日期识别** - 从网站CSS类自动识别票务对应的日期（3天、周五、周六、周日）
- Check relevant ticket categories (grandstands, hospitality, walkabouts, combination packages)
- Filter by specific days (3-days, Friday, Saturday, Sunday)  
- Color-coded output (green for available, red for sold out)
- Structured ticket information with prices and availability status
- Available-only filter to hide sold out tickets
- Summary statistics across all days
- **高效设计** - 单次curl获取所有信息，无需多次请求
- **🤖 自动监控** - GitHub Action 每10分钟自动检查目标票务并邮件提醒

## Installation

The tool automatically sets up a virtual environment on first run.

## Usage

### Basic Usage
```bash
# 默认模式：检查所有日期选项，只显示可用票务
./run_check.sh

# Check specific category
./run_check.sh --category hospitality

# Check specific day
./run_check.sh --day friday

# Show only available tickets for a specific day
./run_check.sh --day saturday --available-only
```

### Options

- `--category`: Choose from grandstands, hospitality, walkabouts, combination-packages
- `--day`: Filter by all, 3-days, friday, saturday, sunday (default: all)
- `--available-only`: Show only available tickets (hide sold out)
- `--verbose`: Show detailed output
- `--no-color`: Disable colored output
- `--help`: Show help message

### Examples

```bash
# 查看所有可用票务（推荐）
./run_check.sh

# Check only available walkabout tickets for Friday
./run_check.sh --category walkabouts --day friday --available-only

# Check hospitality packages with verbose output
./run_check.sh --category hospitality --verbose

# Check 3-day passes only
./run_check.sh --day 3-days

# Check without colors (for redirecting to file)
./run_check.sh --no-color > tickets.txt
```

## Output

The tool displays:
- **按日期分组的可用票务** - 3天票、周五票、周六票、周日票分别显示
- Ticket names organized by category within each day
- Prices in SGD
- Availability status (Available/Sold Out)
- Summary with count per day and total available count

### 示例输出:
```
=== 3-Days Available Tickets ===
Observ@3                                           $9,374     AVAILABLE [Hospitality]

=== Friday Available Tickets ===
Chicane @ Turn 2 Grandstand[FRI]                   $318       AVAILABLE [Grandstands]
Premier Walkabout[FRI]                             $188       AVAILABLE [Walkabouts]

=== Saturday Available Tickets ===
Chicane @ Turn 2 Grandstand[SAT]                   $738       AVAILABLE [Grandstands]
Republic Grandstand[SAT]                           $438       AVAILABLE [Grandstands]

Summary Across All Days:
3-Days: 2 available
Friday: 3 available  
Saturday: 5 available
Sunday: 1 available
Total available tickets: 11
```

## 🤖 自动监控系统

### 监控功能
除了手动检查票务，本工具还提供自动监控功能：

- **🕒 每10分钟自动检查**
- **📧 邮件即时提醒**
- **🎯 智能条件匹配**
- **📊 GitHub Issues 记录**

### 监控的票务类型
1. **周日的 grandstand 票** (高优先级)
2. **三日票价格 ≤ $1500** (高优先级)  
3. **周五 premier walkabout 票** (中优先级)
4. **grandstand 票价格 ≤ $300** (中优先级)

### 快速开始监控
```bash
# 1. 测试监控功能
python test_monitor.py

# 2. 手动运行一次监控
python monitor_tickets.py

# 3. 设置 GitHub Action 自动监控
# 参见 MONITOR_SETUP.md 详细说明
```

详细的监控设置请参考 [MONITOR_SETUP.md](MONITOR_SETUP.md)

---

## Requirements

- Python 3.6+
- Internet connection
- macOS/Linux (Windows users can run check_tickets.py directly)
- For monitoring: GitHub account with Actions enabled