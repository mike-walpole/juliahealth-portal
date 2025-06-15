import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import { readFileSync } from 'fs';
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

async function exportData() {
  try {
    console.log('🚀 Starting data export to Neon Postgres...\n');

    // Read synthetic data
    const rawData = readFileSync('./data/realistic_patient_data.json', 'utf8');
    const data = JSON.parse(rawData);

    console.log('📊 Data loaded:');
    console.log(`- Generation info: ${data.generation_info.total_records} total records`);
    console.log(`- Personas: ${Object.keys(data.personas).length}\n`);

    // Clear existing data (optional - comment out if you want to append)
    console.log('🧹 Clearing existing data...');
    await db.delete(sobrietyData);
    await db.delete(chatInteractions);
    await db.delete(moodDiaryEntries);
    await db.delete(phq5Responses);
    await db.delete(appleWatchData);
    await db.delete(personas);
    console.log('✅ Existing data cleared\n');

    // Insert personas first
    console.log('👥 Inserting personas...');
    const personaInserts = [];
    const personaMap = {};

    for (const [key, personaData] of Object.entries(data.personas)) {
      const personaName = personaData.persona;
      const personaType = personaData.persona_type;
      
      personaInserts.push({
        name: personaName,
        persona_type: personaType
      });
    }

    const insertedPersonas = await db.insert(personas).values(personaInserts).returning();
    
    // Create mapping from persona name to ID
    insertedPersonas.forEach((persona, index) => {
      const key = Object.keys(data.personas)[index];
      personaMap[key] = persona.id;
    });

    console.log(`✅ Inserted ${insertedPersonas.length} personas\n`);

    // Insert data for each persona
    for (const [key, personaData] of Object.entries(data.personas)) {
      const personaId = personaMap[key];
      const personaName = personaData.persona;
      
      console.log(`📱 Processing ${personaName}...`);

      // Apple Watch data
      if (personaData.apple_watch && personaData.apple_watch.length > 0) {
        const appleWatchInserts = personaData.apple_watch.map(record => ({
          persona_id: personaId,
          date: record.date,
          heart_rate_avg: record.heart_rate_avg,
          heart_rate_resting: record.heart_rate_resting,
          heart_rate_variability: record.heart_rate_variability,
          sleep_duration_hours: record.sleep_duration_hours,
          sleep_efficiency: record.sleep_efficiency,
          deep_sleep_hours: record.deep_sleep_hours,
          rem_sleep_hours: record.rem_sleep_hours,
          steps: record.steps,
          active_calories: record.active_calories,
          exercise_minutes: record.exercise_minutes,
          stand_hours: record.stand_hours,
          stress_score: record.stress_score
        }));

        await db.insert(appleWatchData).values(appleWatchInserts);
        console.log(`  ⌚ Apple Watch: ${appleWatchInserts.length} records`);
      }

      // PHQ-5 responses
      if (personaData.phq5 && personaData.phq5.length > 0) {
        const phq5Inserts = personaData.phq5.map(record => ({
          persona_id: personaId,
          date: record.date,
          little_interest: record.little_interest,
          feeling_down: record.feeling_down,
          sleep_trouble: record.sleep_trouble,
          tired_energy: record.tired_energy,
          appetite: record.appetite,
          total_score: record.total_score
        }));

        await db.insert(phq5Responses).values(phq5Inserts);
        console.log(`  📋 PHQ-5: ${phq5Inserts.length} records`);
      }

      // Mood diary entries
      if (personaData.mood_diary && personaData.mood_diary.length > 0) {
        const moodInserts = personaData.mood_diary.map(record => ({
          persona_id: personaId,
          date: record.date,
          mood_rating: record.mood_rating,
          anxiety_level: record.anxiety_level,
          craving_intensity: record.craving_intensity,
          energy_level: record.energy_level,
          sleep_quality: record.sleep_quality,
          pain_level: record.pain_level,
          triggers: record.triggers,
          coping_strategies: record.coping_strategies,
          notes: record.notes,
          word_count: record.word_count
        }));

        await db.insert(moodDiaryEntries).values(moodInserts);
        console.log(`  📝 Mood Diary: ${moodInserts.length} records`);
      }

      // Chat interactions
      if (personaData.chat && personaData.chat.length > 0) {
        const chatInserts = personaData.chat.map(record => ({
          persona_id: personaId,
          date: record.date,
          time: record.time,
          message_count: record.message_count,
          avg_response_time_hours: record.avg_response_time_hours,
          sentiment_score: record.sentiment_score,
          topics: record.topics,
          crisis_indicators: record.crisis_indicators,
          engagement_level: record.engagement_level
        }));

        await db.insert(chatInteractions).values(chatInserts);
        console.log(`  💬 Chat: ${chatInserts.length} records`);
      }

      // Sobriety data
      if (personaData.sobriety && personaData.sobriety.length > 0) {
        const sobrietyInserts = personaData.sobriety.map(record => ({
          persona_id: personaId,
          date: record.date,
          days_sober: record.days_sober,
          relapse_risk_score: record.relapse_risk_score,
          in_treatment: record.in_treatment,
          medication_adherence: record.medication_adherence,
          meeting_attendance: record.meeting_attendance,
          relapse_occurred: record.relapse_occurred
        }));

        await db.insert(sobrietyData).values(sobrietyInserts);
        console.log(`  🎯 Sobriety: ${sobrietyInserts.length} records`);
      }

      console.log(`✅ ${personaName} complete\n`);
    }

    // Summary query
    console.log('📈 Export Summary:');
    const totalPersonas = await db.select().from(personas);
    const totalAppleWatch = await db.select().from(appleWatchData);
    const totalPHQ5 = await db.select().from(phq5Responses);
    const totalMood = await db.select().from(moodDiaryEntries);
    const totalChat = await db.select().from(chatInteractions);
    const totalSobriety = await db.select().from(sobrietyData);

    console.log(`- Personas: ${totalPersonas.length}`);
    console.log(`- Apple Watch records: ${totalAppleWatch.length}`);
    console.log(`- PHQ-5 responses: ${totalPHQ5.length}`);
    console.log(`- Mood diary entries: ${totalMood.length}`);
    console.log(`- Chat interactions: ${totalChat.length}`);
    console.log(`- Sobriety records: ${totalSobriety.length}`);
    console.log(`- Total records: ${totalAppleWatch.length + totalPHQ5.length + totalMood.length + totalChat.length + totalSobriety.length}`);

    console.log('\n🎉 Data export completed successfully!');

  } catch (error) {
    console.error('❌ Export failed:', error);
    process.exit(1);
  } finally {
    await sql.end();
  }
}

exportData(); 