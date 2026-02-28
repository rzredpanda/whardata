"""Patch all scripts to use UTF-8 encoding in file opens"""
import os

scripts = [
    r'scripts\01_game_aggregation.py',
    r'scripts\02_ranking_models.py',
    r'scripts\03_win_probability.py',
    r'scripts\04_line_disparity.py',
    r'scripts\05_validation.py',
    r'scripts\06_pdf_report.py',
]

patches = [
    ("with open(LOG_FILE, 'a') as f:", "with open(LOG_FILE, 'a', encoding='utf-8') as f:"),
    ("with open(eda_report_path) as f:", "with open(eda_report_path, encoding='utf-8') as f:"),
]

for s in scripts:
    with open(s, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in patches:
        content = content.replace(old, new)
    with open(s, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Patched: {s}')

print('All scripts patched for UTF-8 encoding.')
