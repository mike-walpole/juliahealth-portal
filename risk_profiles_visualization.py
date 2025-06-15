import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Load the realistic data
with open('data/realistic_patient_data.json', 'r') as f:
    data = json.load(f)

# Set up the figure with subplots
fig = plt.figure(figsize=(20, 14))

# Create a grid layout for better organization
gs = fig.add_gridspec(3, 2, height_ratios=[2, 1, 1], hspace=0.3, wspace=0.2)

# Colors for each persona
colors = {
    'sarah_chen': '#e74c3c',        # Red - Tech professional stress
    'marcus_rodriguez': '#3498db',   # Blue - Veteran stability  
    'jessica_thompson': '#2ecc71',   # Green - Young adult energy
    'robert_williams': '#f39c12'     # Orange - Older adult depression
}

persona_names = {
    'sarah_chen': 'Sarah Chen (Tech Professional)',
    'marcus_rodriguez': 'Marcus Rodriguez (Veteran)', 
    'jessica_thompson': 'Jessica Thompson (College Student)',
    'robert_williams': 'Robert Williams (Retired)'
}

# Main risk profile plot
ax_main = fig.add_subplot(gs[0, :])

print("Plotting risk profiles for all four personas...")

for persona_id, persona_data in data['personas'].items():
    sobriety_data = persona_data['sobriety']
    
    # Extract risk scores and days
    days = list(range(len(sobriety_data)))
    risks = [s['relapse_risk_score'] for s in sobriety_data]
    days_sober = [s['days_sober'] for s in sobriety_data]
    
    # Plot with 7-day smoothing for clarity
    risk_smooth = pd.Series(risks).rolling(7, center=True).mean()
    
    # Plot the risk profile
    ax_main.plot(days, risk_smooth, color=colors[persona_id], linewidth=3, 
                label=f"{persona_names[persona_id]}", alpha=0.9)
    
    # Add dots for actual data points (subsample for clarity)
    subsample = slice(None, None, 14)  # Every 2 weeks
    ax_main.scatter(days[subsample], [risks[i] for i in range(len(risks))][subsample], 
                   color=colors[persona_id], alpha=0.4, s=20)

# Customize main plot
ax_main.set_title('Relapse Risk Profiles: 180-Day Longitudinal Study\n(7-day smoothed with autocorrelated patterns)', 
                 fontsize=16, fontweight='bold', pad=20)
ax_main.set_xlabel('Study Day', fontsize=12)
ax_main.set_ylabel('Relapse Risk Score', fontsize=12)
ax_main.set_ylim(0, 1)
ax_main.grid(True, alpha=0.3)
ax_main.legend(loc='upper right', fontsize=11)

# Add annotations for key patterns
ax_main.annotate('High early risk\n(new recovery)', 
                xy=(10, 0.7), xytext=(40, 0.85),
                arrowprops=dict(arrowstyle='->', color='darkgreen', lw=2),
                fontsize=10, color='darkgreen', fontweight='bold')

ax_main.annotate('Lowest risk\n(longest sobriety)', 
                xy=(90, 0.2), xytext=(120, 0.35),
                arrowprops=dict(arrowstyle='->', color='darkblue', lw=2),
                fontsize=10, color='darkblue', fontweight='bold')

# Individual persona details - Sarah and Marcus
ax_sarah = fig.add_subplot(gs[1, 0])
sarah_data = data['personas']['sarah_chen']['sobriety']
sarah_risks = [s['relapse_risk_score'] for s in sarah_data]
sarah_days_sober = [s['days_sober'] for s in sarah_data]

ax_sarah.plot(range(len(sarah_risks)), sarah_risks, color=colors['sarah_chen'], linewidth=2)
ax_sarah.fill_between(range(len(sarah_risks)), sarah_risks, alpha=0.3, color=colors['sarah_chen'])
ax_sarah.set_title('Sarah Chen: Work Stress Patterns\n(Started 45 days sober)', fontsize=11, fontweight='bold')
ax_sarah.set_ylabel('Risk Score', fontsize=10)
ax_sarah.grid(True, alpha=0.3)
ax_sarah.set_ylim(0, 1)

# Add sobriety timeline
ax_sarah_twin = ax_sarah.twinx()
ax_sarah_twin.plot(range(len(sarah_days_sober)), sarah_days_sober, 
                  color='darkred', linestyle='--', alpha=0.7, linewidth=2)
ax_sarah_twin.set_ylabel('Days Sober', color='darkred', fontsize=10)
ax_sarah_twin.tick_params(axis='y', labelcolor='darkred')

ax_marcus = fig.add_subplot(gs[1, 1])
marcus_data = data['personas']['marcus_rodriguez']['sobriety']
marcus_risks = [s['relapse_risk_score'] for s in marcus_data]
marcus_days_sober = [s['days_sober'] for s in marcus_data]

ax_marcus.plot(range(len(marcus_risks)), marcus_risks, color=colors['marcus_rodriguez'], linewidth=2)
ax_marcus.fill_between(range(len(marcus_risks)), marcus_risks, alpha=0.3, color=colors['marcus_rodriguez'])
ax_marcus.set_title('Marcus Rodriguez: PTSD Episodes\n(Started 180 days sober)', fontsize=11, fontweight='bold')
ax_marcus.set_ylabel('Risk Score', fontsize=10)
ax_marcus.grid(True, alpha=0.3)
ax_marcus.set_ylim(0, 1)

# Add sobriety timeline
ax_marcus_twin = ax_marcus.twinx()
ax_marcus_twin.plot(range(len(marcus_days_sober)), marcus_days_sober, 
                   color='darkblue', linestyle='--', alpha=0.7, linewidth=2)
ax_marcus_twin.set_ylabel('Days Sober', color='darkblue', fontsize=10)
ax_marcus_twin.tick_params(axis='y', labelcolor='darkblue')

# Individual persona details - Jessica and Robert
ax_jessica = fig.add_subplot(gs[2, 0])
jessica_data = data['personas']['jessica_thompson']['sobriety']
jessica_risks = [s['relapse_risk_score'] for s in jessica_data]
jessica_days_sober = [s['days_sober'] for s in jessica_data]

ax_jessica.plot(range(len(jessica_risks)), jessica_risks, color=colors['jessica_thompson'], linewidth=2)
ax_jessica.fill_between(range(len(jessica_risks)), jessica_risks, alpha=0.3, color=colors['jessica_thompson'])
ax_jessica.set_title('Jessica Thompson: Social Pressure\n(Started 30 days sober)', fontsize=11, fontweight='bold')
ax_jessica.set_xlabel('Study Day', fontsize=10)
ax_jessica.set_ylabel('Risk Score', fontsize=10)
ax_jessica.grid(True, alpha=0.3)
ax_jessica.set_ylim(0, 1)

# Add sobriety timeline
ax_jessica_twin = ax_jessica.twinx()
ax_jessica_twin.plot(range(len(jessica_days_sober)), jessica_days_sober, 
                    color='darkgreen', linestyle='--', alpha=0.7, linewidth=2)
ax_jessica_twin.set_ylabel('Days Sober', color='darkgreen', fontsize=10)
ax_jessica_twin.tick_params(axis='y', labelcolor='darkgreen')

ax_robert = fig.add_subplot(gs[2, 1])
robert_data = data['personas']['robert_williams']['sobriety']
robert_risks = [s['relapse_risk_score'] for s in robert_data]
robert_days_sober = [s['days_sober'] for s in robert_data]

ax_robert.plot(range(len(robert_risks)), robert_risks, color=colors['robert_williams'], linewidth=2)
ax_robert.fill_between(range(len(robert_risks)), robert_risks, alpha=0.3, color=colors['robert_williams'])
ax_robert.set_title('Robert Williams: Depression Episodes\n(Started 90 days sober)', fontsize=11, fontweight='bold')
ax_robert.set_xlabel('Study Day', fontsize=10)
ax_robert.set_ylabel('Risk Score', fontsize=10)
ax_robert.grid(True, alpha=0.3)
ax_robert.set_ylim(0, 1)

# Add sobriety timeline
ax_robert_twin = ax_robert.twinx()
ax_robert_twin.plot(range(len(robert_days_sober)), robert_days_sober, 
                   color='darkorange', linestyle='--', alpha=0.7, linewidth=2)
ax_robert_twin.set_ylabel('Days Sober', color='darkorange', fontsize=10)
ax_robert_twin.tick_params(axis='y', labelcolor='darkorange')

plt.tight_layout()
plt.savefig('data/risk_profiles_all_personas.png', dpi=300, bbox_inches='tight')
plt.show()

# Generate summary statistics
print("\n" + "="*80)
print("RISK PROFILE SUMMARY - 180 DAY STUDY")
print("="*80)

for persona_id, persona_data in data['personas'].items():
    sobriety_data = persona_data['sobriety']
    risks = [s['relapse_risk_score'] for s in sobriety_data]
    
    initial_sober = sobriety_data[0]['days_sober']
    final_sober = sobriety_data[-1]['days_sober']
    
    print(f"\n{persona_names[persona_id]}:")
    print(f"  Sobriety Journey: {initial_sober} → {final_sober} days (+{final_sober - initial_sober} days)")
    print(f"  Risk Statistics:")
    print(f"    Mean Risk: {np.mean(risks):.3f}")
    print(f"    Risk Range: {np.min(risks):.3f} - {np.max(risks):.3f}")
    print(f"    Risk Std Dev: {np.std(risks):.3f}")
    print(f"    High Risk Days (>0.6): {sum(1 for r in risks if r > 0.6)}/180 ({100*sum(1 for r in risks if r > 0.6)/180:.1f}%)")

print(f"\n{'='*80}")
print("KEY PATTERNS OBSERVED:")
print("• Jessica (college) has highest volatility and risk due to early recovery")
print("• Marcus (veteran) has lowest overall risk due to longest sobriety")  
print("• Sarah (professional) shows work stress regime-switching")
print("• Robert (older adult) has persistent depression-related risk elevation")
print("• All personas show realistic autocorrelation and persistence patterns")
print("• Risk decreases over time as sobriety increases (clinical decay pattern)")

# Create a comparison table
print(f"\n{'='*80}")
print("COMPARATIVE RISK METRICS:")
print("="*80)
print(f"{'Persona':<25} {'Start Days':<12} {'End Days':<10} {'Mean Risk':<12} {'High Risk %':<12}")
print("-" * 80)

for persona_id, persona_data in data['personas'].items():
    sobriety_data = persona_data['sobriety']
    risks = [s['relapse_risk_score'] for s in sobriety_data]
    initial_sober = sobriety_data[0]['days_sober']
    final_sober = sobriety_data[-1]['days_sober']
    high_risk_pct = 100 * sum(1 for r in risks if r > 0.6) / 180
    
    name = persona_names[persona_id].split('(')[0].strip()
    print(f"{name:<25} {initial_sober:<12} {final_sober:<10} {np.mean(risks):<12.3f} {high_risk_pct:<12.1f}")

print("\nVisualization saved to: data/risk_profiles_all_personas.png") 