# Personal OS - Quick Setup Guide

Welcome! Let's get your personal task management system running in 5 minutes.

## 🚀 Quick Start

### 1. Clone and Setup (30 seconds)
```bash
git clone https://github.com/yourusername/personal-os.git my-tasks
cd my-tasks
```

### 2. Create Your GOALS.md (2 minutes)

Let Claude help you define your goals. In Claude Code, say:
```
Help me set up my goals. Ask me questions about:
- What I'm working toward professionally
- My current role and responsibilities  
- What success looks like for me this quarter
- My top 3 priorities right now
```

Claude will create a GOALS.md file based on your answers.

### 3. Create Your First Tasks (1 minute)

Either:
- **Quick dump**: Paste your todo list into BACKLOG.md
- **Direct create**: Tell Claude "Create a task to [whatever you need to do]"

### 4. Process Your Backlog (1 minute)

Say to Claude:
```
Process my backlog
```

Claude will:
- Detect any duplicate tasks
- Suggest categories and priorities based on your goals
- Create organized task files
- Clear the backlog when done

## 📝 Essential Commands

These are the only commands you need to remember:

### Daily Use
- `"Process my backlog"` - Turn notes into tasks
- `"Show me my P0 tasks"` - See urgent items
- `"What should I work on?"` - Get suggestions
- `"Mark [task] as done"` - Complete tasks

### Weekly Maintenance  
- `"Show system status"` - See your workload
- `"Clean up old tasks"` - Archive completed work
- `"Review my goals"` - Realign priorities

### When Stuck
- `"What's blocking me?"` - See blocked tasks
- `"Show active tasks"` - See work in progress

## 🎯 How Priorities Work

- **P0**: Do today (max 3)
- **P1**: This week (max 7)
- **P2**: Scheduled (default)
- **P3**: Someday/maybe

The system warns you if you have too many urgent tasks.

## 📂 Your Folder Structure

```
my-tasks/
├── Tasks/          # Your tasks live here
├── CRM/            # People you know
├── Knowledge/      # Your reference docs
├── BACKLOG.md      # Quick capture
├── GOALS.md        # Your north star
└── CLAUDE.md       # System config
```

## 🔄 Your Daily Workflow

### Morning (2 min)
1. `"Show me today's priorities"`
2. Pick 1-3 tasks to make active
3. `"Start working on [task name]"`

### During Work
- Update task notes as you go
- `"Block [task] - waiting on [reason]"` if stuck

### End of Day (2 min)
1. `"Mark [task] as done"` for completed work
2. `"Show me tomorrow's tasks"` to prep

### Weekly (5 min)
1. `"Process my backlog"` if you have notes
2. `"Clean up old tasks"` to archive
3. Review and adjust priorities

## 💡 Pro Tips

1. **Brain dump freely**: Use BACKLOG.md for quick capture, process later
2. **Link knowledge**: Save important docs to Knowledge/ and reference them
3. **Track relationships**: Add people to CRM when you meet them
4. **Be realistic**: 3 hours of deep work = 1-2 big tasks max
5. **Context is king**: Tasks should explain WHY they matter

## 🤝 Adding Contacts

When you meet someone:
```
Add contact: John Smith, john@company.com, NYC, met at AI conference
```

## 📚 Saving Knowledge

Important document or context:
```
Save this to knowledge as "project-xyz-spec": [paste content]
```

## ⚙️ Customization

Edit CLAUDE.md to:
- Add your own categories
- Adjust priority meanings
- Customize the workflow

## 🆘 Getting Help

- `"Explain the task system"` - How it works
- `"Show me examples"` - See sample tasks
- Check core/templates/ for examples

## Ready to Start?

1. Create your GOALS.md
2. Dump your todos into BACKLOG.md
3. Say "Process my backlog"
4. You're running!

The system learns your patterns over time and gets smarter about categorization and priorities.