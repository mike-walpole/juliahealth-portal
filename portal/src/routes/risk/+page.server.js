import { db } from '$lib/db/connection.js';
import { personas, sobrietyData } from '$lib/db/schema.js';
import { eq, desc, gte, and } from 'drizzle-orm';

export async function load() {
	try {
		// Get all personas
		const allPersonas = await db.select().from(personas);
		
		// Get risk trends for all patients (last 30 days)
		const riskTrends = await Promise.all(
			allPersonas.map(async (persona) => {
				const trend = await db
					.select({
						date: sobrietyData.date,
						risk_score: sobrietyData.relapse_risk_score,
						days_sober: sobrietyData.days_sober,
						relapse_occurred: sobrietyData.relapse_occurred
					})
					.from(sobrietyData)
					.where(eq(sobrietyData.persona_id, persona.id))
					.orderBy(desc(sobrietyData.date))
					.limit(30);
				
				return {
					...persona,
					riskTrend: trend.reverse() // Oldest to newest for charting
				};
			})
		);
		
		// Get high-risk patients (risk >= 0.6)
		const highRiskPatients = await db
			.select({
				persona_id: sobrietyData.persona_id,
				name: personas.name,
				date: sobrietyData.date,
				risk_score: sobrietyData.relapse_risk_score,
				days_sober: sobrietyData.days_sober
			})
			.from(sobrietyData)
			.innerJoin(personas, eq(sobrietyData.persona_id, personas.id))
			.where(gte(sobrietyData.relapse_risk_score, 0.6))
			.orderBy(desc(sobrietyData.date))
			.limit(50);
		
		// Get relapse events
		const relapseEvents = await db
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
			.orderBy(desc(sobrietyData.date));
		
		// Calculate risk statistics
		const allRiskScores = await db
			.select({
				risk_score: sobrietyData.relapse_risk_score,
				days_sober: sobrietyData.days_sober
			})
			.from(sobrietyData);
		
		const avgRisk = allRiskScores.reduce((sum, r) => sum + r.risk_score, 0) / allRiskScores.length;
		const highRiskCount = allRiskScores.filter(r => r.risk_score >= 0.6).length;
		const criticalRiskCount = allRiskScores.filter(r => r.risk_score >= 0.8).length;
		
		return {
			riskTrends: riskTrends,
			highRiskPatients,
			relapseEvents,
			riskStats: {
				totalPatients: allPersonas.length,
				avgRisk: Math.round(avgRisk * 1000) / 1000,
				highRiskCount,
				criticalRiskCount
			}
		};
	} catch (error) {
		console.error('Risk analysis data loading error:', error);
		return {
			riskTrends: [],
			highRiskPatients: [],
			relapseEvents: [],
			riskStats: { 
				totalPatients: 0,
				avgRisk: 0, 
				highRiskCount: 0, 
				criticalRiskCount: 0 
			}
		};
	}
} 