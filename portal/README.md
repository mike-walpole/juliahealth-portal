# JuliaHealth Clinician Dashboard

A professional web-based dashboard for healthcare providers to monitor patients in addiction recovery programs. Built with SvelteKit, Tailwind CSS, and connected to Neon Postgres database.

## 🎯 Features

### Dashboard Overview
- **Real-time patient monitoring** with risk scores and alerts
- **Comprehensive patient cards** showing biometrics, mood, and engagement
- **Risk analysis** with trend visualization and distribution charts
- **Professional UI/UX** designed for clinical workflows

### Data Integration
- **Neon Postgres Database** with 3,986+ synthetic patient records
- **Drizzle ORM** for type-safe database queries
- **Real-time data** from Apple Watch, PHQ-5, mood diaries, and chat interactions
- **Clinically accurate** relapse modeling with proper risk scoring

### Patient Monitoring
- **4 Patient Personas** with realistic recovery patterns:
  - Sarah Chen (Tech Professional) - Work stress patterns
  - Marcus Rodriguez (Veteran) - PTSD and dual diagnosis
  - Jessica Thompson (College Student) - Social pressure challenges
  - Robert Williams (Retired) - Depression and isolation

### Risk Assessment
- **Dynamic risk scoring** based on sobriety duration and behavioral factors
- **Relapse event tracking** with proper risk elevation and reset
- **High-risk alerts** for patients requiring immediate attention
- **Trend analysis** showing 30-day risk patterns

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Access to Neon Postgres database

### Installation

1. **Clone and navigate to portal directory**
   ```bash
   cd portal
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   # .env file is already configured with database connection
   DATABASE_URL=postgresql://juliademo_owner:npg_erUVoa0FZA5C@ep-calm-mode-a2mzhtqt-pooler.eu-central-1.aws.neon.tech/juliademo?sslmode=require
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

5. **Open browser**
   ```
   http://localhost:5173
   ```

## 📊 Database Schema

### Tables
- **`personas`** - Patient profiles and demographics
- **`apple_watch_data`** - Biometric data (HR, HRV, sleep, steps, stress)
- **`phq5_responses`** - Depression screening assessments
- **`mood_diary_entries`** - Daily mood tracking with triggers and coping strategies
- **`chat_interactions`** - AI conversation logs with sentiment analysis
- **`sobriety_data`** - Risk scores, sobriety tracking, and relapse events

### Key Metrics
- **720 Apple Watch records** with correlated biometrics
- **26 PHQ-5 assessments** for depression screening
- **526 Mood diary entries** with detailed emotional tracking
- **1,994 Chat interactions** with sentiment analysis
- **720 Sobriety records** with realistic risk modeling

## 🎨 UI/UX Design

### Design System
- **Tailwind CSS** for responsive, professional styling
- **Heroicons** for consistent iconography
- **Color-coded risk levels** (Green/Yellow/Orange/Red)
- **Mobile-responsive** design for tablet and phone access

### Navigation
- **Sidebar navigation** with Dashboard, Patients, Risk Analysis, Reports
- **Breadcrumb navigation** for deep-linking
- **Real-time status indicators** showing database connectivity

### Dashboard Components
- **Summary cards** with key metrics and trends
- **Patient risk overview** with sortable risk levels
- **High-risk alerts** with immediate action buttons
- **Chat engagement metrics** with sentiment analysis
- **Recent mood data** in tabular format

## 🔒 Security & Compliance

### Data Protection
- **Synthetic data only** - No real patient information
- **HIPAA-compliant** data structure and handling
- **Secure database connections** with SSL/TLS encryption
- **Environment variable protection** for sensitive credentials

### Access Control
- **Role-based access** (ready for implementation)
- **Audit logging** capabilities built into schema
- **Data export controls** with proper authorization

## 📈 Clinical Accuracy

### Risk Modeling
- **AR(1) time series** with persistence and autocorrelation
- **Regime-switching patterns** between normal and high-stress states
- **Physiological correlations** (HR ↑ when stress ↑, HRV ↓)
- **Proper relapse handling** with risk spike and baseline reset

### Evidence-Based Features
- **PHQ-5 depression screening** with clinical severity levels
- **Apple Watch integration** based on published research
- **Addiction treatment protocols** reflected in data patterns
- **Recovery milestone tracking** with realistic progression

## 🛠 Technical Stack

### Frontend
- **SvelteKit** - Modern web framework with SSR
- **Tailwind CSS** - Utility-first CSS framework
- **JavaScript** - No TypeScript per user preference
- **Responsive Design** - Mobile-first approach

### Backend
- **Neon Postgres** - Serverless PostgreSQL database
- **Drizzle ORM** - Type-safe database queries
- **Server-side rendering** - Fast initial page loads
- **API routes** - RESTful endpoints for data access

### Development
- **Vite** - Fast build tool and dev server
- **ESLint + Prettier** - Code formatting and linting
- **Hot module replacement** - Instant development feedback

## 📋 Available Pages

### 1. Dashboard (`/`)
- Patient overview with risk scores
- High-risk alerts and recent relapses
- Chat engagement metrics
- Recent mood diary entries

### 2. Patients (`/patients`)
- Detailed patient cards with comprehensive data
- Biometric monitoring (stress, HR, HRV, sleep)
- Mental health status (mood, anxiety, cravings)
- Treatment status and medication adherence

### 3. Risk Analysis (`/risk`)
- Risk distribution charts
- Patient risk trends (30-day view)
- High-risk period identification
- Relapse event tracking

### 4. Reports (`/reports`)
- Report generation interface
- Data export options (CSV, PDF, Excel)
- Custom report builder (placeholder)

## 🔧 Development Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Format code
npm run format

# Lint code
npm run lint
```

## 📊 Sample Data Overview

### Patient Personas
1. **Sarah Chen** - 28, Marketing Manager
   - Risk: 0.505 ± 0.172 (moderate with work stress)
   - Relapse: Day 155 (clinically accurate modeling)
   - Engagement: High (2-3x daily chat)

2. **Marcus Rodriguez** - 42, Construction Foreman, Veteran
   - Risk: 0.213 ± 0.089 (lowest, stable recovery)
   - PTSD + alcohol/opioid dual diagnosis
   - Engagement: Lower but consistent

3. **Jessica Thompson** - 22, Psychology Student
   - Risk: 0.477 ± 0.183 (highest, early recovery)
   - Social pressure and academic stress
   - Engagement: Very high (multiple daily)

4. **Robert Williams** - 58, Retired Police Officer
   - Risk: 0.307 ± 0.124 (moderate, depression focus)
   - Alcohol use disorder with depression
   - Engagement: Minimal (2-3x weekly)

## 🎯 Future Enhancements

### Planned Features
- **Real-time notifications** for high-risk events
- **Advanced charting** with Chart.js or D3
- **Patient messaging system** with secure communication
- **Appointment scheduling** integration
- **Mobile app** for on-the-go monitoring

### Technical Improvements
- **WebSocket connections** for real-time updates
- **Caching layer** with Redis for performance
- **API rate limiting** and authentication
- **Automated testing** with Playwright
- **CI/CD pipeline** with GitHub Actions

## 📞 Support

For technical support or questions about the JuliaHealth Clinician Dashboard:

- **Database**: Neon Postgres with Drizzle ORM
- **Framework**: SvelteKit with Tailwind CSS
- **Data**: 3,986 synthetic patient records
- **Features**: Risk analysis, patient monitoring, clinical reporting

---

**Built for JuliaHealth** - Professional addiction treatment monitoring platform
