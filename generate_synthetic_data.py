import json
import random
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import pandas as pd
from dataclasses import dataclass, asdict
import math

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
    stress_score: float  # 0-100, higher = more stressed

@dataclass
class PHQ5Response:
    date: str
    little_interest: int  # 0-3
    feeling_down: int     # 0-3
    sleep_trouble: int    # 0-3
    tired_energy: int     # 0-3
    appetite: int         # 0-3
    total_score: int
    
@dataclass
class MoodDiaryEntry:
    date: str
    mood_rating: float    # 1-10
    anxiety_level: float  # 1-10
    craving_intensity: float  # 0-10
    energy_level: float   # 1-10
    sleep_quality: float  # 1-10
    pain_level: float     # 0-10 (for those with chronic pain)
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
    sentiment_score: float  # -1 to 1
    topics: List[str]
    crisis_indicators: bool
    engagement_level: float  # 1-10

@dataclass
class SobrietyData:
    date: str
    days_sober: int
    relapse_risk_score: float  # 0-1, higher = higher risk
    in_treatment: bool
    medication_adherence: float  # 0-1
    meeting_attendance: int  # meetings per week
    relapse_occurred: bool

class PersonaDataGenerator:
    def __init__(self, start_date: str = "2024-01-01"):
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.random_seed = 42
        random.seed(self.random_seed)
        np.random.seed(self.random_seed)
        
    def calculate_relapse_risk(self, days_sober: int) -> float:
        """Calculate relapse risk based on days sober - high at first, decaying to steady state at 12 months"""
        if days_sober <= 0:
            return 0.9
        
        # Risk starts high (0.8) and decays exponentially
        # Reaches steady state (~0.1) at 365 days (12 months)
        decay_rate = 0.008  # Adjusted for 12-month decay
        base_risk = 0.1  # Steady state risk
        initial_risk = 0.8
        
        risk = base_risk + (initial_risk - base_risk) * math.exp(-decay_rate * days_sober)
        return min(max(risk, 0.05), 0.9)  # Clamp between 5% and 90%
    
    def add_noise(self, value: float, noise_factor: float = 0.1) -> float:
        """Add random noise to a value"""
        noise = np.random.normal(0, value * noise_factor)
        return max(0, value + noise)
    
    def generate_sarah_data(self) -> Dict[str, Any]:
        """Generate data for Sarah Chen - Tech-Savvy Professional"""
        data = {
            "persona": "Sarah Chen",
            "persona_type": "tech_savvy_professional",
            "apple_watch": [],
            "phq5": [],
            "mood_diary": [],
            "chat": [],
            "sobriety": []
        }
        
        # Sarah starts with 45 days clean
        initial_sobriety = 45
        current_sobriety = initial_sobriety
        
        for day in range(180):
            current_date = self.start_date + timedelta(days=day)
            date_str = current_date.strftime("%Y-%m-%d")
            
            # Update sobriety status
            current_sobriety += 1
            relapse_risk = self.calculate_relapse_risk(current_sobriety)
            
            # Small chance of relapse based on risk score
            relapse_occurred = random.random() < relapse_risk * 0.02  # Scale down for realistic frequency
            if relapse_occurred and current_sobriety > 30:  # Only after some time
                current_sobriety = random.randint(1, 7)  # Reset to early recovery
            
            # Apple Watch Data - patterns reflect work stress and anxiety
            is_weekday = current_date.weekday() < 5
            is_work_stress_day = is_weekday and random.random() < 0.3
            
            base_resting_hr = 85 if current_sobriety < 90 else 78  # Improves with sobriety
            resting_hr = self.add_noise(base_resting_hr + (10 if is_work_stress_day else 0))
            avg_hr = resting_hr + random.randint(15, 25)
            
            # HRV lower during stress
            base_hrv = 25 if current_sobriety > 60 else 20
            hrv = self.add_noise(base_hrv - (8 if is_work_stress_day else 0))
            
            # Sleep patterns - poor quality, especially during stress
            sleep_duration = self.add_noise(6.5 if is_work_stress_day else 7.5, 0.15)
            sleep_efficiency = self.add_noise(78 if is_work_stress_day else 85, 0.1)
            
            apple_watch = AppleWatchData(
                date=date_str,
                heart_rate_avg=avg_hr,
                heart_rate_resting=resting_hr,
                heart_rate_variability=hrv,
                sleep_duration_hours=sleep_duration,
                sleep_efficiency=sleep_efficiency,
                deep_sleep_hours=self.add_noise(sleep_duration * 0.2),
                rem_sleep_hours=self.add_noise(sleep_duration * 0.25),
                steps=random.randint(6000, 12000) if is_weekday else random.randint(3000, 8000),
                active_calories=random.randint(250, 400),
                exercise_minutes=random.randint(0, 60) if random.random() < 0.4 else 0,
                stand_hours=random.randint(8, 12) if is_weekday else random.randint(4, 8),
                stress_score=random.randint(60, 90) if is_work_stress_day else random.randint(30, 60)
            )
            
            # PHQ-5 responses (weekly)
            if day % 7 == 0:
                stress_modifier = 2 if is_work_stress_day else 0
                relapse_modifier = 3 if current_sobriety < 30 else 0
                
                little_interest = min(3, max(0, 1 + stress_modifier + relapse_modifier - (current_sobriety // 30)))
                feeling_down = min(3, max(0, 1 + stress_modifier + relapse_modifier - (current_sobriety // 30)))
                sleep_trouble = min(3, max(0, 2 + stress_modifier - (current_sobriety // 45)))
                tired_energy = min(3, max(0, 2 + stress_modifier + relapse_modifier - (current_sobriety // 30)))
                appetite = min(3, max(0, 1 + stress_modifier - (current_sobriety // 60)))
                
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
            
            # Mood diary (daily, detailed entries)
            if random.random() < 0.9:  # Sarah is consistent
                triggers = []
                if is_work_stress_day:
                    triggers.extend(["work deadline", "presentation anxiety", "long hours"])
                if current_date.weekday() == 4:  # Friday
                    triggers.append("social pressure")
                
                coping_strategies = ["meditation app", "deep breathing", "call therapist"] if triggers else ["exercise", "journaling"]
                
                mood_rating = self.add_noise(7 - relapse_risk * 3 - len(triggers))
                
                mood_entry = MoodDiaryEntry(
                    date=date_str,
                    mood_rating=max(1, min(10, mood_rating)),
                    anxiety_level=max(1, min(10, 4 + len(triggers) + relapse_risk * 2)),
                    craving_intensity=max(0, min(10, relapse_risk * 8 + len(triggers))),
                    energy_level=max(1, min(10, 7 - len(triggers) - relapse_risk * 2)),
                    sleep_quality=max(1, min(10, sleep_efficiency / 10)),
                    pain_level=0,  # Sarah doesn't have chronic pain
                    triggers=triggers,
                    coping_strategies=coping_strategies,
                    notes=f"Day {current_sobriety} sober. {'Stressful work day' if is_work_stress_day else 'Feeling stable'}",
                    word_count=random.randint(50, 150)
                )
                data["mood_diary"].append(asdict(mood_entry))
            
            # Chat interactions (2-3 times daily)
            for chat_session in range(random.randint(2, 4)):
                hour = random.randint(8, 22)
                chat = ChatInteraction(
                    date=date_str,
                    time=f"{hour:02d}:{random.randint(0, 59):02d}",
                    message_count=random.randint(3, 12),
                    avg_response_time_hours=random.uniform(0.1, 2.0),
                    sentiment_score=max(-0.8, min(0.8, 0.3 - relapse_risk - len(triggers) * 0.2)),
                    topics=["coping strategies", "work stress", "sleep issues"] if triggers else ["progress", "goals", "gratitude"],
                    crisis_indicators=relapse_risk > 0.6 and len(triggers) > 2,
                    engagement_level=max(1, min(10, 8 - relapse_risk * 2))
                )
                data["chat"].append(asdict(chat))
            
            # Sobriety tracking
            sobriety = SobrietyData(
                date=date_str,
                days_sober=current_sobriety,
                relapse_risk_score=relapse_risk,
                in_treatment=True,
                medication_adherence=random.uniform(0.85, 0.98),
                meeting_attendance=random.randint(2, 3),  # Outpatient groups
                relapse_occurred=relapse_occurred
            )
            data["sobriety"].append(asdict(sobriety))
            data["apple_watch"].append(asdict(apple_watch))
        
        return data
    
    def generate_marcus_data(self) -> Dict[str, Any]:
        """Generate data for Marcus Rodriguez - Veteran in Recovery"""
        data = {
            "persona": "Marcus Rodriguez",
            "persona_type": "veteran_in_recovery",
            "apple_watch": [],
            "phq5": [],
            "mood_diary": [],
            "chat": [],
            "sobriety": []
        }
        
        # Marcus starts with 6 months (180 days) clean
        initial_sobriety = 180
        current_sobriety = initial_sobriety
        
        for day in range(180):
            current_date = self.start_date + timedelta(days=day)
            date_str = current_date.strftime("%Y-%m-%d")
            
            current_sobriety += 1
            relapse_risk = self.calculate_relapse_risk(current_sobriety)
            
            # Marcus has PTSD episodes
            ptsd_episode = random.random() < 0.1  # 10% chance per day
            high_pain_day = random.random() < 0.3  # Chronic back pain
            
            # Relapse risk higher during PTSD episodes
            if ptsd_episode:
                relapse_risk *= 1.5
            
            relapse_occurred = random.random() < relapse_risk * 0.015  # Lower than Sarah due to longer sobriety
            if relapse_occurred and current_sobriety > 60:
                current_sobriety = random.randint(1, 14)
            
            # Apple Watch Data - PTSD and pain patterns
            base_resting_hr = 72 + (15 if ptsd_episode else 0) + (5 if high_pain_day else 0)
            resting_hr = self.add_noise(base_resting_hr)
            avg_hr = resting_hr + random.randint(10, 20)
            
            # HRV affected by PTSD and pain
            base_hrv = 28 - (12 if ptsd_episode else 0) - (5 if high_pain_day else 0)
            hrv = self.add_noise(max(10, base_hrv))
            
            # Sleep fragmented, worse during PTSD episodes
            sleep_duration = self.add_noise(5.5 if ptsd_episode else 6.8, 0.2)
            sleep_efficiency = self.add_noise(65 if ptsd_episode else 75, 0.15)
            
            # Physical job keeps activity high on weekdays
            is_weekday = current_date.weekday() < 5
            steps = random.randint(8000, 15000) if is_weekday else random.randint(2000, 6000)
            
            apple_watch = AppleWatchData(
                date=date_str,
                heart_rate_avg=avg_hr,
                heart_rate_resting=resting_hr,
                heart_rate_variability=hrv,
                sleep_duration_hours=sleep_duration,
                sleep_efficiency=sleep_efficiency,
                deep_sleep_hours=self.add_noise(sleep_duration * 0.15),  # Less deep sleep
                rem_sleep_hours=self.add_noise(sleep_duration * 0.2),
                steps=steps,
                active_calories=random.randint(400, 700) if is_weekday else random.randint(150, 300),
                exercise_minutes=random.randint(0, 30) if random.random() < 0.2 else 0,
                stand_hours=random.randint(10, 14) if is_weekday else random.randint(3, 7),
                stress_score=random.randint(70, 95) if ptsd_episode else random.randint(40, 70)
            )
            
            # PHQ-5 responses (every 2 weeks, tends to under-report)
            if day % 14 == 0:
                ptsd_modifier = 2 if ptsd_episode else 0
                pain_modifier = 1 if high_pain_day else 0
                
                # Marcus under-reports emotional symptoms
                little_interest = min(3, max(0, 1 + ptsd_modifier + pain_modifier - (current_sobriety // 60)))
                feeling_down = min(3, max(0, 1 + ptsd_modifier - (current_sobriety // 90)))
                sleep_trouble = min(3, max(0, 2 + ptsd_modifier))  # Always has sleep issues
                tired_energy = min(3, max(0, 3 + pain_modifier - (current_sobriety // 30)))
                appetite = min(3, max(0, 1 + ptsd_modifier))
                
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
            
            # Mood diary (brief entries, focuses on practical)
            if random.random() < 0.7:  # Less consistent than Sarah
                triggers = []
                if ptsd_episode:
                    triggers.extend(["nightmare", "flashback", "loud noise"])
                if high_pain_day:
                    triggers.append("back pain")
                if current_date.weekday() == 6:  # Sunday
                    triggers.append("family stress")
                
                coping_strategies = ["breathing exercises", "call sponsor", "walk"] if triggers else ["work", "routine"]
                
                mood_entry = MoodDiaryEntry(
                    date=date_str,
                    mood_rating=max(1, min(10, 6 - relapse_risk * 2 - len(triggers))),
                    anxiety_level=max(1, min(10, 5 + len(triggers) + relapse_risk * 2)),
                    craving_intensity=max(0, min(10, relapse_risk * 6 + len(triggers) * 2)),
                    energy_level=max(1, min(10, 5 - len(triggers) - (1 if high_pain_day else 0))),
                    sleep_quality=max(1, min(10, sleep_efficiency / 12)),
                    pain_level=random.randint(6, 9) if high_pain_day else random.randint(2, 5),
                    triggers=triggers,
                    coping_strategies=coping_strategies,
                    notes=f"Sober {current_sobriety} days. Pain level {'high' if high_pain_day else 'manageable'}",
                    word_count=random.randint(10, 40)  # Brief entries
                )
                data["mood_diary"].append(asdict(mood_entry))
            
            # Chat interactions (every 2-3 days, practical focus)
            if random.random() < 0.4:
                chat = ChatInteraction(
                    date=date_str,
                    time=f"{random.randint(18, 21):02d}:{random.randint(0, 59):02d}",  # Evening
                    message_count=random.randint(2, 6),
                    avg_response_time_hours=random.uniform(2, 12),
                    sentiment_score=max(-0.6, min(0.5, 0.1 - relapse_risk - len(triggers) * 0.3)),
                    topics=["pain management", "family", "work"] if triggers else ["routine", "meetings", "progress"],
                    crisis_indicators=ptsd_episode and relapse_risk > 0.5,
                    engagement_level=max(1, min(10, 6 - relapse_risk * 2))
                )
                data["chat"].append(asdict(chat))
            
            # Sobriety tracking
            sobriety = SobrietyData(
                date=date_str,
                days_sober=current_sobriety,
                relapse_risk_score=relapse_risk,
                in_treatment=True,
                medication_adherence=random.uniform(0.9, 0.99),  # Good at following medical advice
                meeting_attendance=random.randint(3, 5),  # AA + IOP
                relapse_occurred=relapse_occurred
            )
            data["sobriety"].append(asdict(sobriety))
            data["apple_watch"].append(asdict(apple_watch))
        
        return data
    
    def generate_jessica_data(self) -> Dict[str, Any]:
        """Generate data for Jessica Thompson - Young Adult Student"""
        data = {
            "persona": "Jessica Thompson",
            "persona_type": "young_adult_student",
            "apple_watch": [],
            "phq5": [],
            "mood_diary": [],
            "chat": [],
            "sobriety": []
        }
        
        # Jessica starts with 30 days clean
        initial_sobriety = 30
        current_sobriety = initial_sobriety
        
        for day in range(180):
            current_date = self.start_date + timedelta(days=day)
            date_str = current_date.strftime("%Y-%m-%d")
            
            current_sobriety += 1
            relapse_risk = self.calculate_relapse_risk(current_sobriety)
            
            # College stressors
            is_exam_period = day % 30 < 7  # Exam week every month
            social_pressure_day = current_date.weekday() in [4, 5, 6] and random.random() < 0.4  # Weekend parties
            presentation_day = random.random() < 0.1  # Social anxiety trigger
            
            # Higher relapse risk during social pressure
            if social_pressure_day:
                relapse_risk *= 1.8
            
            relapse_occurred = random.random() < relapse_risk * 0.025  # Higher than Marcus due to environment
            if relapse_occurred and current_sobriety > 14:
                current_sobriety = random.randint(1, 5)
            
            # Apple Watch Data - social anxiety and irregular schedule
            base_resting_hr = 78 + (15 if presentation_day else 0) + (10 if is_exam_period else 0)
            resting_hr = self.add_noise(base_resting_hr)
            avg_hr = resting_hr + random.randint(12, 25)
            
            # HRV affected by anxiety and irregular sleep
            base_hrv = 35 - (10 if presentation_day else 0) - (5 if is_exam_period else 0)
            hrv = self.add_noise(base_hrv)
            
            # Irregular sleep schedule
            bedtime_variance = 2 if current_date.weekday() < 5 else 4  # Later on weekends
            sleep_duration = self.add_noise(7 + random.uniform(-bedtime_variance, bedtime_variance/2), 0.3)
            sleep_efficiency = self.add_noise(82 - (10 if is_exam_period else 0), 0.2)
            
            # Active lifestyle but inconsistent
            is_weekday = current_date.weekday() < 5
            base_steps = 8000 if is_weekday else random.randint(3000, 12000)  # Variable weekends
            
            apple_watch = AppleWatchData(
                date=date_str,
                heart_rate_avg=avg_hr,
                heart_rate_resting=resting_hr,
                heart_rate_variability=hrv,
                sleep_duration_hours=max(4, min(12, sleep_duration)),
                sleep_efficiency=sleep_efficiency,
                deep_sleep_hours=self.add_noise(sleep_duration * 0.22),
                rem_sleep_hours=self.add_noise(sleep_duration * 0.28),
                steps=self.add_noise(base_steps, 0.3),
                active_calories=random.randint(200, 500),
                exercise_minutes=random.randint(30, 90) if random.random() < 0.6 else 0,
                stand_hours=random.randint(6, 10) if is_weekday else random.randint(3, 8),
                stress_score=random.randint(70, 95) if presentation_day else random.randint(35, 65)
            )
            
            # PHQ-5 responses (weekly, detailed)
            if day % 7 == 0:
                exam_modifier = 2 if is_exam_period else 0
                social_modifier = 1 if social_pressure_day else 0
                
                little_interest = min(3, max(0, 1 + exam_modifier + social_modifier - (current_sobriety // 45)))
                feeling_down = min(3, max(0, 2 + social_modifier - (current_sobriety // 30)))
                sleep_trouble = min(3, max(0, 1 + exam_modifier))
                tired_energy = min(3, max(0, 2 + exam_modifier - (current_sobriety // 30)))
                appetite = min(3, max(0, 1 + exam_modifier))
                
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
            
            # Mood diary (very detailed, emotional)
            if random.random() < 0.95:  # Very consistent
                triggers = []
                if is_exam_period:
                    triggers.extend(["exam stress", "academic pressure", "perfectionism"])
                if social_pressure_day:
                    triggers.extend(["party invitation", "peer pressure", "FOMO"])
                if presentation_day:
                    triggers.append("public speaking anxiety")
                
                coping_strategies = ["text friend", "listen to music", "journal", "exercise"] if triggers else ["gratitude practice", "study group", "self-care"]
                
                mood_entry = MoodDiaryEntry(
                    date=date_str,
                    mood_rating=max(1, min(10, 7 - relapse_risk * 3 - len(triggers) * 0.5)),
                    anxiety_level=max(1, min(10, 4 + len(triggers) * 1.5 + relapse_risk * 2)),
                    craving_intensity=max(0, min(10, relapse_risk * 7 + len(triggers) * 1.5)),
                    energy_level=max(1, min(10, 7 - len(triggers) - (2 if is_exam_period else 0))),
                    sleep_quality=max(1, min(10, sleep_efficiency / 10)),
                    pain_level=0,  # No chronic pain
                    triggers=triggers,
                    coping_strategies=coping_strategies,
                    notes=f"Day {current_sobriety} clean! 🌟 {'Stressed about exams' if is_exam_period else 'Feeling grateful for support system'}. Future goals: graduate school in counseling! 💪",
                    word_count=random.randint(100, 300)  # Very detailed
                )
                data["mood_diary"].append(asdict(mood_entry))
            
            # Chat interactions (multiple times daily)
            for chat_session in range(random.randint(3, 8)):
                hour = random.randint(7, 23)
                chat = ChatInteraction(
                    date=date_str,
                    time=f"{hour:02d}:{random.randint(0, 59):02d}",
                    message_count=random.randint(5, 20),
                    avg_response_time_hours=random.uniform(0.05, 1.0),  # Quick responses
                    sentiment_score=max(-0.7, min(0.9, 0.4 - relapse_risk - len(triggers) * 0.2)),
                    topics=["school stress", "social anxiety", "future goals"] if triggers else ["progress", "gratitude", "career plans"],
                    crisis_indicators=social_pressure_day and relapse_risk > 0.7,
                    engagement_level=max(1, min(10, 9 - relapse_risk * 2))
                )
                data["chat"].append(asdict(chat))
            
            # Sobriety tracking
            sobriety = SobrietyData(
                date=date_str,
                days_sober=current_sobriety,
                relapse_risk_score=relapse_risk,
                in_treatment=True,
                medication_adherence=random.uniform(0.8, 0.95),  # Sometimes forgets
                meeting_attendance=random.randint(1, 3),  # College group + some AA
                relapse_occurred=relapse_occurred
            )
            data["sobriety"].append(asdict(sobriety))
            data["apple_watch"].append(asdict(apple_watch))
        
        return data
    
    def generate_robert_data(self) -> Dict[str, Any]:
        """Generate data for Robert Williams - Empty Nester"""
        data = {
            "persona": "Robert Williams",
            "persona_type": "empty_nester",
            "apple_watch": [],
            "phq5": [],
            "mood_diary": [],
            "chat": [],
            "sobriety": []
        }
        
        # Robert starts with 90 days sober
        initial_sobriety = 90
        current_sobriety = initial_sobriety
        
        for day in range(180):
            current_date = self.start_date + timedelta(days=day)
            date_str = current_date.strftime("%Y-%m-%d")
            
            current_sobriety += 1
            relapse_risk = self.calculate_relapse_risk(current_sobriety)
            
            # Loneliness and health issues
            lonely_day = random.random() < 0.4  # Frequent loneliness
            high_pain_day = random.random() < 0.5  # Chronic back pain
            diabetes_spike = random.random() < 0.2  # Blood sugar issues
            court_date = day % 30 == 0  # Monthly court check-ins
            
            if lonely_day:
                relapse_risk *= 1.3
            
            relapse_occurred = random.random() < relapse_risk * 0.01  # Lower due to court supervision
            if relapse_occurred and current_sobriety > 30:
                current_sobriety = random.randint(1, 10)
            
            # Apple Watch Data - depression and health monitoring
            base_resting_hr = 70 + (8 if diabetes_spike else 0) + (5 if high_pain_day else 0)
            resting_hr = self.add_noise(base_resting_hr)
            avg_hr = resting_hr + random.randint(8, 15)  # Less active
            
            # HRV affected by depression and health
            base_hrv = 25 - (5 if lonely_day else 0) - (3 if high_pain_day else 0)
            hrv = self.add_noise(base_hrv)
            
            # Sleep - long duration but poor quality
            sleep_duration = self.add_noise(8.5 + (1 if lonely_day else 0), 0.2)
            sleep_efficiency = self.add_noise(68 - (8 if lonely_day else 0), 0.15)
            
            # Low activity baseline
            steps = random.randint(1500, 4000) + (1000 if random.random() < 0.3 else 0)  # Occasional walks
            
            apple_watch = AppleWatchData(
                date=date_str,
                heart_rate_avg=avg_hr,
                heart_rate_resting=resting_hr,
                heart_rate_variability=hrv,
                sleep_duration_hours=min(12, sleep_duration),
                sleep_efficiency=sleep_efficiency,
                deep_sleep_hours=self.add_noise(sleep_duration * 0.15),
                rem_sleep_hours=self.add_noise(sleep_duration * 0.18),
                steps=int(steps),
                active_calories=random.randint(100, 250),
                exercise_minutes=random.randint(0, 20) if random.random() < 0.2 else 0,
                stand_hours=random.randint(4, 8),
                stress_score=random.randint(50, 80) if lonely_day else random.randint(30, 60)
            )
            
            # PHQ-5 responses (bi-weekly, focuses on physical symptoms)
            if day % 14 == 0:
                lonely_modifier = 2 if lonely_day else 0
                pain_modifier = 1 if high_pain_day else 0
                
                # Robert under-reports emotional symptoms, over-reports physical
                little_interest = min(3, max(0, 3 + lonely_modifier - (current_sobriety // 90)))
                feeling_down = min(3, max(0, 2 + lonely_modifier - (current_sobriety // 60)))
                sleep_trouble = min(3, max(0, 2 + pain_modifier))
                tired_energy = min(3, max(0, 3 + pain_modifier + lonely_modifier - (current_sobriety // 45)))
                appetite = min(3, max(0, 1 + lonely_modifier))
                
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
            
            # Mood diary (minimal entries, gaps during depression)
            if random.random() < (0.4 if lonely_day else 0.6):
                triggers = []
                if lonely_day:
                    triggers.extend(["isolation", "missing family"])
                if high_pain_day:
                    triggers.append("back pain")
                if court_date:
                    triggers.append("court stress")
                
                coping_strategies = ["TV", "medication", "nap"] if triggers else ["routine", "walk", "call kids"]
                
                mood_entry = MoodDiaryEntry(
                    date=date_str,
                    mood_rating=max(1, min(10, 5 - relapse_risk * 2 - len(triggers))),
                    anxiety_level=max(1, min(10, 4 + len(triggers) + (2 if court_date else 0))),
                    craving_intensity=max(0, min(10, relapse_risk * 5 + len(triggers) * 2)),
                    energy_level=max(1, min(10, 4 - len(triggers) - (2 if lonely_day else 0))),
                    sleep_quality=max(1, min(10, sleep_efficiency / 10)),
                    pain_level=random.randint(6, 8) if high_pain_day else random.randint(3, 6),
                    triggers=triggers,
                    coping_strategies=coping_strategies,
                    notes=f"{current_sobriety} days. {'Rough day' if triggers else 'Getting by'}",
                    word_count=random.randint(5, 25)  # Very brief
                )
                data["mood_diary"].append(asdict(mood_entry))
            
            # Chat interactions (2-3 times per week, structured)
            if random.random() < 0.35:
                chat = ChatInteraction(
                    date=date_str,
                    time=f"{random.randint(14, 18):02d}:{random.randint(0, 59):02d}",  # Afternoon
                    message_count=random.randint(1, 4),
                    avg_response_time_hours=random.uniform(4, 24),
                    sentiment_score=max(-0.8, min(0.3, -0.1 - relapse_risk - len(triggers) * 0.3)),
                    topics=["court requirements", "health", "loneliness"] if triggers else ["routine", "medication", "progress"],
                    crisis_indicators=lonely_day and relapse_risk > 0.4,
                    engagement_level=max(1, min(10, 5 - relapse_risk * 2))
                )
                data["chat"].append(asdict(chat))
            
            # Sobriety tracking
            sobriety = SobrietyData(
                date=date_str,
                days_sober=current_sobriety,
                relapse_risk_score=relapse_risk,
                in_treatment=True,
                medication_adherence=random.uniform(0.95, 0.99),  # Excellent at medication
                meeting_attendance=random.randint(2, 4),  # Court-mandated meetings
                relapse_occurred=relapse_occurred
            )
            data["sobriety"].append(asdict(sobriety))
            data["apple_watch"].append(asdict(apple_watch))
        
        return data
    
    def generate_all_personas(self) -> Dict[str, Any]:
        """Generate data for all personas"""
        print("Generating synthetic data for all personas...")
        
        all_data = {
            "generation_info": {
                "start_date": self.start_date.strftime("%Y-%m-%d"),
                "days_generated": 180,
                "random_seed": self.random_seed,
                "generation_timestamp": datetime.now().isoformat()
            },
            "personas": {}
        }
        
        # Generate data for each persona
        personas = [
            ("sarah_chen", self.generate_sarah_data),
            ("marcus_rodriguez", self.generate_marcus_data),
            ("jessica_thompson", self.generate_jessica_data),
            ("robert_williams", self.generate_robert_data)
        ]
        
        for persona_id, generator_func in personas:
            print(f"Generating data for {persona_id}...")
            all_data["personas"][persona_id] = generator_func()
        
        return all_data
    
    def save_data(self, data: Dict[str, Any], filename: str = "synthetic_patient_data.json"):
        """Save generated data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {filename}")
        
        # Also save summary statistics
        self.generate_summary_stats(data, filename.replace('.json', '_summary.json'))
    
    def generate_summary_stats(self, data: Dict[str, Any], filename: str):
        """Generate summary statistics for the dataset"""
        summary = {
            "dataset_info": data["generation_info"],
            "persona_summaries": {}
        }
        
        for persona_id, persona_data in data["personas"].items():
            persona_summary = {
                "persona_name": persona_data["persona"],
                "persona_type": persona_data["persona_type"],
                "data_points": {
                    "apple_watch_records": len(persona_data["apple_watch"]),
                    "phq5_assessments": len(persona_data["phq5"]),
                    "mood_diary_entries": len(persona_data["mood_diary"]),
                    "chat_interactions": len(persona_data["chat"]),
                    "sobriety_records": len(persona_data["sobriety"])
                },
                "sobriety_stats": {
                    "initial_days_sober": persona_data["sobriety"][0]["days_sober"],
                    "final_days_sober": persona_data["sobriety"][-1]["days_sober"],
                    "relapses_occurred": sum(1 for s in persona_data["sobriety"] if s["relapse_occurred"]),
                    "avg_relapse_risk": np.mean([s["relapse_risk_score"] for s in persona_data["sobriety"]]),
                    "avg_medication_adherence": np.mean([s["medication_adherence"] for s in persona_data["sobriety"]])
                },
                "health_metrics": {
                    "avg_resting_hr": np.mean([w["heart_rate_resting"] for w in persona_data["apple_watch"]]),
                    "avg_hrv": np.mean([w["heart_rate_variability"] for w in persona_data["apple_watch"]]),
                    "avg_sleep_duration": np.mean([w["sleep_duration_hours"] for w in persona_data["apple_watch"]]),
                    "avg_steps": np.mean([w["steps"] for w in persona_data["apple_watch"]])
                }
            }
            
            if persona_data["phq5"]:
                persona_summary["mental_health"] = {
                    "avg_phq5_score": np.mean([p["total_score"] for p in persona_data["phq5"]]),
                    "phq5_assessments_completed": len(persona_data["phq5"])
                }
            
            summary["persona_summaries"][persona_id] = persona_summary
        
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"Summary statistics saved to {filename}")

if __name__ == "__main__":
    generator = PersonaDataGenerator(start_date="2024-01-01")
    all_data = generator.generate_all_personas()
    generator.save_data(all_data, "data/synthetic_patient_data.json")
    
    print("\n" + "="*50)
    print("SYNTHETIC DATA GENERATION COMPLETE")
    print("="*50)
    print(f"Generated 180 days of data for 4 personas")
    print(f"Total records generated:")
    
    total_records = 0
    for persona_id, persona_data in all_data["personas"].items():
        persona_total = (len(persona_data["apple_watch"]) + 
                        len(persona_data["phq5"]) + 
                        len(persona_data["mood_diary"]) + 
                        len(persona_data["chat"]) + 
                        len(persona_data["sobriety"]))
        print(f"  {persona_data['persona']}: {persona_total:,} records")
        total_records += persona_total
    
    print(f"\nGrand Total: {total_records:,} synthetic data points")
    print("Files created:")
    print("  - data/synthetic_patient_data.json (full dataset)")
    print("  - data/synthetic_patient_data_summary.json (summary statistics)") 