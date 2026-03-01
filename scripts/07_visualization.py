"""
Visualization Agent — WHL 2025
Phase 1c: Generate the required PNG visualization
Relationship between line disparity and team strength
"""
import os, datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as plt_sns
from matplotlib.offsetbox import AnnotationBbox, TextArea

LOG_FILE  = r"c:\Users\ryanz\Downloads\whardata\scratch\agent_log.txt"
OUT_DIR   = r"c:\Users\ryanz\Downloads\whardata\outputs\plots"
RANK_FILE = r"c:\Users\ryanz\Downloads\whardata\outputs\rankings\consensus_rankings.csv"
DISP_FILE = r"c:\Users\ryanz\Downloads\whardata\outputs\disparity\consensus_disparity.csv"

def log(msg):
    ts = datetime.datetime.now().isoformat()
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[VISUAL] {ts} | {msg}\n")
    print(msg)

def main():
    log("=== Visualization Agent STARTED ===")
    
    if not os.path.exists(RANK_FILE) or not os.path.exists(DISP_FILE):
        log("ERROR: Required input files for visualization not found.")
        return
        
    rank_df = pd.read_csv(RANK_FILE)
    disp_df = pd.read_csv(DISP_FILE)
    
    # Merge on team
    df = pd.merge(
        rank_df[['team', 'mean_rank']].rename(columns={'mean_rank': 'team_strength_rank'}),
        disp_df[['team', 'mean_rank', 'consensus_rank']].rename(columns={'mean_rank': 'disparity_score'}),
        on='team'
    )
    
    # Invert strength rank so better teams are higher on Y axis (rank 1 = top)
    # We'll use actual mean rank values for continuous plotting, but inverted
    df['strength_score'] = 33 - df['team_strength_rank'] 
    
    # Set the style
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    
    # Create scatter plot
    scatter = ax.scatter(
        df['disparity_score'], 
        df['strength_score'],
        s=100,
        c=df['strength_score'],
        cmap='viridis',
        alpha=0.7,
        edgecolors='w',
        linewidth=1
    )
    
    # Add trend line
    z = np.polyfit(df['disparity_score'], df['strength_score'], 1)
    p = np.poly1d(z)
    ax.plot(df['disparity_score'], p(df['disparity_score']), "r--", alpha=0.5, 
            label=f'Trend Line (Correlation: {df["disparity_score"].corr(df["strength_score"]):.2f})')
    
    # Label top 10 disparity teams
    top10_teams = set(df.sort_values('consensus_rank').head(10)['team'])
    
    for i, row in df.iterrows():
        team = row['team']
        x = row['disparity_score']
        y = row['strength_score']
        
        # Highlight top 10 disparity teams
        if team in top10_teams:
            ax.annotate(team, (x, y), xytext=(5, 5), textcoords='offset points',
                        fontsize=9, fontweight='bold', color='darkblue')
            # Add a circle around the top 10 points
            ax.scatter(x, y, s=150, facecolors='none', edgecolors='red', linewidth=1.5)
        else:
            ax.annotate(team, (x, y), xytext=(5, 5), textcoords='offset points',
                        fontsize=8, alpha=0.7)
            
    # Draw quadrants to help interpretation
    mean_disp = df['disparity_score'].mean()
    mean_str = df['strength_score'].mean()
    ax.axvline(x=mean_disp, color='gray', linestyle=':', alpha=0.5)
    ax.axhline(y=mean_str, color='gray', linestyle=':', alpha=0.5)
    
    # Label quadrants
    ax.text(df['disparity_score'].min(), df['strength_score'].max(), 
            'High Disparity,\nStrong Team', fontsize=10, alpha=0.5, style='italic', va='top')
    ax.text(df['disparity_score'].max() * 0.95, df['strength_score'].max(), 
            'Low Disparity,\nStrong Team', fontsize=10, alpha=0.5, style='italic', va='top', ha='right')
    ax.text(df['disparity_score'].min(), df['strength_score'].min(), 
            'High Disparity,\nWeak Team', fontsize=10, alpha=0.5, style='italic')
    ax.text(df['disparity_score'].max() * 0.95, df['strength_score'].min(), 
            'Low Disparity,\nWeak Team', fontsize=10, alpha=0.5, style='italic', ha='right')

    # Formatting
    ax.set_title('Relationship Between Line Disparity and Team Strength', fontsize=16, pad=20, fontweight='bold')
    ax.set_xlabel('Line Disparity Score (Lower = More Top-Heavy)', fontsize=12, labelpad=10)
    ax.set_ylabel('Overall Team Strength Score (Higher = Better Team)', fontsize=12, labelpad=10)
    
    # Invert X axis so that "better" (lower numbers = rank 1) is on the right
    ax.invert_xaxis()
    
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(loc='lower left')
    
    # Save the plot
    out_path = os.path.join(OUT_DIR, "Phase1c_LineDisparity_vs_TeamStrength.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    log(f"Visualization saved to: {out_path}")
    
    # Create the secondary plot (correlation heatmap from validation)
    corr_file = r"c:\Users\ryanz\Downloads\whardata\outputs\disparity_method_correlation.csv"
    if os.path.exists(corr_file):
        corr_df = pd.read_csv(corr_file, index_col=0)
        plt.figure(figsize=(10, 8), dpi=300)
        
        # Use simple matplotlib for heatmap to avoid seaborn dependency issues if it's missing
        fig2, ax2 = plt.subplots(figsize=(10, 8))
        cax = ax2.matshow(corr_df, cmap='coolwarm', vmin=0, vmax=1)
        fig2.colorbar(cax)
        
        # Plot formatting
        plt.xticks(range(len(corr_df.columns)), corr_df.columns, rotation=45, ha='left')
        plt.yticks(range(len(corr_df.index)), corr_df.index)
        
        # Add values
        for i in range(len(corr_df.index)):
            for j in range(len(corr_df.columns)):
                plt.text(j, i, f'{corr_df.iloc[i, j]:.2f}', ha='center', va='center', 
                         color='white' if corr_df.iloc[i, j] > 0.7 or corr_df.iloc[i, j] < 0.3 else 'black',
                         fontsize=8)
                
        plt.title('Line Disparity Methods: Rank Correlation Matrix', pad=20, fontweight='bold')
        out_path2 = os.path.join(OUT_DIR, "Disparity_Method_Correlation.png")
        plt.tight_layout()
        plt.savefig(out_path2, bbox_inches='tight', dpi=300)
        log(f"Correlation heatmap saved to: {out_path2}")
        
    log("=== Visualization Agent COMPLETED ===")

if __name__ == '__main__':
    main()
