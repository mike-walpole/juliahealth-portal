import { db } from '$lib/db/connection.js';
import { personas, sobrietyData, chatInteractions, appleWatchData, moodDiaryEntries, phq5Responses } from '$lib/db/schema.js';
import { eq, desc, and, gte } from 'drizzle-orm';

export async function load() {
	try {
		// Get all personas with their latest data
		const allPersonas = await db.select().from(personas);
		
		const patientsWithData = await Promise.all(
			allPersonas.map(async (persona) => {
				// Latest sobriety data
				const latestSobriety = await db
					.select()
					.from(sobrietyData)
					.where(eq(sobrietyData.persona_id, persona.id))
					.orderBy(desc(sobrietyData.date))
					.limit(1);
				
				// Recent chat activity (last 7 days)
				const recentChats = await db
					.select()
					.from(chatInteractions)
					.where(eq(chatInteractions.persona_id, persona.id))
					.orderBy(desc(chatInteractions.date))
					.limit(10);
				
				// Latest Apple Watch data
				const latestWatch = await db
					.select()
					.from(appleWatchData)
					.where(eq(appleWatchData.persona_id, persona.id))
					.orderBy(desc(appleWatchData.date))
					.limit(1);
				
				// Recent mood entries
				const recentMoods = await db
					.select()
					.from(moodDiaryEntries)
					.where(eq(moodDiaryEntries.persona_id, persona.id))
					.orderBy(desc(moodDiaryEntries.date))
					.limit(5);
				
				// Latest PHQ-5 score
				const latestPHQ5 = await db
					.select()
					.from(phq5Responses)
					.where(eq(phq5Responses.persona_id, persona.id))
					.orderBy(desc(phq5Responses.date))
					.limit(1);
				
				// Risk trend (last 30 days)
				const riskTrend = await db
					.select({
						date: sobrietyData.date,
						risk_score: sobrietyData.relapse_risk_score,
						days_sober: sobrietyData.days_sober
					})
					.from(sobrietyData)
					.where(eq(sobrietyData.persona_id, persona.id))
					.orderBy(desc(sobrietyData.date))
					.limit(30);
				
				// Calculate engagement metrics
				const avgSentiment = recentChats.length > 0 
					? recentChats.reduce((sum, chat) => sum + chat.sentiment_score, 0) / recentChats.length
					: 0;
				
				const crisisCount = recentChats.filter(chat => chat.crisis_indicators).length;
				
				return {
					...persona,
					currentRisk: latestSobriety[0]?.relapse_risk_score || 0,
					daysSober: latestSobriety[0]?.days_sober || 0,
					lastUpdate: latestSobriety[0]?.date || null,
					inTreatment: latestSobriety[0]?.in_treatment || false,
					medicationAdherence: latestSobriety[0]?.medication_adherence || 0,
					meetingAttendance: latestSobriety[0]?.meeting_attendance || 0,
					
					// Chat metrics
					totalChats: recentChats.length,
					avgSentiment: avgSentiment,
					crisisIndicators: crisisCount,
					lastChatDate: recentChats[0]?.date || null,
					
					// Biometric data
					currentStress: latestWatch[0]?.stress_score || 0,
					restingHR: latestWatch[0]?.heart_rate_resting || 0,
					hrv: latestWatch[0]?.heart_rate_variability || 0,
					sleepHours: latestWatch[0]?.sleep_duration_hours || 0,
					sleepEfficiency: latestWatch[0]?.sleep_efficiency || 0,
					
					// Mood data
					currentMood: recentMoods[0]?.mood_rating || 0,
					currentAnxiety: recentMoods[0]?.anxiety_level || 0,
					currentCravings: recentMoods[0]?.craving_intensity || 0,
					lastMoodEntry: recentMoods[0]?.date || null,
					
					// PHQ-5 score
					phq5Score: latestPHQ5[0]?.total_score || null,
					phq5Date: latestPHQ5[0]?.date || null,
					
					// Risk trend
					riskTrend: riskTrend.reverse() // Oldest to newest for charting
				};
			})
		);
		
		// Sort by risk score (highest first)
		patientsWithData.sort((a, b) => b.currentRisk - a.currentRisk);
		
		return {
			patients: patientsWithData
		};
	} catch (error) {
		console.error('Patients data loading error:', error);
		return {
			patients: []
		};
	}
} 