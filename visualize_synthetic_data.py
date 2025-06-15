import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import seaborn as sns

# Set style for better plots
plt.style.use('seaborn')
sns.set_palette("husl")

def load_data():
    """Load the synthetic patient data"""
    with open('data/synthetic_patient_data.json', 'r') as f:
        return json.load(f)

def plot_relapse_risk_curves(data):
    """Plot relapse risk curves for all personas showing decay over time"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
    
    for i, (persona_id, persona_data) in enumerate(data['personas'].items()):
        sobriety_data = persona_data['sobriety']
        days = [s['days_sober'] for s in sobriety_data]
        risks = [s['relapse_risk_score'] for s in sobriety_data]
        
        # Plot relapse risk over days sober
        ax1.plot(days, risks, label=persona_data['persona'], 
                color=colors[i], linewidth=2, alpha=0.8)
        
        # Plot relapse risk over calendar time
        calendar_days = list(range(len(risks)))
        ax2.plot(calendar_days, risks, label=persona_data['persona'],
                color=colors[i], linewidth=2, alpha=0.8)
    
    ax1.set_xlabel('Days Sober')
    ax1.set_ylabel('Relapse Risk Score')
    ax1.set_title('Relapse Risk vs. Days Sober\n(Shows Decay Pattern)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.set_xlabel('Calendar Days (Study Period)')
    ax2.set_ylabel('Relapse Risk Score')
    ax2.set_title('Relapse Risk Over Study Period\n(180 Days)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('data/relapse_risk_patterns.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_biomarker_trends(data):
    """Plot key biomarker trends for each persona"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
    
    for i, (persona_id, persona_data) in enumerate(data['personas'].items()):
        ax = axes[i]
        
        # Extract biomarker data
        apple_data = persona_data['apple_watch']
        days = list(range(len(apple_data)))
        
        # Create multiple y-axes for different metrics
        ax2 = ax.twinx()
        ax3 = ax.twinx()
        ax3.spines['right'].set_position(('outward', 60))
        
        # Plot multiple biomarkers
        resting_hr = [w['heart_rate_resting'] for w in apple_data]
        hrv = [w['heart_rate_variability'] for w in apple_data]
        sleep_duration = [w['sleep_duration_hours'] for w in apple_data]
        
        # Smooth the data for better visualization
        window = 7  # 7-day rolling average
        resting_hr_smooth = pd.Series(resting_hr).rolling(window, center=True).mean()
        hrv_smooth = pd.Series(hrv).rolling(window, center=True).mean()
        sleep_smooth = pd.Series(sleep_duration).rolling(window, center=True).mean()
        
        line1 = ax.plot(days, resting_hr_smooth, 'b-', linewidth=2, alpha=0.8, label='Resting HR')
        line2 = ax2.plot(days, hrv_smooth, 'r-', linewidth=2, alpha=0.8, label='HRV')
        line3 = ax3.plot(days, sleep_smooth, 'g-', linewidth=2, alpha=0.8, label='Sleep (hrs)')
        
        # Customize axes
        ax.set_xlabel('Days')
        ax.set_ylabel('Resting Heart Rate (bpm)', color='b')
        ax.tick_params(axis='y', labelcolor='b')
        
        ax2.set_ylabel('Heart Rate Variability', color='r')
        ax2.tick_params(axis='y', labelcolor='r')
        
        ax3.set_ylabel('Sleep Duration (hours)', color='g')
        ax3.tick_params(axis='y', labelcolor='g')
        
        ax.set_title(f"{persona_data['persona']}\nBiomarker Trends (7-day avg)")
        ax.grid(True, alpha=0.3)
        
        # Add legend
        lines = line1 + line2 + line3
        labels = [l.get_label() for l in lines]
        ax.legend(lines, labels, loc='upper left')
    
    plt.tight_layout()
    plt.savefig('data/biomarker_trends.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_engagement_patterns(data):
    """Plot engagement patterns across different data types"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    
    personas = list(data['personas'].items())
    persona_names = [p[1]['persona'] for p in personas]
    
    # Chat interactions per day
    chat_frequencies = []
    for persona_id, persona_data in personas:
        chat_data = persona_data['chat']
        daily_chats = {}
        for chat in chat_data:
            date = chat['date']
            daily_chats[date] = daily_chats.get(date, 0) + 1
        chat_frequencies.append(list(daily_chats.values()))
    
    axes[0,0].boxplot(chat_frequencies, labels=[name.split()[0] for name in persona_names])
    axes[0,0].set_title('Daily Chat Interactions Distribution')
    axes[0,0].set_ylabel('Messages per Day')
    axes[0,0].grid(True, alpha=0.3)
    
    # Mood diary entry lengths
    diary_lengths = []
    for persona_id, persona_data in personas:
        lengths = [entry['word_count'] for entry in persona_data['mood_diary']]
        diary_lengths.append(lengths)
    
    axes[0,1].boxplot(diary_lengths, labels=[name.split()[0] for name in persona_names])
    axes[0,1].set_title('Mood Diary Entry Lengths')
    axes[0,1].set_ylabel('Word Count')
    axes[0,1].grid(True, alpha=0.3)
    
    # PHQ-5 scores over time
    for i, (persona_id, persona_data) in enumerate(personas):
        phq5_data = persona_data['phq5']
        if phq5_data:
            dates = [datetime.strptime(p['date'], '%Y-%m-%d') for p in phq5_data]
            scores = [p['total_score'] for p in phq5_data]
            axes[1,0].plot(dates, scores, 'o-', label=persona_data['persona'].split()[0], 
                          linewidth=2, markersize=6, alpha=0.8)
    
    axes[1,0].set_title('PHQ-5 Depression Scores Over Time')
    axes[1,0].set_ylabel('PHQ-5 Total Score')
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # Activity levels comparison
    activity_data = []
    for persona_id, persona_data in personas:
        steps = [w['steps'] for w in persona_data['apple_watch']]
        activity_data.append(steps)
    
    axes[1,1].boxplot(activity_data, labels=[name.split()[0] for name in persona_names])
    axes[1,1].set_title('Daily Step Count Distribution')
    axes[1,1].set_ylabel('Steps per Day')
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('data/engagement_patterns.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_persona_comparison(data):
    """Create a comprehensive comparison of personas"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    personas = list(data['personas'].items())
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
    
    # 1. Relapse Risk Distribution
    ax = axes[0,0]
    for i, (persona_id, persona_data) in enumerate(personas):
        risks = [s['relapse_risk_score'] for s in persona_data['sobriety']]
        ax.hist(risks, alpha=0.6, label=persona_data['persona'].split()[0], 
               color=colors[i], bins=20)
    ax.set_title('Relapse Risk Distribution')
    ax.set_xlabel('Risk Score')
    ax.set_ylabel('Frequency')
    ax.legend()
    
    # 2. Sleep Quality vs Sobriety
    ax = axes[0,1]
    for i, (persona_id, persona_data) in enumerate(personas):
        days_sober = [s['days_sober'] for s in persona_data['sobriety']]
        sleep_efficiency = [w['sleep_efficiency'] for w in persona_data['apple_watch']]
        ax.scatter(days_sober, sleep_efficiency, alpha=0.6, 
                  label=persona_data['persona'].split()[0], color=colors[i], s=10)
    ax.set_title('Sleep Quality vs Days Sober')
    ax.set_xlabel('Days Sober')
    ax.set_ylabel('Sleep Efficiency (%)')
    ax.legend()
    
    # 3. Heart Rate Variability Trends
    ax = axes[0,2]
    for i, (persona_id, persona_data) in enumerate(personas):
        hrv_data = [w['heart_rate_variability'] for w in persona_data['apple_watch']]
        # 14-day rolling average
        hrv_smooth = pd.Series(hrv_data).rolling(14, center=True).mean()
        days = list(range(len(hrv_smooth)))
        ax.plot(days, hrv_smooth, label=persona_data['persona'].split()[0], 
               color=colors[i], linewidth=2, alpha=0.8)
    ax.set_title('Heart Rate Variability Trends')
    ax.set_xlabel('Days')
    ax.set_ylabel('HRV')
    ax.legend()
    
    # 4. Mood vs Craving Intensity
    ax = axes[1,0]
    for i, (persona_id, persona_data) in enumerate(personas):
        mood_data = persona_data['mood_diary']
        if mood_data:
            mood_ratings = [m['mood_rating'] for m in mood_data]
            craving_intensities = [m['craving_intensity'] for m in mood_data]
            ax.scatter(mood_ratings, craving_intensities, alpha=0.6,
                      label=persona_data['persona'].split()[0], color=colors[i], s=20)
    ax.set_title('Mood vs Craving Intensity')
    ax.set_xlabel('Mood Rating (1-10)')
    ax.set_ylabel('Craving Intensity (0-10)')
    ax.legend()
    
    # 5. Medication Adherence
    ax = axes[1,1]
    adherence_data = []
    names = []
    for persona_id, persona_data in personas:
        adherence = [s['medication_adherence'] for s in persona_data['sobriety']]
        adherence_data.append(adherence)
        names.append(persona_data['persona'].split()[0])
    
    bp = ax.boxplot(adherence_data, labels=names, patch_artist=True)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    ax.set_title('Medication Adherence')
    ax.set_ylabel('Adherence Rate')
    
    # 6. Chat Sentiment Over Time
    ax = axes[1,2]
    for i, (persona_id, persona_data) in enumerate(personas):
        chat_data = persona_data['chat']
        if chat_data:
            # Group by date and average sentiment
            daily_sentiment = {}
            for chat in chat_data:
                date = chat['date']
                sentiment = chat['sentiment_score']
                if date in daily_sentiment:
                    daily_sentiment[date].append(sentiment)
                else:
                    daily_sentiment[date] = [sentiment]
            
            dates = sorted(daily_sentiment.keys())
            avg_sentiments = [np.mean(daily_sentiment[date]) for date in dates]
            
            # Convert dates to days from start
            start_date = datetime.strptime(dates[0], '%Y-%m-%d')
            days = [(datetime.strptime(date, '%Y-%m-%d') - start_date).days for date in dates]
            
            # Smooth with rolling average
            sentiment_smooth = pd.Series(avg_sentiments).rolling(7, center=True).mean()
            ax.plot(days, sentiment_smooth, label=persona_data['persona'].split()[0],
                   color=colors[i], linewidth=2, alpha=0.8)
    
    ax.set_title('Chat Sentiment Trends (7-day avg)')
    ax.set_xlabel('Days')
    ax.set_ylabel('Average Sentiment Score')
    ax.legend()
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('data/persona_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def generate_sample_records(data):
    """Generate sample records for demonstration"""
    samples = {}
    
    for persona_id, persona_data in data['personas'].items():
        # Get a sample day (day 60)
        sample_day = 60
        
        sample = {
            'persona': persona_data['persona'],
            'date': persona_data['apple_watch'][sample_day]['date'],
            'apple_watch': persona_data['apple_watch'][sample_day],
            'sobriety': persona_data['sobriety'][sample_day]
        }
        
        # Find mood diary entry for that day
        mood_entries = [m for m in persona_data['mood_diary'] 
                       if m['date'] == sample['date']]
        if mood_entries:
            sample['mood_diary'] = mood_entries[0]
        
        # Find chat interactions for that day
        chat_entries = [c for c in persona_data['chat'] 
                       if c['date'] == sample['date']]
        if chat_entries:
            sample['chat_sample'] = chat_entries[0]
        
        # Find PHQ-5 if available
        phq5_entries = [p for p in persona_data['phq5'] 
                       if p['date'] == sample['date']]
        if phq5_entries:
            sample['phq5'] = phq5_entries[0]
        
        samples[persona_id] = sample
    
    # Save sample records
    with open('data/sample_records.json', 'w') as f:
        json.dump(samples, f, indent=2)
    
    return samples

def main():
    """Main function to run all visualizations"""
    print("Loading synthetic patient data...")
    data = load_data()
    
    print("Generating visualizations...")
    
    # Create all plots
    plot_relapse_risk_curves(data)
    plot_biomarker_trends(data)
    plot_engagement_patterns(data)
    plot_persona_comparison(data)
    
    # Generate sample records
    print("Generating sample records...")
    samples = generate_sample_records(data)
    
    print("\nSample Record for Sarah Chen (Day 60):")
    print("="*50)
    sarah_sample = samples['sarah_chen']
    print(f"Date: {sarah_sample['date']}")
    print(f"Days Sober: {sarah_sample['sobriety']['days_sober']}")
    print(f"Relapse Risk: {sarah_sample['sobriety']['relapse_risk_score']:.3f}")
    print(f"Resting HR: {sarah_sample['apple_watch']['heart_rate_resting']:.1f} bpm")
    print(f"HRV: {sarah_sample['apple_watch']['heart_rate_variability']:.1f}")
    print(f"Sleep Duration: {sarah_sample['apple_watch']['sleep_duration_hours']:.1f} hours")
    print(f"Steps: {sarah_sample['apple_watch']['steps']:,}")
    
    if 'mood_diary' in sarah_sample:
        print(f"Mood Rating: {sarah_sample['mood_diary']['mood_rating']:.1f}/10")
        print(f"Craving Intensity: {sarah_sample['mood_diary']['craving_intensity']:.1f}/10")
        print(f"Triggers: {sarah_sample['mood_diary']['triggers']}")
    
    print("\n" + "="*60)
    print("VISUALIZATION COMPLETE")
    print("="*60)
    print("Generated plots:")
    print("  - data/relapse_risk_patterns.png")
    print("  - data/biomarker_trends.png") 
    print("  - data/engagement_patterns.png")
    print("  - data/persona_comparison.png")
    print("  - data/sample_records.json")

if __name__ == "__main__":
    main() 