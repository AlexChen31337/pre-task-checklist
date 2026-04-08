#!/usr/bin/env python3
"""
Pre-task verification utility
Checks memory, reference files, and critical details before starting tasks
"""

import sys
import os
import subprocess
from pathlib import Path

# Paths
WORKSPACE = Path.home() / ".openclaw" / "workspace"
TOOLS_MD = WORKSPACE / "TOOLS.md"
AGENTS_MD = WORKSPACE / "AGENTS.md"
SOUL_MD = WORKSPACE / "SOUL.md"
MEMORY_MD = WORKSPACE / "MEMORY.md"

def search_files(query, files):
    """Search multiple files for a query"""
    results = {}
    for file_path in files:
        if file_path.exists():
            try:
                content = file_path.read_text()
                lines = content.split('\n')
                matches = [f"  {i+1}: {line}" 
                          for i, line in enumerate(lines) 
                          if query.lower() in line.lower()]
                if matches:
                    results[file_path.name] = matches[:10]  # Max 10 matches
            except Exception as e:
                results[file_path.name] = [f"  Error: {e}"]
    return results

def verify_ip(hostname):
    """Verify an IP address by attempting connection"""
    print(f"🔍 Verifying IP: {hostname}")
    try:
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=5", hostname, "echo", "connected"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(f"✅ {hostname} - Connection successful")
            return True
        else:
            print(f"❌ {hostname} - Connection failed")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {hostname} - Verification error: {e}")
        return False

def verify_path(path):
    """Verify a file path exists"""
    print(f"🔍 Verifying path: {path}")
    if os.path.exists(path):
        print(f"✅ {path} - Exists")
        return True
    else:
        print(f"❌ {path} - Not found")
        return False

def quick_verify(query):
    """Quick verification of a query"""
    print(f"\n🔍 Quick verify: {query}\n")
    
    # Search reference files
    files = [TOOLS_MD, AGENTS_MD, SOUL_MD, MEMORY_MD]
    results = search_files(query, files)
    
    if results:
        print("📖 Found in reference files:")
        for filename, matches in results.items():
            print(f"\n{filename}:")
            for match in matches:
                print(match)
    else:
        print("⚠️  Not found in reference files")
    
    print("\n✅ Verification complete\n")

def checklist():
    """Run full pre-task checklist"""
    print("\n=== 📋 PRE-TASK CHECKLIST ===\n")
    
    # 1. Task description
    print("1️⃣  What task are you about to start?")
    task = input("> ").strip()
    print(f"   → Task: {task}\n")
    
    # 2. Memory search
    print("2️⃣  Search memory for similar tasks...")
    if task:
        quick_verify(task)
    
    # 3. Verify critical details
    print("3️⃣  Verify critical details? (y/n)")
    choice = input("> ").strip().lower()
    if choice == 'y':
        print("   What to verify? (ip/path/other)")
        verify_type = input("> ").strip().lower()
        value = input("   Enter value: ").strip()
        
        if verify_type == 'ip':
            verify_ip(value)
        elif verify_type == 'path':
            verify_path(value)
        else:
            quick_verify(value)
    
    # 4. Check rules
    print("4️⃣  Check rules in AGENTS.md/SOUL.md? (y/n)")
    choice = input("> ").strip().lower()
    if choice == 'y':
        print("\n📖 Key rules from AGENTS.md:")
        if AGENTS_MD.exists():
            content = AGENTS_MD.read_text()
            for line in content.split('\n')[:30]:
                if any(keyword in line.lower() for keyword in ['rule', 'must', 'never', 'required']):
                    print(f"  {line}")
        
        print("\n📖 Key rules from SOUL.md:")
        if SOUL_MD.exists():
            content = SOUL_MD.read_text()
            for line in content.split('\n')[:30]:
                if any(keyword in line.lower() for keyword in ['rule', 'must', 'never', 'required']):
                    print(f"  {line}")
    
    # 5. Confirmation
    print("\n=== ✅ CHECKLIST COMPLETE ===")
    print("Proceed with task? (y/n)")
    choice = input("> ").strip().lower()
    if choice == 'y':
        print("✅ Proceeding with verified context\n")
        return 0
    else:
        print("❌ Task aborted - need more verification\n")
        return 1

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "verify":
            if len(sys.argv) > 2:
                quick_verify(sys.argv[2])
        elif sys.argv[1] == "ip":
            if len(sys.argv) > 2:
                verify_ip(sys.argv[2])
        elif sys.argv[1] == "path":
            if len(sys.argv) > 2:
                verify_path(sys.argv[2])
    else:
        checklist()
