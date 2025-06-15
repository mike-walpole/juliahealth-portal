# JuliaHealth Database Setup - Neon Postgres

## 🎯 Overview
Successfully exported **3,986 synthetic patient records** to Neon Postgres using Drizzle ORM.

## 📊 Data Summary
- **4 Patient Personas** with realistic addiction recovery patterns
- **720 Apple Watch records** (biometric data)
- **26 PHQ-5 responses** (depression screening)
- **526 Mood diary entries** (daily tracking)
- **1,994 Chat interactions** (AI conversations)
- **720 Sobriety records** (risk scores & relapse events)

## 🔗 Connection Details
```
Database: Neon Postgres
URL: postgresql://juliademo_owner:npg_erUVoa0FZA5C@ep-calm-mode-a2mzhtqt-pooler.eu-central-1.aws.neon.tech/juliademo?sslmode=require
```

## 📋 Database Schema

### Tables Created:
1. **`personas`** - Patient profiles
2. **`apple_watch_data`** - Biometric data (HR, HRV, sleep, steps)
3. **`phq5_responses`** - Depression screening questionnaires
4. **`mood_diary_entries`** - Daily mood tracking with triggers/coping
5. **`chat_interactions`** - AI chat logs with sentiment analysis
6. **`sobriety_data`** - Recovery tracking with risk scores

## 🚨 Key Clinical Features

### Sarah Chen - Relapse Event Analysis
- **1 Relapse Event**: June 4, 2024 (Day 155)
- **Risk Score Spike**: 0.422 → 0.900 after relapse
- **20 High-Risk Days** (>0.8 risk score)
- **Clinically Accurate**: Risk properly elevates after relapse

### Persona Risk Profiles:
- **Sarah Chen**: 0.505 avg risk (work stress + relapse)
- **Jessica Thompson**: 0.461 avg risk (college pressures)
- **Robert Williams**: 0.316 avg risk (stable retirement)
- **Marcus Rodriguez**: 0.213 avg risk (veteran, longest sobriety)

## 💻 Usage Examples

### Connect with Drizzle:
```javascript
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';

const sql = postgres(process.env.DATABASE_URL);
const db = drizzle(sql);
```

### Sample Queries:

#### Get High-Risk Patients:
```javascript
const highRisk = await db
  .select()
  .from(sobrietyData)
  .where(gte(sobrietyData.relapse_risk_score, 0.8))
  .orderBy(desc(sobrietyData.relapse_risk_score));
```

#### Relapse Analysis:
```javascript
const relapses = await db
  .select()
  .from(sobrietyData)
  .where(eq(sobrietyData.relapse_occurred, true));
```

#### Biometric Correlations:
```javascript
const stressData = await db
  .select({
    date: appleWatchData.date,
    stress: appleWatchData.stress_score,
    hr: appleWatchData.heart_rate_resting,
    risk: sobrietyData.relapse_risk_score
  })
  .from(appleWatchData)
  .innerJoin(sobrietyData, eq(appleWatchData.date, sobrietyData.date));
```

## 🛠 Available Scripts
```bash
npm run export    # Export JSON data to database
npm run verify    # Verify data and run sample queries
npm run db:push   # Push schema changes
```

## 📈 Clinical Validation Features

### ✅ Realistic Risk Modeling:
- **AR(1) time series** with persistence
- **Regime-switching** stress patterns
- **Proper relapse handling** with risk spikes
- **Sobriety-based baseline** risk calculation

### ✅ Correlated Biomarkers:
- Heart rate ↑ when stress ↑
- HRV ↓ when stress ↑
- Sleep quality ↓ during high-risk periods
- Mood ratings inversely correlated with risk

### ✅ Behavioral Patterns:
- Chat engagement ↑ during crisis
- Sentiment ↓ after relapse events
- Trigger identification in mood diaries
- Coping strategy usage tracking

## 🎯 Use Cases
- **Algorithm Training**: ML models for relapse prediction
- **Clinical Validation**: Test intervention timing
- **Investor Demos**: Show sophisticated risk modeling
- **Regulatory Submissions**: HIPAA-compliant synthetic data
- **Research Studies**: Addiction treatment effectiveness

## 🔒 Data Privacy
All data is **100% synthetic** - no real patient information used. Safe for:
- Development environments
- Public demonstrations
- Academic research
- Algorithm training
- Regulatory compliance testing 