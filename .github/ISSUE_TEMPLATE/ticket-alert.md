---
title: "🎫 Ticket Alert: {{ env.TICKET_COUNT }} target tickets found!"
assignees: {{ github.repository_owner }}
labels: ticket-alert, automated, high-priority
---

{{ env.ALERT_MESSAGE }}

## 🚀 Quick Actions
- [🎫 Buy Tickets](https://singaporegp.sg/en/tickets/general-tickets/grandstands/)
- [📊 View Run Details]({{ github.server_url }}/{{ github.repository }}/actions/runs/{{ github.run_id }})
- [⚙️ Monitor Settings](https://github.com/{{ github.repository }}/blob/main/MONITOR_SETUP.md)

## 📱 Mobile Notification
If you have the GitHub mobile app installed, you should receive a push notification for this issue.

---
**Monitoring Details:**
- 🕒 Generated at: {{ env.CURRENT_TIME }}
- 🔄 Workflow: {{ github.workflow }}
- 📋 Run ID: {{ github.run_id }}
- 🏷️ Repository: {{ github.repository }}

> This issue was created automatically when target tickets were detected.
> Close this issue when you no longer need alerts for these tickets.