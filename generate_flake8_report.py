#!/usr/bin/env python3
"""
Script to generate flake8 HTML report for the chess tournament application.
"""

import subprocess
import sys
import os

def main():
    """Generate flake8 HTML report."""
    print("Generating flake8 HTML report...")
    
    try:
        # Run flake8 with HTML output
        cmd = [
            sys.executable, "-m", "flake8",
            "--format=html",
            "--htmldir=flake8_report", 
            "--max-line-length=119",
            "--exclude=venv,__pycache__,.git",
            "."
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ flake8 HTML report generated successfully!")
            print("📁 Report saved to: flake8_report/index.html")
            print("🌐 Open flake8_report/index.html in your browser to view the report")
        else:
            print("⚠️  flake8 found some issues:")
            print(result.stdout)
            print(result.stderr)
            print("📁 HTML report still generated at: flake8_report/index.html")
            
    except Exception as e:
        print(f"❌ Error generating flake8 report: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
