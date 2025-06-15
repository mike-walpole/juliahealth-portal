import { pgTable, serial, text, integer, real, boolean, timestamp, jsonb, varchar } from 'drizzle-orm/pg-core';

// Personas table
export const personas = pgTable('personas', {
  id: serial('id').primaryKey(),
  name: varchar('name', { length: 100 }).notNull(),
  persona_type: varchar('persona_type', { length: 50 }).notNull(),
  created_at: timestamp('created_at').defaultNow(),
});

// Apple Watch data
export const appleWatchData = pgTable('apple_watch_data', {
  id: serial('id').primaryKey(),
  persona_id: integer('persona_id').references(() => personas.id),
  date: varchar('date', { length: 10 }).notNull(),
  heart_rate_avg: real('heart_rate_avg').notNull(),
  heart_rate_resting: real('heart_rate_resting').notNull(),
  heart_rate_variability: real('heart_rate_variability').notNull(),
  sleep_duration_hours: real('sleep_duration_hours').notNull(),
  sleep_efficiency: real('sleep_efficiency').notNull(),
  deep_sleep_hours: real('deep_sleep_hours').notNull(),
  rem_sleep_hours: real('rem_sleep_hours').notNull(),
  steps: integer('steps').notNull(),
  active_calories: integer('active_calories').notNull(),
  exercise_minutes: integer('exercise_minutes').notNull(),
  stand_hours: integer('stand_hours').notNull(),
  stress_score: real('stress_score').notNull(),
});

// PHQ-5 responses
export const phq5Responses = pgTable('phq5_responses', {
  id: serial('id').primaryKey(),
  persona_id: integer('persona_id').references(() => personas.id),
  date: varchar('date', { length: 10 }).notNull(),
  little_interest: integer('little_interest').notNull(),
  feeling_down: integer('feeling_down').notNull(),
  sleep_trouble: integer('sleep_trouble').notNull(),
  tired_energy: integer('tired_energy').notNull(),
  appetite: integer('appetite').notNull(),
  total_score: integer('total_score').notNull(),
});

// Mood diary entries
export const moodDiaryEntries = pgTable('mood_diary_entries', {
  id: serial('id').primaryKey(),
  persona_id: integer('persona_id').references(() => personas.id),
  date: varchar('date', { length: 10 }).notNull(),
  mood_rating: real('mood_rating').notNull(),
  anxiety_level: real('anxiety_level').notNull(),
  craving_intensity: real('craving_intensity').notNull(),
  energy_level: real('energy_level').notNull(),
  sleep_quality: real('sleep_quality').notNull(),
  pain_level: real('pain_level').notNull(),
  triggers: jsonb('triggers').notNull(),
  coping_strategies: jsonb('coping_strategies').notNull(),
  notes: text('notes').notNull(),
  word_count: integer('word_count').notNull(),
});

// Chat interactions
export const chatInteractions = pgTable('chat_interactions', {
  id: serial('id').primaryKey(),
  persona_id: integer('persona_id').references(() => personas.id),
  date: varchar('date', { length: 10 }).notNull(),
  time: varchar('time', { length: 5 }).notNull(),
  message_count: integer('message_count').notNull(),
  avg_response_time_hours: real('avg_response_time_hours').notNull(),
  sentiment_score: real('sentiment_score').notNull(),
  topics: jsonb('topics').notNull(),
  crisis_indicators: boolean('crisis_indicators').notNull(),
  engagement_level: real('engagement_level').notNull(),
});

// Sobriety data
export const sobrietyData = pgTable('sobriety_data', {
  id: serial('id').primaryKey(),
  persona_id: integer('persona_id').references(() => personas.id),
  date: varchar('date', { length: 10 }).notNull(),
  days_sober: integer('days_sober').notNull(),
  relapse_risk_score: real('relapse_risk_score').notNull(),
  in_treatment: boolean('in_treatment').notNull(),
  medication_adherence: real('medication_adherence').notNull(),
  meeting_attendance: integer('meeting_attendance').notNull(),
  relapse_occurred: boolean('relapse_occurred').notNull(),
}); 