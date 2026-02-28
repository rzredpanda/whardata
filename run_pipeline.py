"""
Pipeline Runner — runs all WHL scripts in the correct order
"""
import subprocess, sys, os, time, datetime

os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUTF8'] = '1'

BASE = r"c:\Users\ryanz\Downloads\whardata"
LOG  = os.path.join(BASE, "scratch", "pipeline_run.log")

def run_step(script, label):
    print(f"\n{'='*60}")
    print(f"RUNNING: {label}")
    print(f"{'='*60}")
    t0 = datetime.datetime.now()
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONUTF8'] = '1'
    result = subprocess.run(
        [sys.executable, '-X', 'utf8', os.path.join(BASE, 'scripts', script)],
        capture_output=False,
        env=env,
        cwd=BASE
    )
    elapsed = (datetime.datetime.now() - t0).total_seconds()
    status = "✓ OK" if result.returncode == 0 else f"✗ FAILED (code {result.returncode})"
    print(f"\n[{label}] {status} — {elapsed:.1f}s")
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.datetime.now().isoformat()} | {label} | {status} | {elapsed:.1f}s\n")
    return result.returncode == 0

steps = [
    ("00_eda.py",           "Phase 0: EDA"),
    ("01_game_aggregation.py", "Phase 1: Game Aggregation"),
    ("02_ranking_models.py",   "Phase 2: All 10 Ranking Models"),
    ("03_win_probability.py",  "Phase 3: Win Probability Models"),
    ("04_line_disparity.py",   "Phase 4: Line Disparity Analysis"),
    ("05_validation.py",       "Phase 5: Validation"),
    ("06_pdf_report.py",       "Phase 6: PDF Report"),
]

all_ok = True
for script, label in steps:
    ok = run_step(script, label)
    if not ok:
        print(f"\n⚠️  {label} failed. Continuing to next step anyway...")
        all_ok = False

print("\n" + "="*60)
print("PIPELINE COMPLETE" if all_ok else "PIPELINE DONE (with some errors — check logs)")
print("="*60)
print(f"Log: {LOG}")
