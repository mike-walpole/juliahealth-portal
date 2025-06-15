import { db } from '$lib/db/connection.js';
import { personas, sobrietyData, chatInteractions, appleWatchData, moodDiaryEntries, phq5Responses } from '$lib/db/schema.js';
import { eq, desc, gte, and, sql } from 'drizzle-orm';

export async function load() {
	try {
		// Get all personas
		const allPersonas = await db.select().from(personas);
		
		// Get comprehensive patient data
		const patientsWithData = await Promise.all(
			allPersonas.map(async (persona) => {
				// Latest sobriety data
				const latestSobriety = await db
					.select()
					.from(sobrietyData)
					.where(eq(sobrietyData.persona_id, persona.id))
					.orderBy(desc(sobrietyData.date))
					.limit(1);
				
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
				
				return {
					...persona,
					currentRisk: latestSobriety[0]?.relapse_risk_score || 0,
					daysSober: latestSobriety[0]?.days_sober || 0,
					lastUpdate: latestSobriety[0]?.date || null,
					inTreatment: latestSobriety[0]?.in_treatment || false,
					medicationAdherence: latestSobriety[0]?.medication_adherence || 0,
					meetingAttendance: latestSobriety[0]?.meeting_attendance || 0,
					
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
					phq5Date: latestPHQ5[0]?.date || null
				};
			})
		);
		
		// Get high-risk patients (risk > 0.6)
		const highRiskPatients = await db
			.select({
				persona_id: sobrietyData.persona_id,
				name: personas.name,
				risk_score: sobrietyData.relapse_risk_score,
				days_sober: sobrietyData.days_sober,
				date: sobrietyData.date
			})
			.from(sobrietyData)
			.innerJoin(personas, eq(sobrietyData.persona_id, personas.id))
			.where(gte(sobrietyData.relapse_risk_score, 0.6))
			.orderBy(desc(sobrietyData.relapse_risk_score))
			.limit(10);
		
		// Get recent relapse events
		const recentRelapses = await db
			.select({
				persona_id: sobrietyData.persona_id,
				name: personas.name,
				date: sobrietyData.date,
				days_sober: sobrietyData.days_sober,
				risk_score: sobrietyData.relapse_risk_score
			})
			.from(sobrietyData)
			.innerJoin(personas, eq(sobrietyData.persona_id, personas.id))
			.where(eq(sobrietyData.relapse_occurred, true))
			.orderBy(desc(sobrietyData.date))
			.limit(5);
		
		// Get chat engagement stats
		const chatStats = await Promise.all(
			allPersonas.map(async (persona) => {
				const chats = await db
					.select()
					.from(chatInteractions)
					.where(eq(chatInteractions.persona_id, persona.id));
				
				const avgSentiment = chats.length > 0 
					? chats.reduce((sum, chat) => sum + chat.sentiment_score, 0) / chats.length
					: 0;
				
				const crisisCount = chats.filter(chat => chat.crisis_indicators).length;
				
				return {
					name: persona.name,
					totalChats: chats.length,
					avgSentiment: avgSentiment,
					crisisIndicators: crisisCount
				};
			})
		);
		
		// Get recent mood trends
		const recentMoodData = await db
			.select({
				persona_id: moodDiaryEntries.persona_id,
				name: personas.name,
				date: moodDiaryEntries.date,
				mood_rating: moodDiaryEntries.mood_rating,
				anxiety_level: moodDiaryEntries.anxiety_level,
				craving_intensity: moodDiaryEntries.craving_intensity
			})
			.from(moodDiaryEntries)
			.innerJoin(personas, eq(moodDiaryEntries.persona_id, personas.id))
			.orderBy(desc(moodDiaryEntries.date))
			.limit(20);
		
		// Calculate summary statistics
		const totalPatients = allPersonas.length;
		const highRiskCount = patientsWithData.filter(p => p.currentRisk > 0.6).length;
		const avgRisk = patientsWithData.reduce((sum, p) => sum + p.currentRisk, 0) / totalPatients;
		const totalRelapses = recentRelapses.length;
		
		// Sort patients by risk score (highest first)
		patientsWithData.sort((a, b) => b.currentRisk - a.currentRisk);
		
		return {
			summary: {
				totalPatients,
				highRiskCount,
				avgRisk: Math.round(avgRisk * 1000) / 1000,
				totalRelapses
			},
			patients: patientsWithData,
			highRiskPatients,
			recentRelapses,
			chatStats,
			recentMoodData
		};
	} catch (error) {
		console.error('Dashboard data loading error:', error);
		return {
			summary: { totalPatients: 0, highRiskCount: 0, avgRisk: 0, totalRelapses: 0 },
			patients: [],
			highRiskPatients: [],
			recentRelapses: [],
			chatStats: [],
			recentMoodData: []
		};
	}
} 