import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_activity_submission_docx(
    activity_num: int,
    activity_data: dict,
    output_docx_path: str
):
    """
    Creates a formatted submission docx matching MongoDB_Activity_4_Submission.docx
    for student Ayush Yadav (USN: 24BTLCL003).
    """
    doc = docx.Document()

    # Set page margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    def add_meta_line(text, bold=True, size=12):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.bold = bold
        run.font.name = "Times New Roman"
        run.font.size = Pt(size)
        return p

    def add_section_header(text, size=14):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(size)
        return p

    def add_label_and_text(label, text, bold_label=True):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r1 = p.add_run(label + " ")
        r1.bold = bold_label
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(12)
        r2 = p.add_run(text)
        r2.bold = False
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(12)
        return p

    def add_task_bullet(task_text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(task_text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11.5)
        return p

    def add_code_block(code_text):
        for line in code_text.splitlines():
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(line if line else " ")
            run.font.name = "Consolas"
            run.font.size = Pt(9.5)

    def add_image_safely(img_path, width=Inches(6.2)):
        if os.path.exists(img_path):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run()
            run.add_picture(img_path, width=width)

    # 1. Header Information
    add_meta_line("Name: Ayush Yadav", bold=True, size=12)
    add_meta_line("USN: 24BTLCL003", bold=True, size=12)
    add_meta_line("Class: AIML - B", bold=True, size=12)
    
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(10)
    title_p.paragraph_format.space_after = Pt(4)
    r_subj = title_p.add_run("NoSQL Using MongoDB\n")
    r_subj.bold = True
    r_subj.font.name = "Times New Roman"
    r_subj.font.size = Pt(15)

    r_exp = title_p.add_run(f"Experiment – Activity {activity_num}")
    r_exp.bold = True
    r_exp.font.name = "Times New Roman"
    r_exp.font.size = Pt(14)

    # Sections: Act_1, Act_1_Try, Act_2, Act_2_Try
    sections = [
        ("act_1", f"ACTIVITY {activity_num}.1 — {activity_data['act_1']['title'].upper()}"),
        ("act_1_try", f"Activity {activity_num}.1 – Try It Yourself:"),
        ("act_2", f"ACTIVITY {activity_num}.2 — {activity_data['act_2']['title'].upper()}"),
        ("act_2_try", f"ACTIVITY {activity_num}.2 — TRY IT YOURSELF"),
    ]

    for key, header_title in sections:
        sec = activity_data[key]
        add_section_header(header_title, size=13.5 if "TRY IT" in header_title.upper() else 14)
        add_label_and_text("Objective:", sec["objective"])

        if "tasks" in sec and sec["tasks"]:
            p_tasks = doc.add_paragraph()
            p_tasks.paragraph_format.space_before = Pt(4)
            p_tasks.paragraph_format.space_after = Pt(2)
            r = p_tasks.add_run("Tasks:")
            r.bold = True
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)
            for t in sec["tasks"]:
                add_task_bullet(t)

        # Output label & screenshots
        p_out = doc.add_paragraph()
        p_out.paragraph_format.space_before = Pt(6)
        p_out.paragraph_format.space_after = Pt(4)
        r_out = p_out.add_run("Output:")
        r_out.bold = True
        r_out.font.name = "Times New Roman"
        r_out.font.size = Pt(12)

        for img in sec.get("images", []):
            add_image_safely(img)

        # Python script
        p_py = doc.add_paragraph()
        p_py.paragraph_format.space_before = Pt(8)
        p_py.paragraph_format.space_after = Pt(4)
        r_py = p_py.add_run("Python Script:")
        r_py.bold = True
        r_py.font.name = "Times New Roman"
        r_py.font.size = Pt(12)

        add_code_block(sec["code"])

    os.makedirs(os.path.dirname(os.path.abspath(output_docx_path)), exist_ok=True)
    doc.save(output_docx_path)
    print(f"[OK] Saved {output_docx_path}")
