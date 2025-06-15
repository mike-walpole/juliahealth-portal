import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import { eq, desc, and, gte } from 'drizzle-orm';
import 'dotenv/config';

import { 
  personas, 
  appleWatchData, 
  phq5Responses, 
  moodDiaryEntries, 
  chatInteractions, 
  sobrietyData 
} from './schema.js';

// Database connection
const connectionString = process.env.DATABASE_URL;
const sql = postgres(connectionString);
const db = drizzle(sql);

async function verifyData() {
  try {
    console.log('🔍 Verifying exported data...\n');

    // 1. Get all personas
    console.log('👥 PERSONAS:');
    const allPersonas = await db.select().from(personas);
    allPersonas.forEach(persona => {
      console.log(`  ${persona.id}: ${persona.name} (${persona.persona_type})`);
    });
    console.log();

    // 2. Sarah's relapse analysis
    console.log('🚨 SARAH\'S RELAPSE ANALYSIS:');
    const sarah = allPersonas.find(p => p.name === 'Sarah Chen');
    if (sarah) {
      // Get relapse events
      const relapses = await db
        .select()
        .from(sobrietyData)
        .where(and(
          eq(sobrietyData.persona_id, sarah.id),
          eq(sobrietyData.relapse_occurred, true)
        ));

      console.log(`  Relapse events: ${relapses.length}`);
      relapses.forEach(relapse => {
        console.log(`    Date: ${relapse.date}, Days sober: ${relapse.days_sober}, Risk: ${relapse.relapse_risk_score.toFixed(3)}`);
      });

      // Get high-risk days (>0.8)
      const highRiskDays = await db
        .select()
        .from(sobrietyData)
        .where(and(
          eq(sobrietyData.persona_id, sarah.id),
          gte(sobrietyData.relapse_risk_score, 0.8)
        ))
        .orderBy(sobrietyData.date);

      console.log(`  High-risk days (>0.8): ${highRiskDays.length}`);
      highRiskDays.slice(0, 5).forEach(day => {
        console.log(`    ${day.date}: ${day.days_sober} days sober, risk=${day.relapse_risk_score.toFixed(3)}`);
      });
    }
    console.log();

    // 3. Chat engagement by persona
    console.log('💬 CHAT ENGAGEMENT BY PERSONA:');
    for (const persona of allPersonas) {
      const chatCount = await db
        .select()
        .from(chatInteractions)
        .where(eq(chatInteractions.persona_id, persona.id));
      
      const avgSentiment = chatCount.length > 0 
        ? chatCount.reduce((sum, chat) => sum + chat.sentiment_score, 0) / chatCount.length
        : 0;

      console.log(`  ${persona.name}: ${chatCount.length} chats, avg sentiment: ${avgSentiment.toFixed(3)}`);
    }
    console.log();

    // 4. Apple Watch stress correlation
    console.log('⌚ APPLE WATCH STRESS ANALYSIS:');
    for (const persona of allPersonas) {
      const watchData = await db
        .select()
        .from(appleWatchData)
        .where(eq(appleWatchData.persona_id, persona.id))
        .orderBy(desc(appleWatchData.stress_score))
        .limit(3);

      if (watchData.length > 0) {
        console.log(`  ${persona.name} - Top stress days:`);
        watchData.forEach(day => {
          console.log(`    ${day.date}: Stress=${day.stress_score.toFixed(1)}, HR=${day.heart_rate_resting.toFixed(0)}, HRV=${day.heart_rate_variability.toFixed(1)}`);
        });
      }
    }
    console.log();

    // 5. Sample complex query - Join sobriety with mood data
    console.log('🎯 SOBRIETY vs MOOD CORRELATION:');
    const sarahMoodSobriety = await db
      .select({
        date: sobrietyData.date,
        days_sober: sobrietyData.days_sober,
        risk_score: sobrietyData.relapse_risk_score,
        mood_rating: moodDiaryEntries.mood_rating,
        craving_intensity: moodDiaryEntries.craving_intensity
      })
      .from(sobrietyData)
      .innerJoin(moodDiaryEntries, eq(sobrietyData.date, moodDiaryEntries.date))
      .where(eq(sobrietyData.persona_id, sarah.id))
      .orderBy(desc(sobrietyData.relapse_risk_score))
      .limit(5);

    console.log('  Sarah\'s highest risk days with mood data:');
    sarahMoodSobriety.forEach(day => {
      console.log(`    ${day.date}: Risk=${day.risk_score.toFixed(3)}, Mood=${day.mood_rating.toFixed(1)}, Craving=${day.craving_intensity.toFixed(1)}, Sober=${day.days_sober}d`);
    });

    console.log('\n✅ Data verification complete!');
    console.log('\n📋 AVAILABLE TABLES:');
    console.log('  - personas: Patient profiles');
    console.log('  - apple_watch_data: Biometric data');
    console.log('  - phq5_responses: Depression screening');
    console.log('  - mood_diary_entries: Daily mood tracking');
    console.log('  - chat_interactions: AI chat logs');
    console.log('  - sobriety_data: Recovery tracking with risk scores');

  } catch (error) {
    console.error('❌ Verification failed:', error);
  } finally {
    await sql.end();
  }
}

verifyData(); 