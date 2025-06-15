import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from datetime import datetime, timedelta

# Load the realistic data
with open('data/realistic_patient_data.json', 'r') as f:
    data = json.load(f)

def calculate_baseline_risk_proper(days_sober: int) -> float:
    """Calculate baseline relapse risk that decays over time - same function as generator"""
    if days_sober <= 0:
        return 0.9
    
    # Risk decays exponentially but levels off at steady state
    decay_rate = 0.008
    base_risk = 0.08  # Long-term steady state
    initial_risk = 0.75
    
    risk = base_risk + (initial_risk - base_risk) * math.exp(-decay_rate * days_sober)
    return min(max(risk, 0.05), 0.9)

# Set up the figure with 2x2 grid
fig, axes = plt.subplots(2, 2, figsize=(20, 16))
fig.suptitle('Detailed Risk Analysis: Baseline vs Total Risk with Relapse Events', 
             fontsize=16, fontweight='bold', y=0.95)

# Colors for each persona
colors = {
    'sarah_chen': '#e74c3c',
    'marcus_rodriguez': '#3498db', 
    'jessica_thompson': '#2ecc71',
    'robert_williams': '#f39c12'
}

persona_names = {
    'sarah_chen': 'Sarah Chen (Tech Professional)',
    'marcus_rodriguez': 'Marcus Rodriguez (Veteran)', 
    'jessica_thompson': 'Jessica Thompson (College Student)',
    'robert_williams': 'Robert Williams (Retired)'
}

# Plot each persona in a separate subplot
subplot_positions = [
    (0, 0),  # Sarah - top left
    (0, 1),  # Marcus - top right  
    (1, 0),  # Jessica - bottom left
    (1, 1)   # Robert - bottom right
]

for idx, (persona_id, persona_data) in enumerate(data['personas'].items()):
    row, col = subplot_positions[idx]
    ax = axes[row, col]
    
    sobriety_data = persona_data['sobriety']
    
    # Extract data
    days = list(range(len(sobriety_data)))
    actual_risks = [s['relapse_risk_score'] for s in sobriety_data]
    days_sober_sequence = [s['days_sober'] for s in sobriety_data]
    
    # Calculate what the baseline risk SHOULD be based on actual sobriety days
    baseline_risks = [calculate_baseline_risk_proper(days_sober) for days_sober in days_sober_sequence]
    
    # Calculate the "additional risk" (stress, PTSD, etc.) - difference between actual and baseline
    additional_risks = [actual - baseline for actual, baseline in zip(actual_risks, baseline_risks)]
    
    # Plot the components
    ax.plot(days, actual_risks, color=colors[persona_id], linewidth=3, 
           label='Total Risk', alpha=0.9)
    
    ax.plot(days, baseline_risks, color='black', linewidth=2, linestyle='--',
           label='Baseline Risk (Sobriety-driven)', alpha=0.7)
    
    ax.fill_between(days, baseline_risks, actual_risks, 
                   color=colors[persona_id], alpha=0.3, 
                   label='Additional Risk (Stress/PTSD/Depression)')
    
    # Mark relapse events
    for i, day_data in enumerate(sobriety_data):
        if day_data['relapse_occurred']:
            ax.axvline(x=i, color='red', linestyle=':', linewidth=3, alpha=0.8)
            ax.annotate('RELAPSE', xy=(i, 0.9), xytext=(i+10, 0.95),
                       arrowprops=dict(arrowstyle='->', color='red', lw=2),
                       fontsize=10, color='red', fontweight='bold')
    
    # Mark significant sobriety milestones
    if persona_id == 'sarah_chen':
        # Mark the relapse reset
        relapse_day = 48
        ax.axvline(x=relapse_day, color='red', linestyle=':', linewidth=3, alpha=0.8)
        ax.annotate('Risk resets after\nrelapse', 
                   xy=(relapse_day+5, baseline_risks[relapse_day+5]), 
                   xytext=(relapse_day+30, 0.8),
                   arrowprops=dict(arrowstyle='->', color='red', lw=2),
                   fontsize=9, color='red', fontweight='bold')
    
    # Customize subplot
    ax.set_title(f'{persona_names[persona_id]}\nSobriety: {days_sober_sequence[0]} → {days_sober_sequence[-1]} days', 
                fontsize=12, fontweight='bold')
    ax.set_xlabel('Study Day', fontsize=10)
    ax.set_ylabel('Risk Score', fontsize=10)
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=8)
    
    # Add text box with key stats
    mean_baseline = np.mean(baseline_risks)
    mean_additional = np.mean(additional_risks)
    textstr = f'Mean Baseline: {mean_baseline:.3f}\nMean Additional: {mean_additional:.3f}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=8,
           verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('data/detailed_risk_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Generate detailed analysis report
print("\n" + "="*80)
print("DETAILED RISK ANALYSIS REPORT")
print("="*80)

for persona_id, persona_data in data['personas'].items():
    sobriety_data = persona_data['sobriety']
    persona_name = persona_names[persona_id]
    
    days_sober_sequence = [s['days_sober'] for s in sobriety_data]
    actual_risks = [s['relapse_risk_score'] for s in sobriety_data]
    baseline_risks = [calculate_baseline_risk_proper(days_sober) for days_sober in days_sober_sequence]
    additional_risks = [actual - baseline for actual, baseline in zip(actual_risks, baseline_risks)]
    
    print(f"\n{persona_name}:")
    print(f"  Sobriety Journey: {days_sober_sequence[0]} → {days_sober_sequence[-1]} days")
    print(f"  Baseline Risk: {np.mean(baseline_risks):.3f} ± {np.std(baseline_risks):.3f}")
    print(f"  Additional Risk: {np.mean(additional_risks):.3f} ± {np.std(additional_risks):.3f}")
    print(f"  Total Risk: {np.mean(actual_risks):.3f} ± {np.std(actual_risks):.3f}")
    
    # Check for relapse events and analyze risk around them
    relapse_days = [i for i, day_data in enumerate(sobriety_data) if day_data['relapse_occurred']]
    if relapse_days:
        for relapse_day in relapse_days:
            pre_relapse_risk = actual_risks[max(0, relapse_day-5):relapse_day]
            post_relapse_baseline = baseline_risks[relapse_day:min(len(baseline_risks), relapse_day+5)]
            
            print(f"  RELAPSE EVENT (Day {relapse_day}):")
            print(f"    Pre-relapse risk trend: {np.mean(pre_relapse_risk):.3f}")
            print(f"    Post-relapse baseline reset: {post_relapse_baseline[0]:.3f} → {post_relapse_baseline[-1]:.3f}")
    else:
        print(f"  No relapse events detected")

# Create a focused Sarah Chen analysis
print(f"\n{'='*80}")
print("SARAH CHEN RELAPSE DEEP DIVE")
print("="*80)

sarah_data = data['personas']['sarah_chen']['sobriety']
sarah_risks = [s['relapse_risk_score'] for s in sarah_data]
sarah_days_sober = [s['days_sober'] for s in sarah_data]
sarah_baseline = [calculate_baseline_risk_proper(days) for days in sarah_days_sober]

relapse_day = 48
pre_window = slice(max(0, relapse_day-10), relapse_day)
post_window = slice(relapse_day, min(len(sarah_risks), relapse_day+10))

print(f"Pre-relapse period (days {pre_window.start}-{pre_window.stop-1}):")
print(f"  Sobriety: {sarah_days_sober[pre_window.start]} → {sarah_days_sober[pre_window.stop-1]} days")
print(f"  Risk: {np.mean(sarah_risks[pre_window]):.3f} (should be elevated)")
print(f"  Baseline: {np.mean(sarah_baseline[pre_window]):.3f}")

print(f"\nPost-relapse period (days {post_window.start}-{post_window.stop-1}):")
print(f"  Sobriety: {sarah_days_sober[post_window.start]} → {sarah_days_sober[post_window.stop-1]} days")
print(f"  Risk: {np.mean(sarah_risks[post_window]):.3f} (should reset high)")
print(f"  Baseline: {np.mean(sarah_baseline[post_window]):.3f} (reset to high early-recovery risk)")

print(f"\nBaseline Risk Reset Verification:")
print(f"  Before relapse (93 days sober): {calculate_baseline_risk_proper(93):.3f}")
print(f"  After relapse (4 days sober): {calculate_baseline_risk_proper(4):.3f}")
print(f"  Risk increase due to reset: {calculate_baseline_risk_proper(4) - calculate_baseline_risk_proper(93):.3f}")

print("\nVisualization saved to: data/detailed_risk_analysis.png") 