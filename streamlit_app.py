"""Streamlit Interactive Threat Intelligence & Autonomous Remediation Frontend (Root Entrypoint)
Course: 23CSE528 NoSQL Databases using MongoDB | Student: Ayush Yadav (24BTLCL003)
Streamlit Community Cloud and Local Execution Entrypoint
"""

import os
import sys

# Add llm directory to Python module path
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
LLM_DIR = os.path.join(CUR_DIR, "llm")
if os.path.exists(LLM_DIR) and LLM_DIR not in sys.path:
    sys.path.insert(0, LLM_DIR)

# Load and execute main application
with open(os.path.join(LLM_DIR, "streamlit_app.py"), "r", encoding="utf-8") as f:
    code = f.read()

exec(code, globals())
