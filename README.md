# NoSQL Databases using MongoDB (23CSE528)
## Complete Lab Curriculum (Activities 1–18) & Threat Intelligence AI Capstone

**Institution:** School of CSE, Faculty of Engineering and Technology, JAIN (Deemed-to-be University), Bengaluru  
**Student Name:** Ayush Yadav  
**USN:** 24BTLCL003  
**Programme:** B.Tech — Computer Science & Engineering (AIML) - 4th Semester (Section B)  
**Faculty Guide:** Prof. Sujeet S Jagtap  

---

## 📂 Repository Navigation

This repository contains two major components:

1. **Master Lab Experiments Report (Activities 1 to 18)**:
   - Word Document (`.docx`): [24BTLCL003_Ayush_Yadav_MongoDB_Complete_Lab_Report_1_to_18.docx](file:///d:/mangoDB%20and%20no%20sql/24BTLCL003_Ayush_Yadav_MongoDB_Complete_Lab_Report_1_to_18.docx)
   - Markdown Document (`.md`): [24BTLCL003_Ayush_Yadav_MongoDB_Complete_Lab_Report_1_to_18.md](file:///d:/mangoDB%20and%20no%20sql/24BTLCL003_Ayush_Yadav_MongoDB_Complete_Lab_Report_1_to_18.md)
   - Individual Activity Submission Packages: `24BTLCL003_MongoDB_Activity_5_Submission` through `18_Submission` and `Appendix_A_Submission`.

2. **LLM/SLM Cyber Threat Intelligence & Autonomous Remediation Platform**:
   - Location: [llm/](file:///d:/mangoDB%20and%20no%20sql/llm)
   - Presentation Guide for Lecturer: [llm/presentation.md](file:///d:/mangoDB%20and%20no%20sql/llm/presentation.md)
   - Step-by-Step Run Guide: [llm/HOW_TO_RUN.md](file:///d:/mangoDB%20and%20no%20sql/llm/HOW_TO_RUN.md)
   - Full Documentation: [llm/README.md](file:///d:/mangoDB%20and%20no%20sql/llm/README.md)

---

## ⚡ How to Run the Threat Intelligence AI Platform

### Option 1: Fast Interactive Console Test (Zero Setup)
```powershell
cd "d:\mangoDB and no sql\llm"
python quick_test.py
```
Provides an interactive menu to query AI, audit machine vulnerabilities, mitigate threats via ACID transactions, and inspect MongoDB audit logs.

### Option 2: Full Web Browser GUI (Streamlit + FastAPI)
In Terminal 1 (Backend API):
```powershell
cd "d:\mangoDB and no sql\llm"
uvicorn threat_intel_api:app --reload --port 8000
```

In Terminal 2 (Frontend Dashboard):
```powershell
cd "d:\mangoDB and no sql\llm"
streamlit run streamlit_app.py --server.port 8501
```
Open your browser to: **`http://localhost:8501`**

### Option 3: Automated 8-Phase Benchmark
```powershell
cd "d:\mangoDB and no sql\llm"
python run_demo.py
```
Validates all 18 curriculum exercises in sequence in under 5 seconds.
