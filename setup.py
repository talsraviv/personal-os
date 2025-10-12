#!/usr/bin/env python3
"""
Setup script for Personal OS task management starter
Creates necessary directories and copies template files
"""

import os
import shutil
from pathlib import Path

def setup():
    """Setup the task management system"""
    print("🚀 Setting up Personal OS Task Management System...")
    
    base_dir = Path.cwd()
    
    # Create directories
    directories = ['Tasks', 'CRM', 'Knowledge', 'examples']
    for dir_name in directories:
        dir_path = base_dir / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            print(f"✅ Created directory: {dir_name}/")
        else:
            print(f"📁 Directory exists: {dir_name}/")
    
    # Copy template files
    templates = {
        'core/templates/CLAUDE.md': 'CLAUDE.md',
        'core/templates/config.yaml': 'config.yaml',
        'core/templates/gitignore': '.gitignore',
        'core/templates/GOALS.md': 'GOALS.md'
    }
    
    for source, dest in templates.items():
        source_path = base_dir / source
        dest_path = base_dir / dest
        
        if source_path.exists():
            if dest_path.exists():
                response = input(f"⚠️  {dest} already exists. Overwrite? (y/n): ")
                if response.lower() != 'y':
                    print(f"⏭️  Skipped: {dest}")
                    continue
            
            shutil.copy2(source_path, dest_path)
            print(f"✅ Copied: {source} → {dest}")
        else:
            print(f"❌ Template not found: {source}")
    
    # Interactive GOALS setup
    goals_path = base_dir / 'GOALS.md'
    if goals_path.exists() and (goals_path.read_text().count('[') > 5):
        print("📁 GOALS.md exists with content")
    else:
        print("\n📋 Let's set up your goals and priorities...")
        print("(Press Enter to skip any question)\n")
        
        role = input("What's your current role? (e.g., Senior PM, Engineering Manager): ").strip()
        objective1 = input("What's your #1 objective this quarter? ").strip()
        objective2 = input("What's your #2 objective this quarter? ").strip()
        objective3 = input("What's your #3 objective this quarter? ").strip()
        
        # Update GOALS.md with user input if provided
        if any([role, objective1, objective2, objective3]):
            with open(goals_path, 'r') as f:
                goals_content = f.read()
            
            if role:
                goals_content = goals_content.replace(
                    "[Your current position and key responsibilities]",
                    role
                )
            
            objectives = [obj for obj in [objective1, objective2, objective3] if obj]
            if objectives:
                obj_text = "\n".join([f"{i+1}. {obj}" for i, obj in enumerate(objectives)])
                goals_content = goals_content.replace(
                    "1. [Objective 1]\n2. [Objective 2]  \n3. [Objective 3]",
                    obj_text
                )
            
            with open(goals_path, 'w') as f:
                f.write(goals_content)
            
            print("✅ Updated GOALS.md with your input")
        else:
            print("⏭️  Skipped goals setup - you can edit GOALS.md later")
    
    # Create BACKLOG.md if it doesn't exist
    backlog_path = base_dir / 'BACKLOG.md'
    if not backlog_path.exists():
        backlog_path.write_text("# Backlog\n\nDrop raw notes or todos here. Say `clear my backlog` when you're ready for triage.\n")
        print("✅ Created: BACKLOG.md")
    else:
        print("📁 File exists: BACKLOG.md")
    
    # Create GOALS.md with user input
    goals_path = base_dir / 'GOALS.md'
    if not goals_path.exists():
        print("\n🎯 Let's define your goals and design your ideal life...")
        print("Take a moment to think about what really matters to you.\n")
        
        # Professional goals
        print("1. PROFESSIONAL: What does career success look like for you in 12 months?")
        print("   (e.g., role, skills, income, impact, autonomy)")
        professional = input("   → ").strip()
        
        # Personal/Life goals
        print("\n2. PERSONAL: What would make your life feel rich and fulfilling?")
        print("   (e.g., relationships, health, hobbies, experiences, learning)")
        personal = input("   → ").strip()
        
        # Current focus
        print("\n3. NEXT 90 DAYS: What 1-3 things would create the most momentum?")
        print("   (Be specific - what will you ship, launch, or complete?)")
        focus = input("   → ").strip()
        
        goals_content = f"""# Goals & Life Design

## 12-Month Vision

### Professional
{professional if professional else '[What does career success look like?]'}

### Personal
{personal if personal else '[What makes life rich and fulfilling?]'}

## Next 90 Days - Focus Areas
{focus if focus else '[What 1-3 things create the most momentum?]'}

## Weekly Review Questions
- What moved me closer to my vision this week?
- What held me back?
- What needs to change next week?

## Decision Filter
Before taking on new commitments, ask:
- Does this align with my 12-month vision?
- Is this in my zone of genius?
- What would I need to say no to?

## Notes
- Review monthly and adjust course
- Dreams without deadlines are just wishes
- Progress > Perfection
"""
        goals_path.write_text(goals_content)
        print("\n✅ Created: GOALS.md with your life design")
    else:
        print("📁 File exists: GOALS.md")
    
    # Create example files
    example_task = base_dir / 'examples' / 'example_task.md'
    if not example_task.exists():
        example_task.write_text("""---
title: Example Task
category: technical
priority: P2
status: n
estimated_time: 60
resource_refs:
  - Knowledge/example-brief.md
---

# Example Task

## Context
This supports the "Audience growth" goal and references Knowledge/example-brief.md.

## Next Actions
- [ ] First step
- [ ] Second step

## Progress Log
- 2024-10-12: Created example task template.
""")
        print("✅ Created: examples/example_task.md")
    
    print("\n✨ Setup complete!")
    print("\nNext steps:")
    print("1. Review GOALS.md to refine your objectives")
    print("2. Edit CLAUDE.md to customize your AI instructions")
    print("3. Edit config.yaml to set your categories and priorities")
    print("4. Start the MCP server: python manager_ai_mcp/server.py")
    print("5. Tell your AI: 'Read CLAUDE.md for task management'")
    print("\nHappy task managing! 🎯")

if __name__ == "__main__":
    setup()