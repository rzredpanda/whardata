"""
Extra Visuals Agent — WHL 2025 Phase 8
Generates additional charts to enhance the final report package.
"""
import os, datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

LOG_FILE = r"c:\Users\ryanz\Downloads\whardata\scratch\agent_log.txt"
OUT_DIR  = r"c:\Users\ryanz\Downloads\whardata\outputs"
PLOT_DIR = r"c:\Users\ryanz\Downloads\whardata\outputs\plots"
RANK_DIR = r"c:\Users\ryanz\Downloads\whardata\outputs\rankings"
VAL_DIR  = r"c:\Users\ryanz\Downloads\whardata\outputs\validation"
EDA_DIR  = r"c:\Users\ryanz\Downloads\whardata\outputs\eda_tables"

def log(msg):
    ts = datetime.datetime.now().isoformat()
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[VISUALS2] {ts} | {msg}\n")
    print(msg)

def safe_read(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

def main():
    log("=== Extra Visuals Agent STARTED ===")
    os.makedirs(PLOT_DIR, exist_ok=True)
    
    # ──── 1. Consenus Top 10 Teams (Horizontal Bar Chart) ────
    cons_df = safe_read(os.path.join(RANK_DIR, "consensus_rankings.csv"))
    if not cons_df.empty:
        top10 = cons_df.sort_values('mean_rank').head(10).copy()
        top10 = top10.sort_values('mean_rank', ascending=False) # For proper hbar ordering
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x='mean_rank', y='team', data=top10, palette='viridis')
        plt.title('Top 10 Teams by Consensus Rank (Lower is Better)')
        plt.xlabel('Average Rank Across 10 Models')
        plt.ylabel('Team')
        plt.xlim(1, 15)
        
        # Add values on bars
        for idx, row in enumerate(top10.itertuples()):
            plt.text(row.mean_rank + 0.2, idx, f"{row.mean_rank:.2f}", va='center')
            
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_DIR, "Phase8_Consensus_Top10_Teams.png"), dpi=300)
        plt.close()
        log("Generated Consensus Top 10 Teams chart.")

    # ──── 2. Validation Accuracy Comparison (Bar Chart) ────
    val_set2 = safe_read(os.path.join(VAL_DIR, "validation_scores_set2.csv"))
    if not val_set2.empty:
        plot_df = val_set2.sort_values('accuracy', ascending=False).head(15)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x='accuracy', y='model_name', data=plot_df, palette='mako')
        plt.title('Model Predictive Accuracy (Set 2 Validation)')
        plt.xlabel('Out-of-Sample Rank Accuracy')
        plt.ylabel('Ranking Model')
        plt.xlim(0.5, 0.65) # Zoom in to show differences
        
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_DIR, "Phase8_Model_Accuracy_Comparison.png"), dpi=300)
        plt.close()
        log("Generated Model Accuracy Comparison chart.")

    # ──── 3. Team Style Clustering (xGF/60 vs xGA/60 Scatter) ────
    team_xg = safe_read(os.path.join(EDA_DIR, "team_es_xg_rates.csv"))
    if not team_xg.empty:
        plt.figure(figsize=(10, 8))
        sns.scatterplot(x='xgf60', y='xga60', data=team_xg, s=100, color='royalblue', edgecolor='w')
        
        # Plot mean lines to create quadrants
        plt.axvline(team_xg['xgf60'].mean(), color='r', linestyle='--', alpha=0.5)
        plt.axhline(team_xg['xga60'].mean(), color='r', linestyle='--', alpha=0.5)
        
        # Label each team
        for i in range(len(team_xg)):
            plt.text(team_xg.loc[i, 'xgf60'] + 0.02, team_xg.loc[i, 'xga60'], 
                     team_xg.loc[i, 'team'].title(), fontsize=8, alpha=0.8)
                     
        plt.title('Team Profiles: Expected Goals For vs Against (Per 60 Mins, ES)')
        plt.xlabel('Offense (xGF/60) → Higher is Better')
        plt.ylabel('Defense (xGA/60) → Lower is Better')
        
        # Annotate quadrants
        plt.text(team_xg['xgf60'].max(), team_xg['xga60'].min(), 'Good Offense\nGood Defense', 
                 ha='right', va='bottom', color='green', alpha=0.5, fontsize=12, fontweight='bold')
        plt.text(team_xg['xgf60'].min(), team_xg['xga60'].max(), 'Bad Offense\nBad Defense', 
                 ha='left', va='top', color='red', alpha=0.5, fontsize=12, fontweight='bold')
        
        plt.gca().invert_yaxis() # Invert y so "better defense" is at the top conceptually
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_DIR, "Phase8_Team_Style_Quadrants.png"), dpi=300)
        plt.close()
        log("Generated Team Style Quadrants scatter plot.")

    log("=== Extra Visuals Agent COMPLETED ===")

if __name__ == '__main__':
    main()
