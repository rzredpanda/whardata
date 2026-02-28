"""
PDF Report Agent — WHL 2025
Phase 6: Compile comprehensive competition report
"""
import os, datetime, glob
import pandas as pd
import numpy as np

LOG_FILE  = r"c:\Users\ryanz\Downloads\whardata\scratch\agent_log.txt"
OUT_DIR   = r"c:\Users\ryanz\Downloads\whardata\outputs"
RANK_DIR  = r"c:\Users\ryanz\Downloads\whardata\outputs\rankings"
DISP_DIR  = r"c:\Users\ryanz\Downloads\whardata\outputs\disparity"
EDA_DIR   = r"c:\Users\ryanz\Downloads\whardata\outputs\eda_tables"

REPORT_MD  = os.path.join(OUT_DIR, "WHL_Competition_Report.md")
REPORT_PDF = os.path.join(OUT_DIR, "WHL_Competition_Report.pdf")

def log(msg):
    ts = datetime.datetime.now().isoformat()
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[REPORT] {ts} | {msg}\n")
    print(msg)

def safe_read(path, **kwargs):
    try:
        return pd.read_csv(path, **kwargs)
    except Exception as e:
        log(f"  Could not read {path}: {e}")
        return pd.DataFrame()

def fmt_table(df, max_rows=35):
    """Format a DataFrame as a markdown table."""
    return df.head(max_rows).to_markdown(index=False) if not df.empty else "_No data available._"

def main():
    log("=== PDF Report Agent STARTED ===")
    lines = []
    def L(x=""): lines.append(str(x))
    
    L("# WHL 2026 — Wharton High School Data Science Competition")
    L("## World Hockey League Performance Analysis Report")
    L(f"**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}  |  **Prepared by:** Multi-Agent Analytics Pipeline")
    L()
    L("---")
    L()

    # ── SECTION 1: Data Overview & EDA ─────────────────────────────────────────
    L("# Section 1: Data Overview & EDA Findings")
    L()
    L("## 1.1 Dataset Description")
    L("""
The WHL 2025 dataset contains **25,827 rows** representing line-pairing matchup records across
one fictional season of the World Hockey League. There are **1,312 games** across **32 teams**,
with each game containing approximately 18–20 rows capturing different offensive line / defensive
pairing combinations on ice simultaneously.

**Key structural facts:**
- Each row is a line-level matchup summary (not a full game)
- `toi` = time on ice in seconds for that specific pairing
- `home_off_line` / `away_off_line`: `first_off`, `second_off`, `PP_up`, `PP_kill_dwn`, `empty_net_line`
- All analysis filters to `first_off` + `second_off` for even-strength work; PP rows analyzed separately

**Important confounders addressed:**
1. **TOI differences** — all rates computed per 60 minutes (×3600/toi) rather than raw totals
2. **Defensive matchup quality** — Method 3 (disparity) explicitly adjusts for opponent defensive strength
""")
    L()
    
    # EDA tables
    eda_summary = safe_read(os.path.join(EDA_DIR, "numeric_summary.csv"))
    L("## 1.2 Key Numeric Statistics")
    L(fmt_table(eda_summary))
    L()
    
    # Home advantage
    game_eda = safe_read(os.path.join(EDA_DIR, "game_level_eda.csv"))
    if not game_eda.empty:
        hw_rate = game_eda['home_win'].mean()
        ot_rate = game_eda['went_ot'].mean()
        L("## 1.3 Home Advantage")
        L(f"- **Overall home win rate:** {hw_rate:.3f} ({hw_rate*100:.1f}%)")
        L(f"- **OT/SO rate:** {ot_rate:.3f} ({ot_rate*100:.1f}%)")
        reg = game_eda[game_eda['went_ot']==0]
        ot  = game_eda[game_eda['went_ot']==1]
        L(f"- **Regulation home win rate:** {reg['home_win'].mean():.3f}")
        L(f"- **OT/SO home win rate:** {ot['home_win'].mean():.3f}")
    L()
    
    # EDA report
    eda_report_path = os.path.join(OUT_DIR, "eda_report.md")
    if os.path.exists(eda_report_path):
        with open(eda_report_path, encoding='utf-8') as f:
            eda_content = f.read()
        L("## 1.4 Full EDA Findings")
        L(eda_content[:8000])  # Truncate for brevity; full report at eda_report.md
        L()
    
    L("---")
    L()

    # ── SECTION 2: Power Rankings ───────────────────────────────────────────────
    L("# Section 2: Phase 1a — Team Power Rankings")
    L()
    
    model_meta = {
        'model_01_points_standings':   ("Model 1: Raw Points Standings",   "Standard NHL-style: 2pts win, 1pt OT loss. Baseline model."),
        'model_02_xgd60_es':           ("Model 2: xG Differential/60 (ES)","Even-strength xGF/60 minus xGA/60. Adjusts for TOI."),
        'model_03_pythagorean':        ("Model 3: Pythagorean Expectation","xGF^k / (xGF^k + xGA^k). Optimal k tuned empirically."),
        'model_04_elo_ratings':        ("Model 4: Elo Rating System",      "K=20, 1500 base, +100 home advantage. Chronological game processing."),
        'model_05_colley_matrix':      ("Model 5: Colley Matrix",          "Linear system solving for strength-of-schedule-adjusted ratings."),
        'model_06_bradley_terry':      ("Model 6: Bradley-Terry Pairwise", "MLE pairwise model: P(i beats j) = s_i/(s_i+s_j)."),
        'model_07_composite_weighted': ("Model 7: Composite Weighted Score","Z-score weighted sum: xGD(0.35)+GD(0.15)+GSAx(0.20)+PP(0.15)+PK(0.15)."),
        'model_08_logistic_regression':("Model 8: Logistic Regression",    "LR on xGF/60, xGA/60 features. Team strength from coefficients."),
        'model_09_random_forest':      ("Model 9: Random Forest",          "RF with permutation importance. Teams ranked by weighted feature score."),
        'model_10_monte_carlo':        ("Model 10: Monte Carlo Simulation","Poisson xGF sampling, 1,000 season simulations. Mean±SD points shown."),
    }
    
    all_rankings = {}
    for fname, (title, desc) in model_meta.items():
        fp = os.path.join(RANK_DIR, fname + ".csv")
        if os.path.exists(fp):
            mdf = safe_read(fp)
            all_rankings[fname] = mdf
            L(f"## 2.{list(model_meta.keys()).index(fname)+1} {title}")
            L(f"_{desc}_")
            L()
            L(fmt_table(mdf.head(32)))
            L()
    
    # Side-by-side comparison
    L("## 2.11 Side-by-Side Ranking Comparison (All 10 Models)")
    cons_df = safe_read(os.path.join(RANK_DIR, "consensus_rankings.csv"))
    if not cons_df.empty:
        L(fmt_table(cons_df.head(32)))
    L()
    
    L("## 2.12 Recommended Final Power Ranking")
    if not cons_df.empty:
        top32 = cons_df.sort_values('mean_rank')[['team','mean_rank','rank_variance']].head(32)
        top32['recommended_rank'] = range(1, len(top32)+1)
        L("The **consensus ranking** (mean rank across all 10 models) is our recommended final ranking.")
        L("Teams with low rank variance are robustly ranked; those with high variance should be scrutinized.")
        L()
        L(fmt_table(top32))
    L()
    L("---")
    L()

    # ── SECTION 3: Win Probabilities ───────────────────────────────────────────
    L("# Section 3: Phase 1a — Win Probabilities (Round 1 Matchups)")
    L()
    wp_df = safe_read(os.path.join(OUT_DIR, "win_probabilities.csv"))
    if not wp_df.empty:
        L("## 3.1 All 16 Matchup Probabilities (Five Methods + Ensemble)")
        L(fmt_table(wp_df))
        L()
        flagged = wp_df[wp_df.get('flag_disagree','') == 'YES'] if 'flag_disagree' in wp_df.columns else pd.DataFrame()
        if not flagged.empty:
            L(f"### ⚠️ {len(flagged)} Matchups with >10pp Model Disagreement (warrant extra scrutiny):")
            L(fmt_table(flagged))
    L()
    
    wp_val = safe_read(os.path.join(OUT_DIR, "win_prob_validation.csv"))
    if not wp_val.empty:
        L("## 3.2 Win Probability Model Calibration (LR)")
        L(fmt_table(wp_val.T.reset_index().rename(columns={'index':'metric',0:'value'})))
    L()
    L("---")
    L()

    # ── SECTION 4: Line Disparity ───────────────────────────────────────────────
    L("# Section 4: Phase 1b — Line Disparity Analysis")
    L()
    
    disp_meta = {
        'method_01_raw_xg_ratio':          "Raw xG ratio (sum first_off / sum second_off). No adjustments.",
        'method_02_xg_per60_ratio':        "xG/60 ratio. Fixes TOI confounding.",
        'method_03_matchup_adj_xg60':      "Matchup-adjusted xG/60. Scales for opponent defensive quality.",
        'method_04_goals_per60_ratio':     "Goals/60 ratio. Noisier but direct.",
        'method_05_shots_per60_ratio':     "Shots/60 ratio. Volume-based measure.",
        'method_06_xg_share_proportion':   "xG share (distance from 50/50 balance).",
        'method_07_zscore_gap':            "Z-score gap. League-standardized first vs second line xG/60.",
        'method_08_regression_line_effect':"OLS regression controlling for team and defensive quality.",
        'method_09_toi_weighted_quality':  "TOI-weighted average xG/60 per line.",
        'method_10_bootstrap_ci_ratio':    "Bootstrap CI (n=1,000). Reports mean ± 95% CI.",
    }
    
    for i, (fname, desc) in enumerate(disp_meta.items(), 1):
        fp = os.path.join(DISP_DIR, fname + ".csv")
        if os.path.exists(fp):
            ddf = safe_read(fp)
            L(f"## 4.{i} Method {i}: {desc}")
            L(fmt_table(ddf.head(32)))
            L()
    
    # Consensus Top 10
    top10 = safe_read(os.path.join(DISP_DIR, "top10_disparity.csv"))
    L("## 4.11 Consensus Top 10 Teams by Line Disparity")
    L("**This is the final Phase 1b submission answer.**")
    L()
    if not top10.empty:
        L(fmt_table(top10[['consensus_rank','team','mean_rank','rank_variance']]))
    L()
    
    # Method correlation
    disp_corr = safe_read(os.path.join(OUT_DIR, "disparity_method_correlation.csv"))
    L("## 4.12 Method Correlation Matrix (Spearman ρ)")
    L(fmt_table(disp_corr))
    L()
    L("---")
    L()

    # ── SECTION 5: Validation Summary ──────────────────────────────────────────
    L("# Section 5: Validation Summary")
    L()
    val_df = safe_read(os.path.join(OUT_DIR, "validation_scores.csv"))
    if not val_df.empty:
        L("## 5.1 Ranking Model Validation Metrics")
        L(fmt_table(val_df))
        L()
    
    agree_df = safe_read(os.path.join(OUT_DIR, "model_agreement_matrix.csv"), index_col=0)
    L("## 5.2 Model Agreement Matrix (% games where models agree on predicted winner)")
    L(fmt_table(agree_df.reset_index()))
    L()
    
    elo_cal = safe_read(os.path.join(OUT_DIR, "elo_calibration_curve.csv"))
    L("## 5.3 Original Validation 1: Elo Calibration Curve")
    L("Checks whether Elo-predicted win probabilities match actual win rates when binned by decile.")
    L(fmt_table(elo_cal))
    L()
    
    ci_overlap = safe_read(os.path.join(OUT_DIR, "ranking_ci_overlap.csv"))
    L("## 5.4 Original Validation 2: Bootstrap CI Overlap for Adjacent Rankings")
    L("Flags whether adjacent-ranked teams are statistically distinguishable via 95% bootstrap CIs on xGD/60.")
    L(fmt_table(ci_overlap.head(32)))
    L()
    
    L("## 5.5 Baseline Comparisons")
    if not wp_val.empty:
        row = wp_val.iloc[0]
        L(f"| Baseline | Accuracy |")
        L(f"|----------|----------|")
        L(f"| Always pick home team | {row.get('baseline_always_home',0):.4f} |")
        L(f"| Always pick higher-points team | {row.get('baseline_higher_pts',0):.4f} |")
        L(f"| Always pick higher xGD/60 team | {row.get('baseline_higher_xgd',0):.4f} |")
        L(f"| **Logistic Regression (our model)** | **{row.get('in_sample_accuracy',0):.4f}** |")
        L(f"| LR 10-fold CV accuracy | {row.get('cv10_acc_mean',0):.4f} ± {row.get('cv10_acc_std',0):.4f} |")
    L()
    L("---")
    L()

    # ── SECTION 6: Methodology Narrative ───────────────────────────────────────
    L("# Section 6: Methodology Narrative (Phase 1d)")
    L()
    L("## 6.1 Data Cleaning & Preparation (~75 words)")
    L("""
The WHL 2025 dataset (25,827 rows, 26 columns) was loaded and audited for missing values — none
were found. Game-level aggregates were built by summing all row-level statistics within each
`game_id`. Even-strength analysis strictly filtered to `home_off_line ∈ {first_off, second_off}`,
while power play and penalty kill situations were handled separately. All rate statistics were
normalized to per-60-minute rates using the formula `stat × (3600 / toi)` to eliminate
confounding from unequal time-on-ice across line types.
""")
    L()
    
    L("## 6.2 Variable Creation (~75 words)")
    L("""
Key derived variables include: **xGD/60** (xGF/60 − xGA/60, even-strength), **GSAx** (Goals
Saved Above Expected: xGA − actual GA per goalie), **Pythagorean win%** (xGF^k / (xGF^k + xGA^k),
k tuned empirically), **Elo ratings** (initialized at 1500, K=20, +100 home advantage), and
**line disparity metrics** (10 variants from raw xG ratio to bootstrap-adjusted xG/60 ratios).
Matchup-adjusted xG scales raw xG by the ratio of league-average defensive quality to the
specific opponent's defensive quality.
""")
    L()
    
    L("## 6.3 Tools Used (~50 words)")
    L("""
All analysis was conducted in Python using `pandas` (data manipulation), `numpy` (numerical
computation), `scipy` (statistical tests, optimization), `scikit-learn` (logistic regression,
random forest, cross-validation), and `statsmodels` (OLS regression). A custom multi-agent
architecture orchestrated parallel execution of EDA, aggregation, modeling, validation, and
report generation pipelines.
""")
    L()
    
    L("## 6.4 Statistical Methods (~100 words)")
    L("""
Ten power ranking models were built ranging from simple point totals (Model 1) to sophisticated
approaches: **Elo ratings** (sequential Bayesian updating), **Colley matrix** (strength-of-schedule
via linear systems), **Bradley-Terry** (maximum likelihood pairwise competition model), **Pythagorean
expectation** (empirically tuned exponent), **composite weighted z-scores**, **logistic regression**,
**random forest with permutation importance**, and **Monte Carlo simulation** (1,000 full-season
replications). Win probabilities used five independent methods and ensemble averaging. Line disparity
employed 10 complementary techniques including bootstrap confidence intervals and regression control
for opponent defensive quality.
""")
    L()
    
    L("## 6.5 Model Assessment (~75 words)")
    L("""
Every ranking model was evaluated using seven metrics: Kendall's τ and Spearman ρ (rank correlation
vs points-based ground truth), Top-8 hit rate (proportion of true top-8 in model's top-8), Brier
score and log-loss (probability calibration), rank inversion rate (head-to-head prediction accuracy),
and consensus ρ (agreement with mean ranking). The win probability model was further validated via
10-fold cross-validation and leave-one-team-out validation, and compared against three naive baselines.
""")
    L()
    
    L("## 6.6 AI Tool Usage (~50 words)")
    L("""
All code, analysis, and report generation were produced by an AI multi-agent pipeline (Antigravity /
Google DeepMind). The Orchestrator spawned specialized subagents for EDA, game aggregation, ten
ranking models, five win probability models, ten disparity methods, validation, and report compilation.
Human oversight validated the pipeline architecture; all data analysis and statistical modeling was
AI-generated.
""")
    L()
    L("---")
    L()
    
    # ── Submission-ready Summary ─────────────────────────────────────────────
    L("# 🏆 Submission-Ready Summary")
    L()
    L("## Phase 1a: Recommended Power Ranking (Consensus)")
    if not cons_df.empty:
        final_rank = cons_df.sort_values('mean_rank')[['team','mean_rank']].reset_index(drop=True)
        final_rank['rank'] = range(1, len(final_rank)+1)
        L(fmt_table(final_rank[['rank','team','mean_rank']].head(32)))
    L()
    
    L("## Phase 1a: Win Probabilities for Round 1 Matchups")
    if not wp_df.empty:
        L(fmt_table(wp_df[['game','home_team','away_team','p_ensemble']].rename(
            columns={'p_ensemble':'home_win_prob'})))
    L()
    
    L("## Phase 1b: Top 10 Teams by First-to-Second Line Disparity")
    if not top10.empty:
        sub_top10 = top10[['consensus_rank','team','mean_rank']].rename(
            columns={'consensus_rank':'rank','mean_rank':'avg_disparity_rank'})
        L(fmt_table(sub_top10))
    L()
    L("---")
    L("_End of Report_")
    
    # Save Markdown report
    with open(REPORT_MD, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    log(f"Markdown report saved: {REPORT_MD}")
    
    # Try to convert to PDF via reportlab or weasyprint
    pdf_generated = False
    try:
        import subprocess
        # Try pandoc first
        result = subprocess.run(['pandoc', REPORT_MD, '-o', REPORT_PDF, '--pdf-engine=xelatex',
                                 '-V', 'geometry:margin=1in', '-V', 'fontsize=11pt'],
                                capture_output=True, timeout=120)
        if result.returncode == 0:
            pdf_generated = True
            log(f"PDF generated via pandoc: {REPORT_PDF}")
        else:
            log(f"Pandoc failed: {result.stderr.decode()[:300]}")
    except Exception as e:
        log(f"Pandoc not available: {e}")
    
    if not pdf_generated:
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
            
            doc = SimpleDocTemplate(REPORT_PDF, pagesize=letter,
                                    leftMargin=72, rightMargin=72, topMargin=72, bottomMargin=72)
            styles = getSampleStyleSheet()
            story = []
            
            for line in lines:
                if line.startswith("# ") and not line.startswith("## "):
                    story.append(Paragraph(line[2:], styles['Title']))
                elif line.startswith("## "):
                    story.append(Spacer(1,6))
                    story.append(Paragraph(line[3:], styles['Heading2']))
                elif line.startswith("### "):
                    story.append(Paragraph(line[4:], styles['Heading3']))
                elif line.strip():
                    # Strip markdown formatting for reportlab
                    clean = line.replace('**','').replace('_','').replace('`','')
                    if len(clean) < 5000:
                        story.append(Paragraph(clean, styles['Normal']))
                story.append(Spacer(1,3))
            
            doc.build(story)
            pdf_generated = True
            log(f"PDF generated via reportlab: {REPORT_PDF}")
        except Exception as e:
            log(f"reportlab failed: {e}")
    
    if not pdf_generated:
        log("PDF generation failed — Markdown report is available at WHL_Competition_Report.md")
    
    log("=== PDF Report Agent COMPLETED ===")

if __name__ == '__main__':
    main()
