# Task Management System - AI Agent Instructions

You are managing a task system using markdown files with YAML frontmatter for metadata.

## System Overview

```
Project/
├── Tasks/                    # Individual task files (.md)
├── CRM/                      # Contact files (.md)
├── BACKLOG.md               # Unstructured notes to process
├── GOALS.md                 # Strategic priorities (optional)
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
---

# Task Name

## Overview
Brief description of the task and its purpose.

## Next Actions
- [ ] Specific step 1
- [ ] Specific step 2

## Notes
Additional context or requirements.
```

## Categories (Customizable)

Default categories - modify based on your workflow:
- **technical**: Development, coding, system configuration
- **outreach**: Communication, networking, emails, meetings
- **research**: Learning, analysis, investigation
- **writing**: Documentation, content creation, reports
- **admin**: Administrative, organizational tasks
- **other**: Miscellaneous tasks

## Priority Levels

- **P0**: Critical/urgent - must do immediately (limit: ~3 tasks)
- **P1**: Important - has deadlines or blocks others (~5 tasks)
- **P2**: Normal priority - scheduled work (default)
- **P3**: Low priority - nice to have

## Status Codes

- **todo**: Not started (default)
- **active**: Currently working on (limit: 1-3)
- **blocked**: Waiting on something/someone
- **done**: Completed (auto-cleaned after 30 days)

## Task Management Commands

Using the MCP tools or CLI:
- List tasks with filters (priority, category, status)
- Create new tasks with metadata
- Update task status
- Get summaries and statistics
- Check priority distribution
- Prune old completed tasks

## CRM File Format

```yaml
---
name: [Full Name]
email: [email]
company: [Company]
location: [City/Region]
last_contact: [YYYY-MM-DD]
relationship: [cold|warm|hot]
---

# Contact Name

## Notes
Interaction history and context.
```

## Best Practices

1. **Be Specific**: Vague tasks like "fix bug" should prompt clarification
2. **Check Duplicates**: Always check existing tasks before creating new ones
3. **Maintain Balance**: Monitor priority distribution
4. **Regular Cleanup**: Prune completed tasks older than 30 days
5. **Context Preservation**: Include relevant details from backlog in task notes

## Automatic Integrity Checks

When processing any request:
1. Check for duplicate tasks before creating
2. Flag ambiguous items for clarification
3. Monitor priority limits
4. Suggest task batching for similar items
5. Link related tasks and contacts

## Integration with MCP Server

The MCP server provides these tools:
- `list_tasks`: Filter and view tasks
- `create_task`: Create with metadata
- `update_task_status`: Change task state
- `process_backlog_with_dedup`: Smart backlog processing
- `list_contacts`: View CRM entries
- `add_contact`: Create contacts
- `get_system_status`: Dashboard view
- `prune_completed_tasks`: Cleanup

## Customization Points

Users can customize:
1. Categories (add/modify in personal config)
2. Priority criteria (define what's urgent for you)
3. Status codes (add custom states)
4. File naming conventions
5. Additional metadata fields

---

*This is a template. Copy to CLAUDE.md and customize for your specific workflow.*