import docx

doc_path = r"C:\Users\AYUSH YADAV\.gemini\antigravity\brain\7681611c-aa82-48d4-9cf3-85926f5db335\.user_uploaded\media_1794943820531_d292f9d5.docx"
doc = docx.Document(doc_path)
for i, p in enumerate(doc.paragraphs):
    print(f"P[{i}]: {p.text}")

for t_idx, table in enumerate(doc.tables):
    print(f"\n--- TABLE {t_idx} ---")
    for r_idx, row in enumerate(table.rows):
        for c_idx, cell in enumerate(row.cells):
            print(f"  Cell [{r_idx}, {c_idx}]: {cell.text.strip()}")
