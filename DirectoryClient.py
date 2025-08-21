#!/usr/bin/env python3
"""
DirectoryClient.py - CLI tool for managing TODO system and CRM

Task Management:
    python DirectoryClient.py list [--category CATEGORY] [--priority PRIORITY] [--status STATUS] [--include-done]
    python DirectoryClient.py prune-tasks [--days-old DAYS]
    python DirectoryClient.py update-status TASK_FILE STATUS
    python DirectoryClient.py start TASK_FILE
    python DirectoryClient.py complete TASK_FILE
    python DirectoryClient.py summary
    python DirectoryClient.py check-limits

CRM Management:
    python DirectoryClient.py crm-list [--location LOCATION] [--company COMPANY] [--name NAME]
    python DirectoryClient.py crm-add NAME [--email EMAIL] [--company COMPANY] [--location LOCATION]
    python DirectoryClient.py crm-update NAME FIELD VALUE
    python DirectoryClient.py crm-search QUERY
    python DirectoryClient.py crm-summary

System Management:
    python DirectoryClient.py status          # Comprehensive system status dashboard
    python DirectoryClient.py double-check    # Check system integrity and recent work
    python DirectoryClient.py anticipate      # Suggest next actions based on current state
"""

import os
import sys
import argparse
import yaml
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, timedelta

class DirectoryClient:
    def __init__(self, base_dir=None):
        if base_dir is None:
            current_dir = Path.cwd()
            if current_dir.name in ['ManagerAI', 'TODOAgent']:
                base_dir = current_dir
            else:
                # Look for ManagerAI first, then fall back to TODOAgent
                if (current_dir / 'ManagerAI').exists():
                    base_dir = current_dir / 'ManagerAI'
                else:
                    base_dir = current_dir
        
        self.base_dir = Path(base_dir)
        self.tasks_dir = self.base_dir / 'Tasks'
        self.crm_dir = self.base_dir / 'CRM'
        
        self.tasks_dir.mkdir(exist_ok=True)
        self.crm_dir.mkdir(exist_ok=True)
    
    def parse_markdown_file(self, file_path):
        """Parse a markdown file and extract YAML frontmatter"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.startswith('---'):
                return None
            
            parts = content.split('---', 2)
            if len(parts) < 3:
                return None
            
            yaml_content = parts[1].strip()
            data = yaml.safe_load(yaml_content)
            data['file_path'] = file_path
            data['filename'] = file_path.name
            data['body_content'] = parts[2].strip() if len(parts) > 2 else ""
            
            return data
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None
    
    def get_all_tasks(self):
        """Get all tasks from the Tasks directory"""
        tasks = []
        for file_path in self.tasks_dir.glob('*.md'):
            task_data = self.parse_markdown_file(file_path)
            if task_data:
                tasks.append(task_data)
        return tasks
    
    def filter_tasks(self, tasks, category=None, priority=None, status=None):
        """Filter tasks based on criteria"""
        filtered = tasks
        
        if category:
            categories = [c.strip() for c in category.split(',')]
            filtered = [t for t in filtered if t.get('category') in categories]
        
        if priority:
            priorities = [p.strip() for p in priority.split(',')]
            filtered = [t for t in filtered if t.get('priority') in priorities]
        
        if status:
            statuses = [s.strip() for s in status.split(',')]
            filtered = [t for t in filtered if t.get('status') in statuses]
        
        return filtered
    
    def list_tasks(self, category=None, priority=None, status=None, include_done=False):
        """List tasks with optional filters, hiding completed by default."""
        tasks = self.get_all_tasks()
        
        if not include_done and status is None:
            tasks = [t for t in tasks if t.get('status') != 'd']
            
        filtered_tasks = self.filter_tasks(tasks, category, priority, status)
        
        if not filtered_tasks:
            print("No tasks found matching criteria.")
            return
        
        by_priority = defaultdict(list)
        for task in filtered_tasks:
            by_priority[task.get('priority', 'P2')].append(task)
        
        for priority in ['P0', 'P1', 'P2', 'P3']:
            if priority in by_priority:
                print(f"\n=== {priority} Tasks ===")
                for task in by_priority[priority]:
                    status_icon = {'n': '○', 's': '◐', 'b': '◑', 'd': '●'}.get(task.get('status', 'n'), '?')
                    print(f"{status_icon} [{(task.get('category') or 'other'):10}] {task.get('title', 'Untitled')} ({task['filename']})")

    def prune_old_done_tasks(self, days_old=30):
        """Delete completed tasks older than a specified number of days."""
        tasks = self.get_all_tasks()
        done_tasks = [t for t in tasks if t.get('status') == 'd']
        
        if not done_tasks:
            print("No completed tasks to prune.")
            return
        
        pruned_count = 0
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        for task in done_tasks:
            file_path = Path(task['file_path'])
            modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            
            if modified_time < cutoff_date:
                try:
                    file_path.unlink()
                    pruned_count += 1
                    print(f"Pruned old task: {task.get('title', file_path.name)}")
                except Exception as e:
                    print(f"Error pruning {file_path.name}: {e}")
        
        print(f"\nPruned {pruned_count} completed tasks older than {days_old} days.")

    def update_task_status(self, task_file, new_status):
        """Update the status of a specific task"""
        file_path = self.tasks_dir / task_file
        if not file_path.exists():
            print(f"Task file not found: {task_file}")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.startswith('---'):
                print("Invalid task file format (no YAML frontmatter)")
                return False
            
            parts = content.split('---', 2)
            yaml_content = parts[1].strip()
            body_content = parts[2] if len(parts) > 2 else ""
            
            task_data = yaml.safe_load(yaml_content)
            task_data['status'] = new_status
            
            new_yaml = yaml.dump(task_data, default_flow_style=False, sort_keys=False)
            new_content = f"---\n{new_yaml}---{body_content}"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"Updated {task_file} status to '{new_status}'")
            return True
            
        except Exception as e:
            print(f"Error updating {task_file}: {e}")
            return False
    
    def start_task(self, task_file):
        """Mark a task as started"""
        return self.update_task_status(task_file, 's')
    
    def complete_task(self, task_file):
        """Mark a task as completed"""
        return self.update_task_status(task_file, 'd')
    
    def show_summary(self):
        """Show summary statistics"""
        tasks = self.get_all_tasks()
        
        if not tasks:
            print("No tasks found.")
            return
        
        by_priority = Counter(t.get('priority', 'P2') for t in tasks)
        by_category = Counter(t.get('category', 'other') for t in tasks)
        by_status = Counter(t.get('status', 'n') for t in tasks)
        
        print("=== Task Summary ===")
        print(f"Total Tasks: {len(tasks)}")
        
        print(f"\nBy Priority:")
        for priority in ['P0', 'P1', 'P2', 'P3']:
            print(f"  {priority}: {by_priority.get(priority, 0)}")
        
        print(f"\nBy Category:")
        for category, count in by_category.most_common():
            print(f"  {category}: {count}")
        
        print(f"\nBy Status:")
        status_names = {'n': 'Not Started', 's': 'Started', 'b': 'Blocked', 'd': 'Done'}
        for status in ['n', 's', 'b', 'd']:
            print(f"  {status_names.get(status, status)}: {by_status.get(status, 0)}")
    
    def check_priority_limits(self):
        """Check priority distribution and alert on high counts"""
        tasks = [t for t in self.get_all_tasks() if t.get('status') != 'd']
        by_priority = Counter(t.get('priority', 'P2') for t in tasks)
        
        thresholds = {'P0': 3, 'P1': 5, 'P2': 10}  # Now just thresholds for alerts, not hard limits
        alerts = []
        
        print("=== Priority Distribution (active tasks only) ===")
        for priority in ['P0', 'P1', 'P2', 'P3']:
            count = by_priority.get(priority, 0)
            if priority in thresholds:
                threshold = thresholds[priority]
                if count > threshold:
                    print(f"⚠️  {priority}: {count} (above typical threshold of {threshold})")
                    alerts.append(f"{priority} has {count} tasks (typical threshold: {threshold})")
                else:
                    print(f"✓ {priority}: {count}/{threshold}")
            else:
                print(f"  {priority}: {count}")
        
        if alerts:
            print(f"\n💡 Note: You have a high concentration of priority tasks:")
            for alert in alerts:
                print(f"   {alert}")
            print("   Consider if all these are truly high priority.")
        else:
            print(f"\n✓ Priority distribution looks balanced")
    
    def get_all_contacts(self):
        """Get all contacts from the CRM directory"""
        contacts = []
        for file_path in self.crm_dir.glob('*.md'):
            contact_data = self.parse_markdown_file(file_path)
            if contact_data:
                contacts.append(contact_data)
        return contacts
    
    def filter_contacts(self, contacts, location=None, company=None, name=None):
        """Filter contacts based on criteria"""
        filtered = contacts
        
        if location:
            locations = [l.strip().lower() for l in location.split(',')]
            filtered = [c for c in filtered if (c.get('location') or '').lower() in locations]
        
        if company:
            companies = [comp.strip().lower() for comp in company.split(',')]
            filtered = [c for c in filtered if any(comp in (c.get('company') or '').lower() for comp in companies)]
        
        if name:
            name_search = name.lower()
            filtered = [c for c in filtered if name_search in (c.get('name') or '').lower()]
        
        return filtered
    
    def list_contacts(self, location=None, company=None, name=None):
        """List contacts with optional filters"""
        contacts = self.get_all_contacts()
        filtered_contacts = self.filter_contacts(contacts, location, company, name)
        
        if not filtered_contacts:
            print("No contacts found matching criteria.")
            return
        
        by_location = defaultdict(list)
        for contact in filtered_contacts:
            by_location[contact.get('location', 'Unknown')].append(contact)
        
        for location, location_contacts in by_location.items():
            print(f"\n=== {location} ===")
            for contact in location_contacts:
                company = contact.get('company', 'No company')
                email = contact.get('email', 'No email')
                last_contact = contact.get('last_contact', 'Never')
                relationship = contact.get('relationship_strength', 'unknown')
                
                print(f"• {contact.get('name', 'Unknown')} @ {company}")
                print(f"  Email: {email} | Last contact: {last_contact} | Relationship: {relationship}")
    
    def add_contact(self, name, email=None, company=None, location=None, phone=None, linkedin=None):
        """Add a new contact to CRM"""
        filename = name.replace('.', '') + '.md'
        file_path = self.crm_dir / filename
        
        if file_path.exists():
            print(f"Contact {name} already exists at {filename}")
            return False
        
        contact_data = {
            'name': name, 'email': email, 'company': company, 'location': location,
            'phone': phone, 'linkedin': linkedin,
            'last_contact': datetime.now().strftime('%Y-%m-%d'),
            'relationship_strength': 'new',
            'created_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        contact_data = {k: v for k, v in contact_data.items() if v}
        yaml_content = yaml.dump(contact_data, default_flow_style=False, sort_keys=False)
        
        content = f"""---
{yaml_content}---

# {name}
## Contact Information
- **Company**: {company or 'TBD'}
- **Role**: 
- **Email**: {email or 'TBD'}
- **Phone**: {phone or 'TBD'}
- **LinkedIn**: {linkedin or 'TBD'}
- **Location**: {location or 'TBD'}

## Relationship Notes
- 

## Interaction History
### {datetime.now().strftime('%Y-%m-%d')}
- Contact added to CRM

## Next Steps
- [ ] Initial outreach
"""
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added contact: {name} ({filename})")
            return True
        except Exception as e:
            print(f"Error adding contact {name}: {e}")
            return False
    
    def update_contact_field(self, name, field, value):
        """Update a specific field for a contact"""
        file_path = None
        for f_path in self.crm_dir.glob('*.md'):
            contact_data = self.parse_markdown_file(f_path)
            if contact_data and contact_data.get('name', '').lower() == name.lower():
                file_path = f_path
                break
        
        if not file_path:
            print(f"Contact {name} not found.")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            parts = content.split('---', 2)
            yaml_content = parts[1].strip()
            body_content = parts[2] if len(parts) > 2 else ""
            
            contact_data = yaml.safe_load(yaml_content)
            contact_data[field] = value
            
            new_yaml = yaml.dump(contact_data, default_flow_style=False, sort_keys=False)
            new_content = f"---\n{new_yaml}---{body_content}"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"Updated {name} {field} to '{value}'")
            return True
            
        except Exception as e:
            print(f"Error updating {name}: {e}")
            return False
    
    def search_contacts(self, query):
        """Search contacts by name, company, or content"""
        contacts = self.get_all_contacts()
        query_lower = query.lower()
        
        matches = [c for c in contacts if 
                   query_lower in (c.get('name') or '').lower() or
                   query_lower in (c.get('company') or '').lower() or
                   query_lower in str(c.get('email') or '').lower() or
                   query_lower in (c.get('location') or '').lower() or
                   query_lower in (c.get('body_content') or '').lower()]
        
        if not matches:
            print(f"No contacts found matching '{query}'")
            return
        
        print(f"\n=== Search Results for '{query}' ===")
        for contact in matches:
            print(f"• {contact.get('name', 'Unknown')} @ {contact.get('company', 'No company')} ({contact['filename']})")
    
    def crm_summary(self):
        """Show CRM summary statistics"""
        contacts = self.get_all_contacts()
        
        if not contacts:
            print("No contacts found.")
            return
        
        by_location = Counter(c.get('location', 'Unknown') for c in contacts)
        by_company = Counter(c.get('company', 'Unknown') for c in contacts)
        by_relationship = Counter(c.get('relationship_strength', 'unknown') for c in contacts)
        
        print("=== CRM Summary ===")
        print(f"Total Contacts: {len(contacts)}")
        
        print(f"\nBy Location:")
        for location, count in by_location.most_common():
            print(f"  {location}: {count}")
        
        print(f"\nTop 10 Companies:")
        for company, count in by_company.most_common(10):
            print(f"  {company}: {count}")
        
        print(f"\nBy Relationship Strength:")
        for strength, count in by_relationship.most_common():
            print(f"  {strength}: {count}")
    
    def double_check_work(self):
        """Double-check system integrity and recent work"""
        print("=== Double-Checking System Integrity ===\n")
        
        # Check for tasks without proper YAML frontmatter
        print("1. Checking task file integrity...")
        malformed_tasks = []
        for task_file in self.tasks_dir.glob('*.md'):
            try:
                with open(task_file, 'r') as f:
                    content = f.read()
                    if not content.startswith('---'):
                        malformed_tasks.append(task_file.name)
                    else:
                        # Try to parse YAML
                        parts = content.split('---', 2)
                        if len(parts) < 3:
                            malformed_tasks.append(task_file.name)
                        else:
                            yaml.safe_load(parts[1])
            except Exception as e:
                malformed_tasks.append(f"{task_file.name} (Error: {str(e)})")
        
        if malformed_tasks:
            print(f"   ⚠️  Found {len(malformed_tasks)} tasks with issues:")
            for task in malformed_tasks:
                print(f"      - {task}")
        else:
            print("   ✓ All task files properly formatted")
        
        # Check priority distribution
        print("\n2. Checking priority distribution...")
        all_tasks = self.get_all_tasks()
        tasks = [t for t in all_tasks if t.get('status') != 'd']  # Exclude done tasks
        priority_counts = Counter(task['priority'] for task in tasks)
        
        thresholds = {'P0': 3, 'P1': 5, 'P2': 10}  # Thresholds for alerts only
        high_priority_alerts = []
        for priority, threshold in thresholds.items():
            count = priority_counts.get(priority, 0)
            if count > threshold:
                high_priority_alerts.append(f"{priority}: {count} tasks (typical threshold: {threshold})")
        
        if high_priority_alerts:
            print("   💡 High priority concentration:")
            for alert in high_priority_alerts:
                print(f"      - {alert}")
        else:
            print("   ✓ Priority distribution is balanced")
        
        # Check for duplicate tasks
        print("\n3. Checking for duplicate tasks...")
        task_titles = [task['title'] for task in tasks]
        duplicates = [title for title, count in Counter(task_titles).items() if count > 1]
        
        if duplicates:
            print(f"   ⚠️  Found {len(duplicates)} duplicate task titles:")
            for dup in duplicates:
                print(f"      - {dup}")
        else:
            print("   ✓ No duplicate tasks found")
        
        # Check for orphaned CRM contacts (mentioned in tasks but no CRM file)
        print("\n4. Checking CRM consistency...")
        crm_names_in_tasks = set()
        for task in tasks:
            if task['category'] == 'outreach':
                # Simple name extraction from title
                title_words = task['title'].lower().split()
                for i, word in enumerate(title_words):
                    if word in ['with', 'to', 'contact']:
                        if i + 1 < len(title_words):
                            crm_names_in_tasks.add(title_words[i + 1].title())
        
        existing_contacts = set(c['name'].split()[0] for c in self.get_all_contacts() if c.get('name'))
        missing_contacts = crm_names_in_tasks - existing_contacts
        
        if missing_contacts:
            print(f"   ⚠️  Contacts mentioned in tasks but not in CRM:")
            for contact in missing_contacts:
                print(f"      - {contact}")
        else:
            print("   ✓ CRM and tasks are consistent")
        
        # Recent activity check
        print("\n5. Recent activity (last 7 days)...")
        recent_date = datetime.now() - timedelta(days=7)
        recent_tasks = []
        
        for task_file in self.tasks_dir.glob('*.md'):
            if task_file.stat().st_mtime > recent_date.timestamp():
                recent_tasks.append(task_file.name)
        
        if recent_tasks:
            print(f"   Recently modified tasks ({len(recent_tasks)}):")
            for task in recent_tasks[-5:]:  # Show last 5
                print(f"      - {task}")
            if len(recent_tasks) > 5:
                print(f"      ... and {len(recent_tasks) - 5} more")
        else:
            print("   No recent task activity")
    
    def anticipate_next(self):
        """Anticipate next questions/tasks and suggest proactive actions"""
        print("=== Anticipating Next Steps ===\n")
        
        all_tasks = self.get_all_tasks()
        tasks = [t for t in all_tasks if t.get('status') != 'd']  # Exclude done tasks
        goals = self._read_goals()
        
        # Group tasks by status and priority
        started_tasks = [t for t in tasks if t['status'] == 's']
        not_started_high_pri = [t for t in tasks if t['status'] == 'n' and t['priority'] in ['P0', 'P1']]
        blocked_tasks = [t for t in tasks if t['status'] == 'b']
        
        suggestions = []
        
        # 1. Started tasks that might need attention
        if started_tasks:
            suggestions.append({
                'type': 'In-Progress Tasks',
                'items': [f"Continue work on: {t['title']}" for t in started_tasks[:3]],
                'command': f"python DirectoryClient.py list --status s"
            })
        
        # 2. High priority tasks not yet started
        if not_started_high_pri:
            suggestions.append({
                'type': 'High Priority Tasks to Start',
                'items': [f"{t['priority']}: {t['title']}" for t in not_started_high_pri[:3]],
                'command': f"python DirectoryClient.py start '{not_started_high_pri[0]['filename']}'"
            })
        
        # 3. Blocked tasks that might be unblocked
        if blocked_tasks:
            suggestions.append({
                'type': 'Blocked Tasks to Review',
                'items': [f"{t['title']} (check if unblocked)" for t in blocked_tasks[:2]],
                'command': "python DirectoryClient.py list --status b"
            })
        
        # 4. Category-based suggestions
        category_counts = Counter(t['category'] for t in tasks)
        
        # If heavy on one category, suggest balance
        if category_counts:
            top_category = category_counts.most_common(1)[0]
            if top_category[1] > len(tasks) * 0.5:  # More than 50% in one category
                other_categories = [cat for cat in ['outreach', 'technical', 'writing', 'research'] 
                                  if cat != top_category[0]]
                suggestions.append({
                    'type': 'Category Balance',
                    'items': [f"Consider adding more {cat} tasks for balance" for cat in other_categories[:2]],
                    'command': None
                })
        
        # 5. Time-based suggestions
        current_hour = datetime.now().hour
        if 9 <= current_hour < 12:  # Morning
            outreach_tasks = [t for t in tasks if t['category'] == 'outreach' and t['status'] == 'n']
            if outreach_tasks:
                suggestions.append({
                    'type': 'Morning Outreach',
                    'items': ["Morning is ideal for outreach - consider sending emails"],
                    'command': "python DirectoryClient.py list --category outreach --status n"
                })
        elif 14 <= current_hour < 17:  # Afternoon
            deep_work = [t for t in tasks if t['category'] in ['technical', 'writing', 'research'] 
                        and t['status'] == 'n']
            if deep_work:
                suggestions.append({
                    'type': 'Afternoon Deep Work',
                    'items': ["Good time for focused technical/writing work"],
                    'command': "python DirectoryClient.py list --category technical,writing,research --status n"
                })
        
        # 6. Maintenance suggestions
        done_tasks = [t for t in all_tasks if t['status'] == 'd']  # Use all_tasks from above
        old_done = [t for t in done_tasks 
                   if (datetime.now() - datetime.fromisoformat(t.get('completed_date', '2020-01-01'))).days > 30]
        if len(old_done) > 10:
            suggestions.append({
                'type': 'Maintenance',
                'items': [f"Clean up {len(old_done)} old completed tasks"],
                'command': "python DirectoryClient.py prune-tasks --days-old 30"
            })
        
        # 7. Goal alignment check
        if goals and 'current focus' in goals.lower():
            suggestions.append({
                'type': 'Goal Alignment',
                'items': ["Review if current tasks align with goals in Goals.md"],
                'command': "cat Goals.md"
            })
        
        # Display suggestions
        if not suggestions:
            print("No specific suggestions at this time. System appears well-managed!")
            return
        
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion['type']}:")
            for item in suggestion['items']:
                print(f"   • {item}")
            if suggestion['command']:
                print(f"   → Run: {suggestion['command']}")
            print()
        
        # Proactive action prompt
        print("\n💡 Quick Actions:")
        print("1. Review and start highest priority task")
        print("2. Process any items in BACKLOG.md")
        print("3. Update status of in-progress tasks")
        print("4. Add new contacts from recent interactions to CRM")
    
    def _read_goals(self):
        """Helper to read Goals.md content"""
        goals_file = self.base_dir / 'Goals.md'
        if goals_file.exists():
            try:
                with open(goals_file, 'r') as f:
                    return f.read()
            except:
                pass
        return ""
    
    def status(self):
        """Show comprehensive system status with actionable insights"""
        print("=== 📊 Current System Status ===\n")
        
        # Get all tasks
        all_tasks = self.get_all_tasks()
        active_tasks = [t for t in all_tasks if t.get('status') != 'd']
        
        # Priority distribution
        priority_counts = Counter(task['priority'] for task in active_tasks)
        limits = {'P0': 3, 'P1': 5, 'P2': 10}
        
        print("## Priority Distribution:")
        for priority in ['P0', 'P1', 'P2', 'P3']:
            count = priority_counts.get(priority, 0)
            if priority in limits:
                threshold = limits[priority]
                if count > threshold:
                    print(f"- **{priority}**: {count} ⚠️ (above typical threshold of {threshold})")
                else:
                    print(f"- **{priority}**: {count}")
            else:
                print(f"- **{priority}**: {count}")
        
        # Add a note if there are many high-priority items
        high_pri_count = priority_counts.get('P0', 0) + priority_counts.get('P1', 0)
        if high_pri_count > 5:
            print(f"\n💡 Note: You have {high_pri_count} high-priority (P0/P1) tasks - consider if they're all truly urgent")
        
        # Task status overview
        print("\n## Task Status:")
        status_counts = Counter(task['status'] for task in active_tasks)
        status_map = {'n': 'Not Started', 's': 'In Progress', 'b': 'Blocked'}
        
        for status_code, status_name in status_map.items():
            count = status_counts.get(status_code, 0)
            if count > 0:
                print(f"- {status_name}: {count}")
                if status_code == 's':
                    started = [t for t in active_tasks if t['status'] == 's']
                    for task in started[:3]:
                        print(f"  → {task['title']}")
        
        # Category breakdown
        print("\n## Category Distribution:")
        category_counts = Counter(task['category'] for task in active_tasks)
        for category, count in category_counts.most_common():
            percentage = (count / len(active_tasks)) * 100 if active_tasks else 0
            print(f"- {category}: {count} ({percentage:.0f}%)")
        
        # Time-based insights
        current_hour = datetime.now().hour
        current_day = datetime.now().strftime('%A')
        
        print(f"\n## 💡 Time-Based Insights ({current_day}, {current_hour}:00):")
        
        if 9 <= current_hour < 12:
            outreach_available = [t for t in active_tasks if t['category'] == 'outreach' and t['status'] == 'n']
            if outreach_available:
                print(f"- Morning is ideal for outreach - you have {len(outreach_available)} outreach tasks")
        elif 14 <= current_hour < 17:
            deep_work = [t for t in active_tasks if t['category'] in ['technical', 'writing', 'research'] and t['status'] == 'n']
            if deep_work:
                print(f"- Afternoon deep work time - {len(deep_work)} technical/writing tasks available")
        elif current_hour >= 17:
            print("- Evening: Good time for planning tomorrow or quick admin tasks")
        
        if current_day == 'Friday':
            print("- It's Friday! Consider doing a weekly review")
        
        # High priority items needing attention
        print("\n## 🎯 Immediate Actions:")
        
        # P0/P1 not started
        high_pri_not_started = [t for t in active_tasks if t['priority'] in ['P0', 'P1'] and t['status'] == 'n']
        if high_pri_not_started:
            print(f"1. Start a high-priority task ({len(high_pri_not_started)} P0/P1 tasks waiting)")
            print(f"   → {high_pri_not_started[0]['title']}")
        
        # Blocked tasks
        blocked = [t for t in active_tasks if t['status'] == 'b']
        if blocked:
            print(f"2. Review {len(blocked)} blocked task(s) - might be unblocked now")
        
        # Aging tasks
        old_not_started = []
        for task in active_tasks:
            if task['status'] == 'n':
                try:
                    file_path = self.tasks_dir / task['filename']
                    age_days = (datetime.now() - datetime.fromtimestamp(file_path.stat().st_ctime)).days
                    if age_days > 7:
                        old_not_started.append((task, age_days))
                except:
                    pass
        
        if old_not_started:
            oldest = sorted(old_not_started, key=lambda x: x[1], reverse=True)[0]
            print(f"3. Address aging tasks - '{oldest[0]['title']}' is {oldest[1]} days old")
        
        # System health
        print("\n## 🔍 System Health:")
        
        # Check for missing CRM entries
        crm_names_in_tasks = set()
        for task in active_tasks:
            if task['category'] == 'outreach':
                title_words = task['title'].lower().split()
                for i, word in enumerate(title_words):
                    if word in ['with', 'to', 'contact']:
                        if i + 1 < len(title_words):
                            crm_names_in_tasks.add(title_words[i + 1].title())
        
        contacts = self.get_all_contacts()
        existing_names = set(c['name'].split()[0] for c in contacts if c.get('name'))
        missing_crm = crm_names_in_tasks - existing_names
        
        if missing_crm:
            print(f"- ⚠️ {len(missing_crm)} contacts mentioned in tasks but not in CRM: {', '.join(missing_crm)}")
        else:
            print("- ✓ CRM and tasks are in sync")
        
        # Done tasks ready for cleanup
        done_tasks = [t for t in all_tasks if t['status'] == 'd']
        if len(done_tasks) > 10:
            print(f"- ℹ️ {len(done_tasks)} completed tasks (run 'prune-tasks' to clean up)")
        
        # Quick stats
        print(f"\n## 📈 Quick Stats:")
        print(f"- Total active tasks: {len(active_tasks)}")
        print(f"- Total contacts in CRM: {len(contacts)}")
        
        if active_tasks:
            total_estimate = sum(t.get('estimated_time', 0) for t in active_tasks)
            print(f"- Total estimated time: {total_estimate} minutes ({total_estimate/60:.1f} hours)")
            
            p0p1_estimate = sum(t.get('estimated_time', 0) for t in active_tasks if t['priority'] in ['P0', 'P1'])
            if p0p1_estimate:
                print(f"- P0/P1 time commitment: {p0p1_estimate} minutes ({p0p1_estimate/60:.1f} hours)")
        
        # Backlog check
        backlog_file = self.base_dir / 'BACKLOG.md'
        if backlog_file.exists():
            with open(backlog_file, 'r') as f:
                content = f.read().strip()
                if content and content != 'all done!':
                    lines = len([l for l in content.split('\n') if l.strip() and l.strip().startswith('-')])
                    if lines > 0:
                        print(f"\n⚠️ BACKLOG.md has {lines} items to process!")

def main():
    parser = argparse.ArgumentParser(description='DirectoryClient - TODO System CLI Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    list_parser = subparsers.add_parser('list', help='List tasks, hiding completed by default')
    list_parser.add_argument('--category', help='Filter by category (comma-separated)')
    list_parser.add_argument('--priority', help='Filter by priority (comma-separated)')
    list_parser.add_argument('--status', help='Filter by status (comma-separated)')
    list_parser.add_argument('--include-done', action='store_true', help='Include completed tasks')
    
    prune_parser = subparsers.add_parser('prune-tasks', help='Delete completed tasks older than a specified time')
    prune_parser.add_argument('--days-old', type=int, default=30, help='Days old to be considered for pruning')

    update_parser = subparsers.add_parser('update-status', help='Update task status')
    update_parser.add_argument('task_file', help='Task filename')
    update_parser.add_argument('status', choices=['n', 's', 'b', 'd'], help='New status')
    
    start_parser = subparsers.add_parser('start', help='Mark task as started')
    start_parser.add_argument('task_file', help='Task filename')
    
    complete_parser = subparsers.add_parser('complete', help='Mark task as completed')
    complete_parser.add_argument('task_file', help='Task filename')
    
    subparsers.add_parser('summary', help='Show task summary statistics')
    subparsers.add_parser('check-limits', help='Check priority distribution and alert on high concentrations')
    
    crm_list_parser = subparsers.add_parser('crm-list', help='List CRM contacts')
    crm_list_parser.add_argument('--location', help='Filter by location')
    crm_list_parser.add_argument('--company', help='Filter by company')
    crm_list_parser.add_argument('--name', help='Filter by name')
    
    crm_add_parser = subparsers.add_parser('crm-add', help='Add new contact')
    crm_add_parser.add_argument('name', help='Contact name')
    crm_add_parser.add_argument('--email', help='Email address')
    crm_add_parser.add_argument('--company', help='Company name')
    crm_add_parser.add_argument('--location', help='Location')
    crm_add_parser.add_argument('--phone', help='Phone number')
    crm_add_parser.add_argument('--linkedin', help='LinkedIn URL')
    
    crm_update_parser = subparsers.add_parser('crm-update', help='Update contact field')
    crm_update_parser.add_argument('name', help='Contact name')
    crm_update_parser.add_argument('field', help='Field to update')
    crm_update_parser.add_argument('value', help='New value')
    
    crm_search_parser = subparsers.add_parser('crm-search', help='Search contacts')
    crm_search_parser.add_argument('query', help='Search query')
    
    subparsers.add_parser('crm-summary', help='Show CRM summary statistics')
    
    subparsers.add_parser('double-check', help='Double-check system integrity and recent work')
    subparsers.add_parser('anticipate', help='Anticipate next questions/tasks and suggest actions')
    subparsers.add_parser('status', help='Show comprehensive system status with actionable insights')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    client = DirectoryClient()
    
    if args.command == 'list':
        client.list_tasks(args.category, args.priority, args.status, args.include_done)
    elif args.command == 'prune-tasks':
        client.prune_old_done_tasks(args.days_old)
    elif args.command == 'update-status':
        client.update_task_status(args.task_file, args.status)
    elif args.command == 'start':
        client.start_task(args.task_file)
    elif args.command == 'complete':
        client.complete_task(args.task_file)
    elif args.command == 'summary':
        client.show_summary()
    elif args.command == 'check-limits':
        client.check_priority_limits()
    elif args.command == 'crm-list':
        client.list_contacts(args.location, args.company, args.name)
    elif args.command == 'crm-add':
        client.add_contact(args.name, args.email, args.company, args.location, args.phone, args.linkedin)
    elif args.command == 'crm-update':
        client.update_contact_field(args.name, args.field, args.value)
    elif args.command == 'crm-search':
        client.search_contacts(args.query)
    elif args.command == 'crm-summary':
        client.crm_summary()
    elif args.command == 'double-check':
        client.double_check_work()
    elif args.command == 'anticipate':
        client.anticipate_next()
    elif args.command == 'status':
        client.status()

if __name__ == '__main__':
    main()
