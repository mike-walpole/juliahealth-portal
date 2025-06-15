# JuliaHealth Patient App

A comprehensive React Native Expo app for patients in addiction recovery treatment, designed to work alongside the JuliaHealth clinician dashboard.

## Features

### 🏠 Dashboard
- **Recovery Progress**: Days sober counter with risk assessment
- **Health Overview**: Real-time biometric data from Apple Watch
- **Mental Health Tracking**: Mood, anxiety, and craving levels
- **Quick Actions**: Mood logging and chat access
- **Emergency Support**: Crisis hotline and emergency contacts

### 💚 Health Tracking
- **Biometric Monitoring**: Heart rate, HRV, sleep, stress levels
- **Activity Tracking**: Steps, calories, exercise minutes
- **Mental Health Metrics**: Mood, anxiety, cravings, energy
- **Mood Diary**: Interactive logging with sentiment analysis
- **PHQ-5 Assessment**: Depression screening questionnaire
- **Sleep Analysis**: Duration, efficiency, deep sleep, REM sleep

### 💬 AI Chat (Julia)
- **24/7 AI Companion**: Intelligent responses based on recovery context
- **Crisis Detection**: Automatic alerts for concerning messages
- **Sentiment Analysis**: Real-time mood tracking through conversations
- **Quick Responses**: Pre-built buttons for common check-ins
- **Category Recognition**: Specialized responses for cravings, stress, sleep, etc.
- **Chat History**: Persistent conversation storage

### 👤 Profile & Settings
- **Recovery Journey**: Sobriety tracking with milestone progress
- **Treatment Information**: Program details, counselor contact
- **Goals & Achievements**: Personal recovery milestones
- **Emergency Contacts**: Quick access to support network
- **Privacy Settings**: Data sharing and notification preferences

## Database Integration

The app matches all database fields from the clinician portal:

### Apple Watch Data
- Heart rate (average, resting, variability)
- Sleep metrics (duration, efficiency, deep sleep, REM)
- Activity data (steps, calories, exercise, stand hours)
- Stress scores

### Mood Diary Entries
- Mood rating (1-10)
- Anxiety level (1-10)
- Craving intensity (1-10)
- Energy level (1-10)
- Sleep quality (1-10)
- Pain level (1-10)
- Triggers and coping strategies
- Daily notes

### PHQ-5 Responses
- Little interest in activities
- Feeling down/depressed
- Sleep troubles
- Tired/low energy
- Appetite changes
- Total depression score

### Chat Interactions
- Message sentiment analysis
- Crisis indicator detection
- Topic categorization
- Engagement level tracking

### Sobriety Data
- Days sober tracking
- Relapse risk assessment
- Treatment participation
- Medication adherence
- Meeting attendance

## Technology Stack

- **Framework**: React Native with Expo
- **Navigation**: Expo Router with tabs
- **Chat**: React Native Gifted Chat
- **Storage**: AsyncStorage for local data persistence
- **UI**: Custom themed components with Tailwind-inspired styling
- **Icons**: SF Symbols via IconSymbol component

## Key Features

### 🍎 Apple Health Integration
- **Automatic Data Sync**: Real-time biometric data from Apple Watch and iPhone
- **Comprehensive Health Metrics**: Heart rate, HRV, sleep, activity, and more
- **Mindfulness Logging**: Write meditation sessions back to Apple Health
- **Privacy Controls**: User-controlled data sharing and sync preferences
- **Seamless Experience**: One-tap connection with proper permission handling

### Intelligent Chat System
- **Crisis Detection**: Monitors for keywords indicating self-harm or relapse
- **Contextual Responses**: Tailored advice based on message content
- **Recovery-Focused**: HALT technique, breathing exercises, sponsor reminders
- **Sentiment Tracking**: Analyzes emotional state through conversation

### Health Data Synchronization
- Real-time biometric monitoring from Apple Health
- Comprehensive mood tracking
- Sleep and activity analysis
- Mental health assessments

### Emergency Support
- One-tap crisis hotline access (988)
- Emergency contact integration
- Counselor communication
- Crisis alert system

### Privacy & Security
- Local data storage with AsyncStorage
- Configurable data sharing preferences
- HIPAA-compliant design considerations
- User-controlled privacy settings

## Getting Started

```bash
# Install dependencies
npm install

# Start the development server
npm start

# Run on iOS
npm run ios

# Run on Android
npm run android
```

## App Structure

```
app/
├── (tabs)/
│   ├── index.tsx          # Dashboard screen
│   ├── health.tsx         # Health tracking
│   ├── chat.tsx           # AI chat interface
│   └── profile.tsx        # Profile & settings
└── _layout.tsx            # Root layout

components/
├── ThemedText.tsx         # Themed text component
├── ThemedView.tsx         # Themed view component
└── ui/
    └── IconSymbol.tsx     # SF Symbols icons
```

## Data Flow

1. **Patient Input**: Users log mood, health data, and chat messages
2. **Local Storage**: Data persisted with AsyncStorage
3. **Analysis**: Real-time sentiment and crisis detection
4. **Sync**: Data can be shared with clinician dashboard (when enabled)
5. **Insights**: AI-powered responses and health score calculations

## Recovery-Focused Design

The app is specifically designed for addiction recovery with:
- **Trauma-informed UI**: Calming colors, clear navigation
- **Crisis-aware features**: Immediate support access
- **Progress visualization**: Motivational milestone tracking
- **Evidence-based tools**: HALT technique, breathing exercises
- **Peer support integration**: Group meeting reminders

## Future Enhancements

- Real-time data sync with clinician portal
- Push notifications for medication reminders
- Integration with wearable devices
- Peer support group features
- Telehealth appointment scheduling
- Medication tracking and adherence monitoring

---

Built with ❤️ for the recovery community
