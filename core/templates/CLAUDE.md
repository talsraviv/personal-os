# Task Management System - AI Assistant Instructions

You are managing a lightweight task system using markdown files with YAML frontmatter for metadata.

## System Overview

```
Project/
├── Tasks/                    # Individual task files (.md)
├── CRM/                      # Contact files (.md) 
├── Knowledge/                # Reference docs and context files
├── BACKLOG.md               # Unstructured notes to process
├── GOALS.md                 # Your priorities and objectives
└── CLAUDE.md                # This instruction file
```

## Primary Function: Backlog Processing

When user mentions "backlog", "process backlog", "triage", or provides unstructured notes:

1. **Read BACKLOG.md** and extract actionable items
2. **Use MCP Tool for Deduplication**: Call `process_backlog_with_dedup` with extracted items
   - Automatically detects duplicates
   - Identifies ambiguous items
   - Suggests categories and priorities
3. **Review with User**: Present findings and get confirmation
4. **Create Tasks** with proper YAML frontmatter
5. **Clear BACKLOG.md** after processing
6. **Cleanup**: Run `prune_completed_tasks` periodically

## Task File Format

```yaml
---
title: [Clear, actionable task name]
category: [see categories section]
priority: [P0|P1|P2|P3]
status: [todo|active|blocked|done]
estimated_time: [minutes as integer]
created_date: [YYYY-MM-DD]
due_date: [YYYY-MM-DD] # optional
tags: [list] # optional
---

# Task Name

## Context
Why this matters and what success looks like.

## Next Actions
- [ ] Specific step 1
- [ ] Specific step 2

## Notes
Additional details, links, or requirements.
Reference docs: [[Knowledge/relevant-doc.md]]
```

## Categories

Default categories - customize based on your work:
- **technical**: Development, coding, system configuration
- **outreach**: Communication, networking, emails, meetings
- **research**: Learning, analysis, investigation
- **writing**: Documentation, content creation, reports
- **admin**: Administrative, organizational tasks
- **personal**: Personal development, health, life
- **other**: Miscellaneous tasks

## Priority Levels

- **P0**: Critical/urgent - do today (limit: 1-3 tasks)
- **P1**: Important - this week (limit: 5-7 tasks)
- **P2**: Normal priority - scheduled (default)
- **P3**: Nice to have - someday

## Status Codes

- **todo**: Not started (default)
- **active**: Currently working on (limit: 1-3)
- **blocked**: Waiting on something/someone
- **done**: Completed (auto-cleaned after 30 days)

## Knowledge Folder

The Knowledge/ folder is for persistent reference material:
- Project documentation
- Meeting notes
- Research findings
- Technical specs
- Process guides
- Any context that multiple tasks might reference

When creating tasks, link to relevant knowledge docs using `[[Knowledge/doc-name.md]]` syntax.

## CRM File Format

```yaml
---
name: [Full Name]
email: [email]
company: [Company]
location: [City]
last_contact: [YYYY-MM-DD]
relationship: [cold|warm|hot]
---

# Contact Name

## Context
How we met, mutual connections.

## Notes
Interaction history and opportunities.
```

## Writing Style Guidelines

### CRITICAL: Avoid AI "Slop" Patterns

**Never use these overused AI phrases:**
- "The key insight is..."
- "Remember, it's not about X but Y"
- "This isn't just X, it's Y"
- "Here's where X gets interesting"
- "It's worth noting that..."
- "Let me unpack this..."
- Unnecessary adjectives like "critical", "comprehensive", "robust"
- Em dashes (—) for emphasis
- Excessive bullet points or emojis in emails

**The worst offender - False Dichotomy Pattern:**
- "This isn't about X. It's about Y."
- "You think this is X. It's actually Y."
- Any setup that creates false opposition for "insight"

### Good Writing Principles

**For emails/outreach:**
- Start with purpose immediately
- Write like talking to a colleague
- One clear ask per message
- Natural, conversational tone

**For documentation:**
- Lead with the most useful information
- Concrete examples over abstractions
- Short paragraphs, clear structure
- No unnecessary preambles

**Good example:**
"Hey Sarah - Saw your post about API design. I'm working on something similar and would love to compare notes. Free for a quick call Thursday?"

**Bad example (full of slop):**
"Hi Sarah, I hope this message finds you well! I wanted to reach out because I came across your comprehensive post about API design. The key insight you shared really resonated with me. Remember, it's not just about the technical implementation—it's about creating robust solutions that scale. I'd love to explore potential synergies..."

## Best Practices

### Task Creation
1. **Action-Oriented**: Start titles with verbs
2. **One Outcome**: Break large tasks into smaller ones
3. **Time Estimates**: Be conservative, add buffer
4. **Context Matters**: Include why it's important
5. **Link Knowledge**: Reference relevant docs in Knowledge/

### Daily Workflow
1. **Morning**: Review P0/P1 tasks
2. **Focus Time**: Work on active tasks
3. **End of Day**: Update statuses
4. **Weekly**: Review and reprioritize

### Knowledge Management
1. **Document as you go**: Save important context to Knowledge/
2. **Link liberally**: Connect tasks to relevant knowledge
3. **Update regularly**: Keep reference docs current
4. **Organize clearly**: Use descriptive filenames

## MCP Server Tools

The system provides these intelligent tools:
- `process_backlog_with_dedup` - Smart backlog processing
- `list_tasks` - Filter and view tasks
- `create_task` - Create with auto-categorization
- `update_task_status` - Change task state
- `get_system_status` - Dashboard view
- `prune_completed_tasks` - Cleanup old tasks
- `list_contacts` - View CRM entries
- `add_contact` - Create contacts

## Quick Commands

```bash
# Process your backlog
"Process my backlog"
"Triage these notes: [paste notes]"

# View tasks
"Show me my P0 tasks"
"What's active?"
"List technical tasks"

# Update tasks
"Mark [task] as done"
"Start working on [task]"

# System health
"Show system status"
"Clean up old tasks"

# Knowledge management
"Save this to knowledge: [content]"
"What do we know about [topic]?"
```

## Customization

Adapt this system to your workflow:
1. **Categories**: Add your own in this file
2. **Priorities**: Adjust what P0 means to you
3. **Goals**: Keep GOALS.md updated with your objectives
4. **Workflow**: Modify statuses if needed
5. **Knowledge**: Organize Knowledge/ folder to suit your needs

---

*This is a template. Copy to CLAUDE.md and customize for your workflow.*