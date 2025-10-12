# PersonalOS

A task management system designed for AI assistants with intelligent deduplication and MCP server integration.

## Directory Structure

```
ManagerAI/
├── core/                    # Reusable system components (public)
│   ├── mcp/                # MCP server implementation
│   │   └── server.py       # Core server with deduplication
│   ├── templates/          # Template files for users
│   │   ├── CLAUDE.md       # AI instruction template
│   │   ├── config.yaml     # Configuration template
│   │   └── gitignore       # Gitignore template
│   └── README.md           # Core system documentation
│
├── examples/               # Example usage and workflows
│   └── (example files)
│
├── Tasks/                  # Your personal tasks (gitignored)
├── CRM/                    # Your contacts (gitignored)
├── BACKLOG.md             # Your backlog (gitignored)
├── CLAUDE.md              # Your customized instructions (gitignored)
└── config.yaml            # Your configuration (gitignored)
```

## Requirements

- Python 3.7 or later
- pip package manager

## Quick Start

### For New Users

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the setup script**:
   ```bash
   python setup.py
   ```

3. **Or manually setup**:
   ```bash
   # Create personal directories
   mkdir Tasks CRM
   
   # Copy templates
   cp core/templates/CLAUDE.md ./CLAUDE.md
   cp core/templates/config.yaml ./config.yaml
   cp core/templates/gitignore ./.gitignore
   
   # Create backlog
   touch BACKLOG.md
   ```

4. **Start the MCP server**:
   ```bash
   python core/mcp/server.py
   ```

5. **Tell your AI assistant**:
   ```
   "Read CLAUDE.md for task management instructions"
   ```

## How Should You Use This?

1. Run `python setup.py` the first time—answer the short onboarding interview so `GOALS.md` reflects what matters to you.
2. Whenever ideas pop up, drop them straight into `BACKLOG.md`; stash any supporting docs in `Knowledge/`.
3. In Claude Code or Droid CLI, say “clear my backlog” to have the assistant turn those notes into structured tasks and clear the inbox.
4. Ask for guidance during the day (“What should I work on today?”, “What’s blocked?”) and follow the task files it creates under `Tasks/`.
5. Keep task status letters up to date (`n/s/b/d`) so the assistant can track progress and suggest the next focus items.
6. Review `GOALS.md` weekly and prune or reprioritize tasks to stay aligned with your objectives.

## What's What

### Core System (`core/`)
- **Public and reusable** - Safe to commit and share
- Generic MCP server with deduplication logic
- Template files for configuration
- No personal information

### Personal Data (root level)
- **Private** - Should be gitignored
- Your actual tasks, contacts, and notes
- Your customized configuration
- Never committed to public repos

### Examples (`examples/`)
- Sample workflows and use cases
- Demo tasks and configurations
- Learning resources

## Features

- 🔍 **Smart Deduplication** - Automatically detects duplicate tasks
- 🤔 **Ambiguity Detection** - Flags vague items for clarification
- 📊 **Task Organization** - Categories, priorities, and status tracking
- 👥 **CRM Integration** - Manage contacts alongside tasks
- 🔧 **MCP Server** - Reliable tool interface for AI assistants
- ⚙️ **Configurable** - Customize for your workflow

## For Contributors

The `core/` directory contains the reusable system. Contributions should:
- Not include personal information
- Be generic and configurable
- Include documentation
- Follow the existing patterns

## For Personal Use

Your personal files stay in the root directory and are gitignored:
- `Tasks/` - Your task files
- `CRM/` - Your contacts
- `BACKLOG.md` - Your notes
- `CLAUDE.md` - Your customized AI instructions
- `config.yaml` - Your configuration

## License

MIT - See LICENSE file for details.
