import json

with open('data/realistic_patient_data.json', 'r') as f:
    data = json.load(f)

sarah_sobriety = data['personas']['sarah_chen']['sobriety']

print('Sarah Chen Relapse Analysis:')
print('Day | Days Sober | Risk Score | Relapsed?')
print('-' * 45)

relapse_day = None
for i, day_data in enumerate(sarah_sobriety):
    risk = day_data['relapse_risk_score']
    days_sober = day_data['days_sober']
    
    # Check for relapse indicators
    if day_data['relapse_occurred']:
        print(f'{i:3d} | {days_sober:9d} | {risk:8.3f} | YES ⚠️ RELAPSE OCCURRED')
        relapse_day = i
    elif i > 0 and days_sober < sarah_sobriety[i-1]['days_sober']:
        print(f'{i:3d} | {days_sober:9d} | {risk:8.3f} | RESET ⚠️ (dropped from {sarah_sobriety[i-1]["days_sober"]})')
        if relapse_day is None:
            relapse_day = i
    elif i < 10 or (relapse_day and abs(i - relapse_day) < 5) or i % 30 == 0:
        status = "No" if not day_data['relapse_occurred'] else "YES"
        print(f'{i:3d} | {days_sober:9d} | {risk:8.3f} | {status}')

if relapse_day:
    pre_relapse_days = sarah_sobriety[relapse_day-1]['days_sober'] if relapse_day > 0 else 'N/A'
    post_relapse_days = sarah_sobriety[relapse_day]['days_sober']
    risk_at_relapse = sarah_sobriety[relapse_day]['relapse_risk_score']
    
    print(f'\n📍 RELAPSE DETECTED:')
    print(f'   Study Day: {relapse_day}')
    print(f'   Before: {pre_relapse_days} days sober')
    print(f'   After: {post_relapse_days} days sober') 
    print(f'   Risk Score: {risk_at_relapse:.3f}')
    print(f'   Recovery Progress: Built back up to {sarah_sobriety[-1]["days_sober"]} days by study end')
else:
    print('\n✅ No relapse detected - sobriety counter should have increased smoothly')

# Check all personas for relapses
print('\n' + '='*60)
print('RELAPSE SUMMARY - ALL PERSONAS')
print('='*60)

for persona_id, persona_data in data['personas'].items():
    sobriety_data = persona_data['sobriety']
    persona_name = persona_data['persona']
    
    # Count actual relapses
    relapses = sum(1 for day in sobriety_data if day['relapse_occurred'])
    
    # Check for sobriety counter drops (another way to detect relapses)
    counter_drops = 0
    for i in range(1, len(sobriety_data)):
        if sobriety_data[i]['days_sober'] < sobriety_data[i-1]['days_sober']:
            counter_drops += 1
    
    start_days = sobriety_data[0]['days_sober']
    end_days = sobriety_data[-1]['days_sober']
    expected_end = start_days + 180
    days_lost = expected_end - end_days
    
    print(f'{persona_name}:')
    print(f'  Flagged relapses: {relapses}')
    print(f'  Counter drops: {counter_drops}') 
    print(f'  Days lost: {days_lost} (expected {expected_end}, got {end_days})')
    print(f'  Status: {"⚠️ RELAPSED" if days_lost > 10 else "✅ MAINTAINED SOBRIETY"}')
    print() 