import json
import random
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import pandas as pd
from dataclasses import dataclass, asdict
import math
from scipy import stats

@dataclass
class AppleWatchData:
    date: str
    heart_rate_avg: float
    heart_rate_resting: float
    heart_rate_variability: float
    sleep_duration_hours: float
    sleep_efficiency: float
    deep_sleep_hours: float
    rem_sleep_hours: float
    steps: int
    active_calories: int
    exercise_minutes: int
    stand_hours: int
    stress_score: float

@dataclass
class PHQ5Response:
    date: str
    little_interest: int
    feeling_down: int
    sleep_trouble: int
    tired_energy: int
    appetite: int
    total_score: int
    
@dataclass
class MoodDiaryEntry:
    date: str
    mood_rating: float
    anxiety_level: float
    craving_intensity: float
    energy_level: float
    sleep_quality: float
    pain_level: float
    triggers: List[str]
    coping_strategies: List[str]
    notes: str
    word_count: int

@dataclass
class ChatInteraction:
    date: str
    time: str
    message_count: int
    avg_response_time_hours: float
    sentiment_score: float
    topics: List[str]
    crisis_indicators: bool
    engagement_level: float

@dataclass
class SobrietyData:
    date: str
    days_sober: int
    relapse_risk_score: float
    in_treatment: bool
    medication_adherence: float
    meeting_attendance: int
    relapse_occurred: bool

class RealisticTimeSeriesGenerator:
    """Generate realistic time series with autocorrelation and persistence"""
    
    def __init__(self, random_seed=42):
        np.random.seed(random_seed)
        
    def generate_ar1_series(self, n_days: int, mean: float, std: float, phi: float = 0.7) -> np.ndarray:
        """Generate AR(1) time series with persistence parameter phi"""
        series = np.zeros(n_days)
        series[0] = np.random.normal(mean, std)
        
        for t in range(1, n_days):
            series[t] = phi * series[t-1] + (1 - phi) * mean + np.random.normal(0, std * np.sqrt(1 - phi**2))
        
        return series
    
    def generate_regime_switching_series(self, n_days: int, base_mean: float, base_std: float, 
                                       high_mean: float, high_std: float, 
                                       prob_enter_high: float = 0.05, prob_exit_high: float = 0.3) -> np.ndarray:
        """Generate series that switches between normal and high-risk regimes"""
        series = np.zeros(n_days)
        is_high_regime = np.zeros(n_days, dtype=bool)
        
        # Start in normal regime
        current_regime = 'normal'
        
        for t in range(n_days):
            # Regime switching logic
            if current_regime == 'normal':
                if np.random.random() < prob_enter_high:
                    current_regime = 'high'
            else:  # high regime
                if np.random.random() < prob_exit_high:
                    current_regime = 'normal'
            
            is_high_regime[t] = (current_regime == 'high')
            
            # Generate values based on current regime
            if current_regime == 'normal':
                if t == 0:
                    series[t] = np.random.normal(base_mean, base_std)
                else:
                    # AR(1) within regime
                    series[t] = 0.8 * series[t-1] + 0.2 * base_mean + np.random.normal(0, base_std * 0.5)
            else:
                if t == 0 or not is_high_regime[t-1]:
                    # Entering high regime
                    series[t] = np.random.normal(high_mean, high_std)
                else:
                    # Continuing in high regime
                    series[t] = 0.9 * series[t-1] + 0.1 * high_mean + np.random.normal(0, high_std * 0.3)
        
        return series, is_high_regime
    
    def add_weekly_seasonality(self, series: np.ndarray, amplitude: float = 0.1) -> np.ndarray:
        """Add weekly seasonality (weekends different from weekdays)"""
        n_days = len(series)
        seasonal = np.zeros(n_days)
        
        for i in range(n_days):
            day_of_week = i % 7
            if day_of_week in [5, 6]:  # Weekend
                seasonal[i] = amplitude * np.sin(2 * np.pi * day_of_week / 7)
            else:  # Weekday
                seasonal[i] = -amplitude * 0.3
        
        return series + seasonal * np.mean(series)

class PersonaDataGenerator:
    def __init__(self, start_date: str = "2024-01-01"):
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.ts_gen = RealisticTimeSeriesGenerator(random_seed=42)
        random.seed(42)
        np.random.seed(42)
        
    def calculate_base_relapse_risk(self, days_sober: int) -> float:
        """Calculate baseline relapse risk that decays over time"""
        if days_sober <= 0:
            return 0.9
        
        # Risk decays exponentially but levels off at steady state
        decay_rate = 0.008
        base_risk = 0.08  # Long-term steady state
        initial_risk = 0.75
        
        risk = base_risk + (initial_risk - base_risk) * math.exp(-decay_rate * days_sober)
        return min(max(risk, 0.05), 0.9)
    
    def generate_sarah_data(self) -> Dict[str, Any]:
        """Generate realistic data for Sarah Chen with work stress patterns"""
        data = {
            "persona": "Sarah Chen",
            "persona_type": "tech_savvy_professional",
            "apple_watch": [],
            "phq5": [],
            "mood_diary": [],
            "chat": [],
            "sobriety": []
        }
        
        n_days = 180
        initial_sobriety = 45
        
        # Generate realistic variation with work stress periods
        stress_periods, is_high_stress = self.ts_gen.generate_regime_switching_series(
            n_days, base_mean=0.0, base_std=0.05, 
            high_mean=0.15, high_std=0.08,
            prob_enter_high=0.08, prob_exit_high=0.25  # Stress periods last ~4 days on average
        )
        
        # Generate correlated biomarkers (will be adjusted for individual days)
        # Resting HR: baseline 78-82, higher during stress
        resting_hr_base = 80
        resting_hr_series = self.ts_gen.generate_ar1_series(n_days, resting_hr_base, 3, phi=0.8)
        resting_hr_series += is_high_stress * 8  # Stress increases HR
        resting_hr_series = self.ts_gen.add_weekly_seasonality(resting_hr_series, 0.02)
        
        # HRV: baseline 25, lower during stress (inversely correlated with HR)
        hrv_base = 25
        hrv_series = self.ts_gen.generate_ar1_series(n_days, hrv_base, 2, phi=0.8)
        hrv_series -= is_high_stress * 6  # Stress decreases HRV
        hrv_series = np.clip(hrv_series, 10, 45)
        
        # Sleep: baseline 7.5 hours, worse during stress
        sleep_base = 7.5
        sleep_series = self.ts_gen.generate_ar1_series(n_days, sleep_base, 0.5, phi=0.6)
        sleep_series -= is_high_stress * 0.8  # Stress reduces sleep
        sleep_series = np.clip(sleep_series, 5, 10)
        
        # Sleep efficiency: correlated with duration
        sleep_eff_base = 85
        sleep_eff_series = self.ts_gen.generate_ar1_series(n_days, sleep_eff_base, 5, phi=0.7)
        sleep_eff_series -= is_high_stress * 12  # Stress reduces efficiency
        sleep_eff_series = np.clip(sleep_eff_series, 60, 95)
        
        # Steps: baseline varies by weekday/weekend
        steps_base = 8000
        steps_series = self.ts_gen.generate_ar1_series(n_days, steps_base, 1500, phi=0.5)
        steps_series = self.ts_gen.add_weekly_seasonality(steps_series, 0.15)  # Lower on weekends
        steps_series = np.clip(steps_series, 3000, 15000)
        
        current_sobriety = initial_sobriety
        
        for day in range(n_days):
            current_date = self.start_date + timedelta(days=day)
            date_str = current_date.strftime("%Y-%m-%d")
            
            current_sobriety += 1
            
            # Calculate current baseline risk based on actual sobriety
            base_risk = self.calculate_base_relapse_risk(current_sobriety)
            
            # Add stress variation to baseline risk
            stress_addition = stress_periods[day]
            current_risk = np.clip(base_risk + stress_addition, 0.05, 0.9)
            
            # Check for relapse (very rare, based on risk)
            relapse_occurred = np.random.random() < current_risk * 0.01
            if relapse_occurred and current_sobriety > 30:
                current_sobriety = random.randint(1, 7)
                # Recalculate risk after relapse - should be very high
                base_risk = self.calculate_base_relapse_risk(current_sobriety)
                current_risk = np.clip(base_risk + stress_addition, 0.05, 0.9)
            
            # Generate mood/craving based on current risk
            mood_rating = max(1, min(10, 7.5 - current_risk * 4 + np.random.normal(0, 0.8)))
            craving_intensity = min(10, max(0, current_risk * 8 + np.random.normal(0, 1)))
            
            # Apple Watch data
            is_weekday = current_date.weekday() < 5
            
            apple_watch = AppleWatchData(
                date=date_str,
                heart_rate_avg=resting_hr_series[day] + random.randint(15, 25),
                heart_rate_resting=resting_hr_series[day],
                heart_rate_variability=hrv_series[day],
                sleep_duration_hours=sleep_series[day],
                sleep_efficiency=sleep_eff_series[day],
                deep_sleep_hours=sleep_series[day] * (0.18 + np.random.normal(0, 0.02)),
                rem_sleep_hours=sleep_series[day] * (0.25 + np.random.normal(0, 0.03)),
                steps=int(steps_series[day]),
                active_calories=int(steps_series[day] * 0.04 + np.random.normal(0, 20)),
                exercise_minutes=max(0, int(np.random.normal(25, 15))) if random.random() < 0.6 else 0,
                stand_hours=random.randint(8, 12) if is_weekday else random.randint(4, 9),
                stress_score=(current_risk * 60 + 30 + np.random.normal(0, 5))
            )
            
            # PHQ-5 responses (weekly)
            if day % 7 == 0:
                stress_level = int(is_high_stress[day])
                base_depression = max(0, 3 - current_sobriety // 60)  # Improves with time
                
                little_interest = min(3, max(0, int(base_depression + stress_level + np.random.normal(0, 0.5))))
                feeling_down = min(3, max(0, int(base_depression + stress_level + np.random.normal(0, 0.5))))
                sleep_trouble = min(3, max(0, int(1 + stress_level + np.random.normal(0, 0.5))))
                tired_energy = min(3, max(0, int(base_depression + stress_level + np.random.normal(0, 0.5))))
                appetite = min(3, max(0, int(base_depression + np.random.normal(0, 0.5))))
                
                phq5 = PHQ5Response(
                    date=date_str,
                    little_interest=little_interest,
                    feeling_down=feeling_down,
                    sleep_trouble=sleep_trouble,
                    tired_energy=tired_energy,
                    appetite=appetite,
                    total_score=little_interest + feeling_down + sleep_trouble + tired_energy + appetite
                )
                data["phq5"].append(asdict(phq5))
            
            # Mood diary (Sarah is consistent but varies by stress)
            if random.random() < (0.95 if not is_high_stress[day] else 0.85):
                triggers = []
                if is_high_stress[day]:
                    triggers.extend(random.sample(["work deadline", "presentation", "long hours", "conflict"], 
                                                random.randint(1, 3)))
                if current_date.weekday() == 4:  # Friday
                    if random.random() < 0.3:
                        triggers.append("social pressure")
                
                # Add relapse-specific triggers if recent relapse
                if relapse_occurred:
                    triggers.extend(["guilt", "shame", "restart anxiety"])
                elif current_sobriety < 30:
                    triggers.extend(["early recovery", "vulnerability"])
                
                coping_strategies = []
                if triggers:
                    coping_strategies.extend(random.sample(["meditation", "deep breathing", "call therapist", "exercise"], 
                                                         random.randint(1, 3)))
                else:
                    coping_strategies.extend(random.sample(["journaling", "gratitude", "exercise", "routine"], 
                                                         random.randint(1, 2)))
                
                mood_entry = MoodDiaryEntry(
                    date=date_str,
                    mood_rating=mood_rating,
                    anxiety_level=max(1, min(10, 4 + len(triggers) + current_risk * 3)),
                    craving_intensity=craving_intensity,
                    energy_level=max(1, min(10, 8 - len(triggers) - current_risk * 2)),
                    sleep_quality=sleep_eff_series[day] / 10,
                    pain_level=0,
                    triggers=triggers,
                    coping_strategies=coping_strategies,
                    notes=f"Day {current_sobriety} sober. {'Just relapsed - need to reset and focus' if relapse_occurred else 'Challenging period' if is_high_stress[day] else 'Staying focused on recovery'}.",
                    word_count=random.randint(80, 200)
                )
                data["mood_diary"].append(asdict(mood_entry))
            
            # Chat interactions (frequent, varies with stress and risk)
            chat_freq = 3 if not is_high_stress[day] else 5  # More chats when stressed
            if relapse_occurred or current_sobriety < 14:  # Much more engagement after relapse
                chat_freq += 3
                
            for _ in range(random.randint(max(1, chat_freq-1), chat_freq+2)):
                sentiment_base = 0.3 - current_risk * 0.8 - len(triggers) * 0.2
                if relapse_occurred:
                    sentiment_base -= 0.4  # More negative after relapse
                
                topics = ["work stress", "coping strategies", "sleep"] if triggers else ["progress", "goals", "routine"]
                if relapse_occurred:
                    topics = ["relapse", "guilt", "restart", "support"]
                elif current_sobriety < 30:
                    topics = ["early recovery", "cravings", "support", "routine"]
                
                chat = ChatInteraction(
                    date=date_str,
                    time=f"{random.randint(8, 22):02d}:{random.randint(0, 59):02d}",
                    message_count=random.randint(2, 15),
                    avg_response_time_hours=random.uniform(0.1, 3.0),
                    sentiment_score=max(-0.8, min(0.8, sentiment_base + np.random.normal(0, 0.2))),
                    topics=topics,
                    crisis_indicators=is_high_stress[day] and current_risk > 0.5,
                    engagement_level=max(1, min(10, 8 - current_risk * 3))
                )
                data["chat"].append(asdict(chat))
            
            # Sobriety tracking
            sobriety = SobrietyData(
                date=date_str,
                days_sober=current_sobriety,
                relapse_risk_score=current_risk,
                in_treatment=True,
                medication_adherence=max(0.7, min(1.0, 0.92 + np.random.normal(0, 0.05))),
                meeting_attendance=random.randint(2, 3),
                relapse_occurred=relapse_occurred
            )
            data["sobriety"].append(asdict(sobriety))
            data["apple_watch"].append(asdict(apple_watch))
        
        return data
    
    def generate_marcus_data(self) -> Dict[str, Any]:
        """Generate realistic data for Marcus Rodriguez - Veteran with longer sobriety"""
        data = {
            "persona": "Marcus Rodriguez",
            "persona_type": "veteran_in_recovery",
            "apple_watch": [],
            "phq5": [],
            "mood_diary": [],
            "chat": [],
            "sobriety": []
        }
        
        n_days = 180
        initial_sobriety = 180  # Already 6 months sober
        
        # Generate base relapse risk trend (lower due to longer sobriety)
        base_risks = np.array([self.calculate_base_relapse_risk(initial_sobriety + i) for i in range(n_days)])
        
        # PTSD episodes create different stress pattern - less frequent but more intense
        ptsd_periods, is_ptsd_episode = self.ts_gen.generate_regime_switching_series(
            n_days, base_mean=0.0, base_std=0.03, 
            high_mean=0.25, high_std=0.12,  # More intense than Sarah's work stress
            prob_enter_high=0.05, prob_exit_high=0.4  # Less frequent, shorter duration
        )
        
        # Combine base risk with PTSD variations
        relapse_risks = np.clip(base_risks + ptsd_periods, 0.05, 0.8)
        
        # Generate biomarkers - Marcus has different baselines
        resting_hr_base = 72  # Lower baseline than Sarah
        resting_hr_series = self.ts_gen.generate_ar1_series(n_days, resting_hr_base, 4, phi=0.8)
        resting_hr_series += is_ptsd_episode * 15  # PTSD episodes spike HR more
        
        # HRV baseline higher (better fitness) but drops more during episodes
        hrv_base = 28
        hrv_series = self.ts_gen.generate_ar1_series(n_days, hrv_base, 3, phi=0.8)
        hrv_series -= is_ptsd_episode * 10
        hrv_series = np.clip(hrv_series, 12, 45)
        
        # Sleep fragmented, especially during PTSD
        sleep_base = 6.5  # Shorter baseline
        sleep_series = self.ts_gen.generate_ar1_series(n_days, sleep_base, 0.6, phi=0.7)
        sleep_series -= is_ptsd_episode * 1.2
        sleep_series = np.clip(sleep_series, 4, 9)
        
        # Sleep efficiency worse than Sarah's
        sleep_eff_base = 75
        sleep_eff_series = self.ts_gen.generate_ar1_series(n_days, sleep_eff_base, 6, phi=0.7)
        sleep_eff_series -= is_ptsd_episode * 15
        sleep_eff_series = np.clip(sleep_eff_series, 50, 90)
        
        # Higher activity due to physical job
        steps_base = 12000
        steps_series = self.ts_gen.generate_ar1_series(n_days, steps_base, 2000, phi=0.6)
        steps_series = self.ts_gen.add_weekly_seasonality(steps_series, 0.2)  # Big weekend drop
        steps_series = np.clip(steps_series, 5000, 18000)
        
        current_sobriety = initial_sobriety
        
        for day in range(n_days):
            current_date = self.start_date + timedelta(days=day)
            date_str = current_date.strftime("%Y-%m-%d")
            current_sobriety += 1
            
            apple_watch = AppleWatchData(
                date=date_str,
                heart_rate_avg=resting_hr_series[day] + random.randint(12, 20),
                heart_rate_resting=resting_hr_series[day],
                heart_rate_variability=hrv_series[day],
                sleep_duration_hours=sleep_series[day],
                sleep_efficiency=sleep_eff_series[day],
                deep_sleep_hours=sleep_series[day] * (0.15 + np.random.normal(0, 0.02)),
                rem_sleep_hours=sleep_series[day] * (0.20 + np.random.normal(0, 0.03)),
                steps=int(steps_series[day]),
                active_calories=int(steps_series[day] * 0.05 + np.random.normal(0, 30)),
                exercise_minutes=max(0, int(np.random.normal(15, 10))) if random.random() < 0.3 else 0,
                stand_hours=random.randint(10, 14) if current_date.weekday() < 5 else random.randint(4, 8),
                stress_score=(relapse_risks[day] * 70 + 25 + np.random.normal(0, 8))
            )
            
            # Less frequent mood diary entries
            if random.random() < (0.6 if not is_ptsd_episode[day] else 0.4):
                triggers = []
                if is_ptsd_episode[day]:
                    triggers.extend(random.sample(["nightmare", "flashback", "loud noise", "crowd"], 
                                                random.randint(1, 2)))
                
                mood_entry = MoodDiaryEntry(
                    date=date_str,
                    mood_rating=max(1, min(10, 6.5 - relapse_risks[day] * 3)),
                    anxiety_level=max(1, min(10, 5 + len(triggers) + relapse_risks[day] * 2)),
                    craving_intensity=max(0, min(10, relapse_risks[day] * 6 + len(triggers) * 2)),
                    energy_level=max(1, min(10, 6 - len(triggers))),
                    sleep_quality=sleep_eff_series[day] / 12,
                    pain_level=random.randint(3, 7),  # Chronic back pain
                    triggers=triggers,
                    coping_strategies=["breathing exercises", "walk"] if triggers else ["work", "routine"],
                    notes=f"Day {current_sobriety}. {'Rough night' if is_ptsd_episode[day] else 'Steady'}",
                    word_count=random.randint(15, 50)
                )
                data["mood_diary"].append(asdict(mood_entry))
            
            # Less frequent chat interactions
            if random.random() < 0.35:
                # Define chat topics based on PTSD episodes
                chat_topics = ["PTSD", "pain", "family"] if is_ptsd_episode[day] else ["work", "routine", "meetings"]
                
                chat = ChatInteraction(
                    date=date_str,
                    time=f"{random.randint(18, 21):02d}:{random.randint(0, 59):02d}",
                    message_count=random.randint(2, 8),
                    avg_response_time_hours=random.uniform(3, 12),
                    sentiment_score=max(-0.6, min(0.4, 0.1 - relapse_risks[day] * 0.6)),
                    topics=chat_topics,
                    crisis_indicators=is_ptsd_episode[day] and relapse_risks[day] > 0.5,
                    engagement_level=max(1, min(10, 6 - relapse_risks[day] * 2))
                )
                data["chat"].append(asdict(chat))
            
            sobriety = SobrietyData(
                date=date_str,
                days_sober=current_sobriety,
                relapse_risk_score=relapse_risks[day],
                in_treatment=True,
                medication_adherence=max(0.85, min(1.0, 0.95 + np.random.normal(0, 0.03))),
                meeting_attendance=random.randint(3, 5),
                relapse_occurred=False
            )
            data["sobriety"].append(asdict(sobriety))
            data["apple_watch"].append(asdict(apple_watch))
        
        return data
    
    def generate_jessica_data(self) -> Dict[str, Any]:
        """Generate realistic data for Jessica Thompson - Young adult with higher volatility"""
        data = {
            "persona": "Jessica Thompson", 
            "persona_type": "young_adult_student",
            "apple_watch": [],
            "phq5": [],
            "mood_diary": [],
            "chat": [],
            "sobriety": []
        }
        
        n_days = 180
        initial_sobriety = 30  # Early recovery
        
        # Higher baseline risk due to early recovery
        base_risks = np.array([self.calculate_base_relapse_risk(initial_sobriety + i) for i in range(n_days)])
        
        # Social pressure periods - more frequent, college environment
        social_stress, is_social_pressure = self.ts_gen.generate_regime_switching_series(
            n_days, base_mean=0.0, base_std=0.06, 
            high_mean=0.20, high_std=0.10,
            prob_enter_high=0.12, prob_exit_high=0.3  # More frequent social challenges
        )
        
        relapse_risks = np.clip(base_risks + social_stress, 0.05, 0.85)
        
        # Higher baseline HR due to youth and anxiety
        resting_hr_base = 82
        resting_hr_series = self.ts_gen.generate_ar1_series(n_days, resting_hr_base, 5, phi=0.7)
        resting_hr_series += is_social_pressure * 12
        
        # Good HRV baseline but variable
        hrv_base = 32
        hrv_series = self.ts_gen.generate_ar1_series(n_days, hrv_base, 4, phi=0.6)
        hrv_series -= is_social_pressure * 8
        hrv_series = np.clip(hrv_series, 15, 50)
        
        # Irregular sleep schedule
        sleep_base = 6.8
        sleep_series = self.ts_gen.generate_ar1_series(n_days, sleep_base, 1.2, phi=0.5)  # More variable
        sleep_series = self.ts_gen.add_weekly_seasonality(sleep_series, 0.25)  # Later weekend nights
        sleep_series = np.clip(sleep_series, 4, 11)
        
        # Variable sleep efficiency
        sleep_eff_base = 78
        sleep_eff_series = self.ts_gen.generate_ar1_series(n_days, sleep_eff_base, 8, phi=0.6)
        sleep_eff_series -= is_social_pressure * 10
        sleep_eff_series = np.clip(sleep_eff_series, 60, 92)
        
        # Active but inconsistent
        steps_base = 9000
        steps_series = self.ts_gen.generate_ar1_series(n_days, steps_base, 2500, phi=0.4)
        steps_series = np.clip(steps_series, 3000, 16000)
        
        current_sobriety = initial_sobriety
        
        for day in range(n_days):
            current_date = self.start_date + timedelta(days=day)
            date_str = current_date.strftime("%Y-%m-%d")
            current_sobriety += 1
            
            apple_watch = AppleWatchData(
                date=date_str,
                heart_rate_avg=resting_hr_series[day] + random.randint(18, 28),
                heart_rate_resting=resting_hr_series[day],
                heart_rate_variability=hrv_series[day],
                sleep_duration_hours=sleep_series[day],
                sleep_efficiency=sleep_eff_series[day],
                deep_sleep_hours=sleep_series[day] * (0.20 + np.random.normal(0, 0.03)),
                rem_sleep_hours=sleep_series[day] * (0.28 + np.random.normal(0, 0.04)),
                steps=int(steps_series[day]),
                active_calories=int(steps_series[day] * 0.045 + np.random.normal(0, 25)),
                exercise_minutes=max(0, int(np.random.normal(35, 20))) if random.random() < 0.7 else 0,
                stand_hours=random.randint(6, 11),
                stress_score=(relapse_risks[day] * 65 + 25 + np.random.normal(0, 10))
            )
            
            # Very frequent mood diary entries
            if random.random() < 0.92:
                triggers = []
                if is_social_pressure[day]:
                    triggers.extend(random.sample(["party invite", "peer pressure", "exam stress", "social anxiety"], 
                                                random.randint(1, 3)))
                
                mood_entry = MoodDiaryEntry(
                    date=date_str,
                    mood_rating=max(1, min(10, 7.2 - relapse_risks[day] * 3.5)),
                    anxiety_level=max(1, min(10, 5 + len(triggers) + relapse_risks[day] * 2.5)),
                    craving_intensity=max(0, min(10, relapse_risks[day] * 7 + len(triggers) * 1.5)),
                    energy_level=max(1, min(10, 7.5 - len(triggers) - relapse_risks[day] * 1.5)),
                    sleep_quality=sleep_eff_series[day] / 10,
                    pain_level=0,
                    triggers=triggers,
                    coping_strategies=["text friend", "music", "exercise"] if triggers else ["study", "gratitude"],
                    notes=f"Day {current_sobriety} clean! 🌟 {'Challenging but staying strong' if triggers else 'Grateful for support'}",
                    word_count=random.randint(150, 350)
                )
                data["mood_diary"].append(asdict(mood_entry))
            
            # Frequent chat interactions
            for _ in range(random.randint(4, 9)):
                # Define triggers for chat context
                chat_triggers = []
                if is_social_pressure[day]:
                    chat_triggers = ["college stress", "social pressure", "future goals"]
                else:
                    chat_triggers = ["progress", "career", "recovery"]
                
                chat = ChatInteraction(
                    date=date_str,
                    time=f"{random.randint(7, 23):02d}:{random.randint(0, 59):02d}",
                    message_count=random.randint(6, 25),
                    avg_response_time_hours=random.uniform(0.05, 2.0),
                    sentiment_score=max(-0.7, min(0.8, 0.4 - relapse_risks[day] * 0.7)),
                    topics=chat_triggers,
                    crisis_indicators=is_social_pressure[day] and relapse_risks[day] > 0.6,
                    engagement_level=max(1, min(10, 8.5 - relapse_risks[day] * 2))
                )
                data["chat"].append(asdict(chat))
            
            sobriety = SobrietyData(
                date=date_str,
                days_sober=current_sobriety,
                relapse_risk_score=relapse_risks[day],
                in_treatment=True,
                medication_adherence=max(0.7, min(1.0, 0.88 + np.random.normal(0, 0.08))),
                meeting_attendance=random.randint(2, 4),
                relapse_occurred=False
            )
            data["sobriety"].append(asdict(sobriety))
            data["apple_watch"].append(asdict(apple_watch))
        
        return data
    
    def generate_robert_data(self) -> Dict[str, Any]:
        """Generate realistic data for Robert Williams - Older adult with depression"""
        data = {
            "persona": "Robert Williams",
            "persona_type": "empty_nester", 
            "apple_watch": [],
            "phq5": [],
            "mood_diary": [],
            "chat": [],
            "sobriety": []
        }
        
        n_days = 180
        initial_sobriety = 90  # 3 months sober
        
        base_risks = np.array([self.calculate_base_relapse_risk(initial_sobriety + i) for i in range(n_days)])
        
        # Loneliness/depression episodes
        depression_periods, is_depressed = self.ts_gen.generate_regime_switching_series(
            n_days, base_mean=0.0, base_std=0.04, 
            high_mean=0.18, high_std=0.09,
            prob_enter_high=0.06, prob_exit_high=0.2  # Longer depression periods
        )
        
        relapse_risks = np.clip(base_risks + depression_periods, 0.05, 0.75)
        
        # Lower resting HR but affected by depression
        resting_hr_base = 68
        resting_hr_series = self.ts_gen.generate_ar1_series(n_days, resting_hr_base, 3, phi=0.85)
        resting_hr_series += is_depressed * 8
        
        # Lower HRV baseline
        hrv_base = 22
        hrv_series = self.ts_gen.generate_ar1_series(n_days, hrv_base, 2, phi=0.8)
        hrv_series -= is_depressed * 5
        hrv_series = np.clip(hrv_series, 12, 35)
        
        # Long sleep but poor quality
        sleep_base = 8.5
        sleep_series = self.ts_gen.generate_ar1_series(n_days, sleep_base, 0.8, phi=0.8)
        sleep_series += is_depressed * 1.2  # Sleep more when depressed
        sleep_series = np.clip(sleep_series, 6, 12)
        
        # Poor sleep efficiency
        sleep_eff_base = 68
        sleep_eff_series = self.ts_gen.generate_ar1_series(n_days, sleep_eff_base, 6, phi=0.8)
        sleep_eff_series -= is_depressed * 10
        sleep_eff_series = np.clip(sleep_eff_series, 45, 80)
        
        # Very low activity
        steps_base = 3500
        steps_series = self.ts_gen.generate_ar1_series(n_days, steps_base, 800, phi=0.7)
        steps_series -= is_depressed * 800
        steps_series = np.clip(steps_series, 1200, 6000)
        
        current_sobriety = initial_sobriety
        
        for day in range(n_days):
            current_date = self.start_date + timedelta(days=day)
            date_str = current_date.strftime("%Y-%m-%d")
            current_sobriety += 1
            
            apple_watch = AppleWatchData(
                date=date_str,
                heart_rate_avg=resting_hr_series[day] + random.randint(8, 15),
                heart_rate_resting=resting_hr_series[day],
                heart_rate_variability=hrv_series[day],
                sleep_duration_hours=sleep_series[day],
                sleep_efficiency=sleep_eff_series[day],
                deep_sleep_hours=sleep_series[day] * (0.12 + np.random.normal(0, 0.02)),
                rem_sleep_hours=sleep_series[day] * (0.16 + np.random.normal(0, 0.02)),
                steps=int(steps_series[day]),
                active_calories=int(steps_series[day] * 0.03 + np.random.normal(0, 15)),
                exercise_minutes=max(0, int(np.random.normal(10, 8))) if random.random() < 0.2 else 0,
                stand_hours=random.randint(4, 8),
                stress_score=(relapse_risks[day] * 55 + 35 + np.random.normal(0, 8))
            )
            
            # Infrequent mood diary entries, gaps during depression
            if random.random() < (0.45 if not is_depressed[day] else 0.25):
                triggers = []
                if is_depressed[day]:
                    triggers.extend(random.sample(["loneliness", "missing family", "boredom"], 
                                                random.randint(1, 2)))
                
                mood_entry = MoodDiaryEntry(
                    date=date_str,
                    mood_rating=max(1, min(10, 5.2 - relapse_risks[day] * 2.5)),
                    anxiety_level=max(1, min(10, 4 + len(triggers) + relapse_risks[day] * 1.5)),
                    craving_intensity=max(0, min(10, relapse_risks[day] * 5.5 + len(triggers) * 2)),
                    energy_level=max(1, min(10, 4.5 - len(triggers) - relapse_risks[day] * 1.5)),
                    sleep_quality=sleep_eff_series[day] / 10,
                    pain_level=random.randint(4, 8),  # Chronic pain
                    triggers=triggers,
                    coping_strategies=["TV", "nap"] if triggers else ["routine", "walk"],
                    notes=f"{current_sobriety} days. {'Tough day' if triggers else 'Getting by'}",
                    word_count=random.randint(8, 30)
                )
                data["mood_diary"].append(asdict(mood_entry))
            
            # Infrequent chat interactions
            if random.random() < 0.25:
                # Define chat topics based on depression state
                chat_topics = ["loneliness", "health", "family"] if is_depressed[day] else ["routine", "court", "medication"]
                
                chat = ChatInteraction(
                    date=date_str,
                    time=f"{random.randint(14, 19):02d}:{random.randint(0, 59):02d}",
                    message_count=random.randint(1, 5),
                    avg_response_time_hours=random.uniform(6, 24),
                    sentiment_score=max(-0.8, min(0.2, -0.2 - relapse_risks[day] * 0.5)),
                    topics=chat_topics,
                    crisis_indicators=is_depressed[day] and relapse_risks[day] > 0.4,
                    engagement_level=max(1, min(10, 4.5 - relapse_risks[day] * 2))
                )
                data["chat"].append(asdict(chat))
            
            sobriety = SobrietyData(
                date=date_str,
                days_sober=current_sobriety,
                relapse_risk_score=relapse_risks[day],
                in_treatment=True,
                medication_adherence=max(0.9, min(1.0, 0.97 + np.random.normal(0, 0.02))),
                meeting_attendance=random.randint(2, 4),
                relapse_occurred=False
            )
            data["sobriety"].append(asdict(sobriety))
            data["apple_watch"].append(asdict(apple_watch))
        
        return data

    def generate_all_personas(self) -> Dict[str, Any]:
        """Generate realistic data for all personas"""
        print("Generating realistic synthetic data...")
        
        all_data = {
            "generation_info": {
                "start_date": self.start_date.strftime("%Y-%m-%d"),
                "days_generated": 180,
                "generation_method": "realistic_time_series_with_autocorrelation",
                "generation_timestamp": datetime.now().isoformat()
            },
            "personas": {}
        }
        
        print("Generating realistic data for Sarah Chen...")
        all_data["personas"]["sarah_chen"] = self.generate_sarah_data()
        
        print("Generating realistic data for Marcus Rodriguez...")
        all_data["personas"]["marcus_rodriguez"] = self.generate_marcus_data()
        
        print("Generating realistic data for Jessica Thompson...")
        all_data["personas"]["jessica_thompson"] = self.generate_jessica_data()
        
        print("Generating realistic data for Robert Williams...")
        all_data["personas"]["robert_williams"] = self.generate_robert_data()
        
        return all_data
    
    def save_data(self, data: Dict[str, Any], filename: str = "realistic_patient_data.json"):
        """Save generated data to JSON file"""
        # Convert numpy types to native Python types for JSON serialization
        def convert_numpy_types(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.bool_):
                return bool(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {key: convert_numpy_types(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy_types(item) for item in obj]
            else:
                return obj
        
        data_clean = convert_numpy_types(data)
        
        with open(filename, 'w') as f:
            json.dump(data_clean, f, indent=2)
        print(f"Realistic data saved to {filename}")

if __name__ == "__main__":
    generator = PersonaDataGenerator(start_date="2024-01-01")
    all_data = generator.generate_all_personas()
    generator.save_data(all_data, "data/realistic_patient_data.json")
    
    print("\n" + "="*50)
    print("REALISTIC DATA GENERATION COMPLETE")
    print("="*50)
    print("Generated 180 days of realistic data with:")
    print("- Autocorrelated time series")
    print("- Persistent risk states")
    print("- Regime-switching patterns")
    print("- Weekly seasonality")
    print("- Correlated biomarkers")
    
    sarah_data = all_data["personas"]["sarah_chen"]
    print(f"\nSarah Chen records: {len(sarah_data['apple_watch'])} days")
    print(f"Chat interactions: {len(sarah_data['chat'])}")
    print(f"Mood diary entries: {len(sarah_data['mood_diary'])}")
    
    # Show sample risk variation
    risks = [s['relapse_risk_score'] for s in sarah_data['sobriety'][:14]]
    print(f"\nFirst 14 days relapse risk: {[f'{r:.3f}' for r in risks]}")
    print("Notice: Values cluster around mean with persistence!") 