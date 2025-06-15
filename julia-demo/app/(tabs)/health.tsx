import React, { useState, useEffect } from 'react';
import { ScrollView, StyleSheet, View, Text, TouchableOpacity, Alert, TextInput, Modal } from 'react-native';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { IconSymbol } from '@/components/ui/IconSymbol';
import AsyncStorage from '@react-native-async-storage/async-storage';
import AppleHealthService from '../../services/AppleHealthService';

interface HealthData {
  // Apple Watch Data
  heartRateAvg: number;
  heartRateResting: number;
  heartRateVariability: number;
  sleepDurationHours: number;
  sleepEfficiency: number;
  deepSleepHours: number;
  remSleepHours: number;
  steps: number;
  activeCalories: number;
  exerciseMinutes: number;
  standHours: number;
  stressScore: number;
  
  // Mood Diary Data
  moodRating: number;
  anxietyLevel: number;
  cravingIntensity: number;
  energyLevel: number;
  sleepQuality: number;
  painLevel: number;
  triggers: string[];
  copingStrategies: string[];
  notes: string;
  
  // PHQ-5 Data
  phq5: {
    littleInterest: number;
    feelingDown: number;
    sleepTrouble: number;
    tiredEnergy: number;
    appetite: number;
    totalScore: number;
  };
  
  lastUpdate: string;
}

export default function HealthScreen() {
  const [healthData, setHealthData] = useState<HealthData>({
    // Apple Watch Data
    heartRateAvg: 75,
    heartRateResting: 68,
    heartRateVariability: 42,
    sleepDurationHours: 7.5,
    sleepEfficiency: 85,
    deepSleepHours: 1.8,
    remSleepHours: 1.2,
    steps: 8500,
    activeCalories: 420,
    exerciseMinutes: 35,
    standHours: 10,
    stressScore: 3.2,
    
    // Mood Diary Data
    moodRating: 7.2,
    anxietyLevel: 4.1,
    cravingIntensity: 2.8,
    energyLevel: 6.5,
    sleepQuality: 7.8,
    painLevel: 1.5,
    triggers: ['work stress', 'social situations'],
    copingStrategies: ['deep breathing', 'meditation', 'exercise'],
    notes: 'Feeling good today, managed stress well with breathing exercises.',
    
    // PHQ-5 Data
    phq5: {
      littleInterest: 1,
      feelingDown: 2,
      sleepTrouble: 1,
      tiredEnergy: 2,
      appetite: 1,
      totalScore: 7
    },
    
    lastUpdate: new Date().toLocaleDateString()
  });

  const [showMoodModal, setShowMoodModal] = useState(false);
  const [showPHQ5Modal, setShowPHQ5Modal] = useState(false);
  const [tempMoodData, setTempMoodData] = useState({
    mood: 5,
    anxiety: 5,
    cravings: 5,
    energy: 5,
    sleepQuality: 5,
    pain: 1,
    notes: ''
  });

  useEffect(() => {
    loadHealthData();
  }, []);

  const loadHealthData = async () => {
    try {
      const stored = await AsyncStorage.getItem('healthData');
      if (stored) {
        setHealthData(JSON.parse(stored));
      }
    } catch (error) {
      console.error('Error loading health data:', error);
    }
  };

  const saveHealthData = async (newData: HealthData) => {
    try {
      await AsyncStorage.setItem('healthData', JSON.stringify(newData));
      setHealthData(newData);
    } catch (error) {
      console.error('Error saving health data:', error);
    }
  };

  const handleMoodSubmit = async () => {
    const updatedData = {
      ...healthData,
      moodRating: tempMoodData.mood,
      anxietyLevel: tempMoodData.anxiety,
      cravingIntensity: tempMoodData.cravings,
      energyLevel: tempMoodData.energy,
      sleepQuality: tempMoodData.sleepQuality,
      painLevel: tempMoodData.pain,
      notes: tempMoodData.notes,
      lastUpdate: new Date().toLocaleDateString()
    };
    
    await saveHealthData(updatedData);
    setShowMoodModal(false);
    Alert.alert('Success', 'Your mood diary has been updated!');
  };

  const getHealthScore = () => {
    const scores = [
      healthData.moodRating / 10,
      (10 - healthData.anxietyLevel) / 10,
      (10 - healthData.cravingIntensity) / 10,
      healthData.energyLevel / 10,
      healthData.sleepQuality / 10,
      (10 - healthData.stressScore) / 10
    ];
    return (scores.reduce((a, b) => a + b, 0) / scores.length * 100).toFixed(0);
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return '#10b981';
    if (score >= 60) return '#3b82f6';
    if (score >= 40) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <ScrollView style={styles.container}>
      <ThemedView style={styles.header}>
        <ThemedText type="title" style={styles.title}>Health Overview</ThemedText>
        <ThemedText style={styles.subtitle}>Track your wellness journey</ThemedText>
      </ThemedView>

      {/* Overall Health Score */}
      <ThemedView style={styles.card}>
        <View style={styles.cardHeader}>
          <IconSymbol name="heart.fill" size={24} color="#ef4444" />
          <ThemedText type="subtitle" style={styles.cardTitle}>Overall Health Score</ThemedText>
        </View>
        
        <View style={styles.scoreContainer}>
          <ThemedText style={[styles.scoreNumber, { color: getScoreColor(parseInt(getHealthScore())) }]}>
            {getHealthScore()}%
          </ThemedText>
          <ThemedText style={styles.scoreLabel}>Based on your recent data</ThemedText>
        </View>
      </ThemedView>

      {/* Biometric Data */}
      <ThemedView style={styles.card}>
        <View style={styles.cardHeader}>
          <IconSymbol name="waveform.path.ecg" size={24} color="#3b82f6" />
          <ThemedText type="subtitle" style={styles.cardTitle}>Biometric Data</ThemedText>
        </View>
        
        <View style={styles.metricsGrid}>
          <View style={styles.metricItem}>
            <IconSymbol name="heart" size={20} color="#ef4444" />
            <ThemedText style={styles.metricValue}>{healthData.heartRateResting}</ThemedText>
            <ThemedText style={styles.metricLabel}>Resting HR</ThemedText>
          </View>
          
          <View style={styles.metricItem}>
            <IconSymbol name="waveform" size={20} color="#8b5cf6" />
            <ThemedText style={styles.metricValue}>{healthData.heartRateVariability}</ThemedText>
            <ThemedText style={styles.metricLabel}>HRV</ThemedText>
          </View>
          
          <View style={styles.metricItem}>
            <IconSymbol name="moon" size={20} color="#6366f1" />
            <ThemedText style={styles.metricValue}>{healthData.sleepDurationHours}h</ThemedText>
            <ThemedText style={styles.metricLabel}>Sleep</ThemedText>
          </View>
          
          <View style={styles.metricItem}>
            <IconSymbol name="bolt" size={20} color="#f59e0b" />
            <ThemedText style={styles.metricValue}>{healthData.stressScore.toFixed(1)}</ThemedText>
            <ThemedText style={styles.metricLabel}>Stress</ThemedText>
          </View>
        </View>
      </ThemedView>

      {/* Activity Data */}
      <ThemedView style={styles.card}>
        <View style={styles.cardHeader}>
          <IconSymbol name="figure.walk" size={24} color="#10b981" />
          <ThemedText type="subtitle" style={styles.cardTitle}>Activity</ThemedText>
        </View>
        
        <View style={styles.activityGrid}>
          <View style={styles.activityItem}>
            <ThemedText style={styles.activityValue}>{healthData.steps.toLocaleString()}</ThemedText>
            <ThemedText style={styles.activityLabel}>Steps</ThemedText>
          </View>
          
          <View style={styles.activityItem}>
            <ThemedText style={styles.activityValue}>{healthData.activeCalories}</ThemedText>
            <ThemedText style={styles.activityLabel}>Calories</ThemedText>
          </View>
          
          <View style={styles.activityItem}>
            <ThemedText style={styles.activityValue}>{healthData.exerciseMinutes}</ThemedText>
            <ThemedText style={styles.activityLabel}>Exercise Min</ThemedText>
          </View>
          
          <View style={styles.activityItem}>
            <ThemedText style={styles.activityValue}>{healthData.standHours}</ThemedText>
            <ThemedText style={styles.activityLabel}>Stand Hours</ThemedText>
          </View>
        </View>
      </ThemedView>

      {/* Mental Health */}
      <ThemedView style={styles.card}>
        <View style={styles.cardHeader}>
          <IconSymbol name="brain.head.profile" size={24} color="#8b5cf6" />
          <ThemedText type="subtitle" style={styles.cardTitle}>Mental Health</ThemedText>
        </View>
        
        <View style={styles.mentalHealthGrid}>
          <View style={styles.mentalHealthItem}>
            <ThemedText style={styles.mentalHealthLabel}>Mood</ThemedText>
            <ThemedText style={styles.mentalHealthValue}>{healthData.moodRating.toFixed(1)}/10</ThemedText>
          </View>
          
          <View style={styles.mentalHealthItem}>
            <ThemedText style={styles.mentalHealthLabel}>Anxiety</ThemedText>
            <ThemedText style={styles.mentalHealthValue}>{healthData.anxietyLevel.toFixed(1)}/10</ThemedText>
          </View>
          
          <View style={styles.mentalHealthItem}>
            <ThemedText style={styles.mentalHealthLabel}>Cravings</ThemedText>
            <ThemedText style={styles.mentalHealthValue}>{healthData.cravingIntensity.toFixed(1)}/10</ThemedText>
          </View>
          
          <View style={styles.mentalHealthItem}>
            <ThemedText style={styles.mentalHealthLabel}>Energy</ThemedText>
            <ThemedText style={styles.mentalHealthValue}>{healthData.energyLevel.toFixed(1)}/10</ThemedText>
          </View>
        </View>
        
        <TouchableOpacity style={styles.updateButton} onPress={() => setShowMoodModal(true)}>
          <IconSymbol name="pencil" size={16} color="#ffffff" />
          <ThemedText style={styles.updateButtonText}>Update Mood Diary</ThemedText>
        </TouchableOpacity>
      </ThemedView>

      {/* PHQ-5 Assessment */}
      <ThemedView style={styles.card}>
        <View style={styles.cardHeader}>
          <IconSymbol name="list.clipboard" size={24} color="#f59e0b" />
          <ThemedText type="subtitle" style={styles.cardTitle}>PHQ-5 Assessment</ThemedText>
        </View>
        
        <View style={styles.phq5Container}>
          <ThemedText style={styles.phq5Score}>Score: {healthData.phq5.totalScore}/20</ThemedText>
          <ThemedText style={styles.phq5Description}>
            {healthData.phq5.totalScore <= 4 ? 'Minimal symptoms' :
             healthData.phq5.totalScore <= 9 ? 'Mild symptoms' :
             healthData.phq5.totalScore <= 14 ? 'Moderate symptoms' : 'Severe symptoms'}
          </ThemedText>
        </View>
        
        <TouchableOpacity style={styles.updateButton} onPress={() => setShowPHQ5Modal(true)}>
          <IconSymbol name="pencil" size={16} color="#ffffff" />
          <ThemedText style={styles.updateButtonText}>Take Assessment</ThemedText>
        </TouchableOpacity>
      </ThemedView>

      {/* Sleep Details */}
      <ThemedView style={styles.card}>
        <View style={styles.cardHeader}>
          <IconSymbol name="bed.double" size={24} color="#6366f1" />
          <ThemedText type="subtitle" style={styles.cardTitle}>Sleep Analysis</ThemedText>
        </View>
        
        <View style={styles.sleepGrid}>
          <View style={styles.sleepItem}>
            <ThemedText style={styles.sleepLabel}>Total Sleep</ThemedText>
            <ThemedText style={styles.sleepValue}>{healthData.sleepDurationHours}h</ThemedText>
          </View>
          
          <View style={styles.sleepItem}>
            <ThemedText style={styles.sleepLabel}>Efficiency</ThemedText>
            <ThemedText style={styles.sleepValue}>{healthData.sleepEfficiency}%</ThemedText>
          </View>
          
          <View style={styles.sleepItem}>
            <ThemedText style={styles.sleepLabel}>Deep Sleep</ThemedText>
            <ThemedText style={styles.sleepValue}>{healthData.deepSleepHours}h</ThemedText>
          </View>
          
          <View style={styles.sleepItem}>
            <ThemedText style={styles.sleepLabel}>REM Sleep</ThemedText>
            <ThemedText style={styles.sleepValue}>{healthData.remSleepHours}h</ThemedText>
          </View>
        </View>
      </ThemedView>

      {/* Mood Diary Modal */}
      <Modal visible={showMoodModal} animationType="slide" presentationStyle="pageSheet">
        <View style={styles.modalContainer}>
          <View style={styles.modalHeader}>
            <ThemedText type="title">Mood Diary</ThemedText>
            <TouchableOpacity onPress={() => setShowMoodModal(false)}>
              <ThemedText style={styles.closeButton}>✕</ThemedText>
            </TouchableOpacity>
          </View>
          
          <ScrollView style={styles.modalContent}>
            <View style={styles.sliderContainer}>
              <ThemedText style={styles.sliderLabel}>Mood (1-10)</ThemedText>
              <ThemedText style={styles.sliderValue}>{tempMoodData.mood}</ThemedText>
              <View style={styles.sliderButtons}>
                <TouchableOpacity onPress={() => setTempMoodData({...tempMoodData, mood: Math.max(1, tempMoodData.mood - 1)})}>
                  <ThemedText style={styles.sliderButton}>-</ThemedText>
                </TouchableOpacity>
                <TouchableOpacity onPress={() => setTempMoodData({...tempMoodData, mood: Math.min(10, tempMoodData.mood + 1)})}>
                  <ThemedText style={styles.sliderButton}>+</ThemedText>
                </TouchableOpacity>
              </View>
            </View>
            
            <View style={styles.sliderContainer}>
              <ThemedText style={styles.sliderLabel}>Anxiety (1-10)</ThemedText>
              <ThemedText style={styles.sliderValue}>{tempMoodData.anxiety}</ThemedText>
              <View style={styles.sliderButtons}>
                <TouchableOpacity onPress={() => setTempMoodData({...tempMoodData, anxiety: Math.max(1, tempMoodData.anxiety - 1)})}>
                  <ThemedText style={styles.sliderButton}>-</ThemedText>
                </TouchableOpacity>
                <TouchableOpacity onPress={() => setTempMoodData({...tempMoodData, anxiety: Math.min(10, tempMoodData.anxiety + 1)})}>
                  <ThemedText style={styles.sliderButton}>+</ThemedText>
                </TouchableOpacity>
              </View>
            </View>
            
            <View style={styles.sliderContainer}>
              <ThemedText style={styles.sliderLabel}>Cravings (1-10)</ThemedText>
              <ThemedText style={styles.sliderValue}>{tempMoodData.cravings}</ThemedText>
              <View style={styles.sliderButtons}>
                <TouchableOpacity onPress={() => setTempMoodData({...tempMoodData, cravings: Math.max(1, tempMoodData.cravings - 1)})}>
                  <ThemedText style={styles.sliderButton}>-</ThemedText>
                </TouchableOpacity>
                <TouchableOpacity onPress={() => setTempMoodData({...tempMoodData, cravings: Math.min(10, tempMoodData.cravings + 1)})}>
                  <ThemedText style={styles.sliderButton}>+</ThemedText>
                </TouchableOpacity>
              </View>
            </View>
            
            <View style={styles.notesContainer}>
              <ThemedText style={styles.notesLabel}>Notes</ThemedText>
              <TextInput
                style={styles.notesInput}
                multiline
                numberOfLines={4}
                value={tempMoodData.notes}
                onChangeText={(text) => setTempMoodData({...tempMoodData, notes: text})}
                placeholder="How are you feeling today? Any triggers or coping strategies?"
              />
            </View>
            
            <TouchableOpacity style={styles.submitButton} onPress={handleMoodSubmit}>
              <ThemedText style={styles.submitButtonText}>Save Mood Entry</ThemedText>
            </TouchableOpacity>
          </ScrollView>
        </View>
      </Modal>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  header: {
    padding: 20,
    paddingTop: 60,
    backgroundColor: 'transparent',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
    opacity: 0.7,
  },
  card: {
    margin: 16,
    marginTop: 8,
    padding: 20,
    borderRadius: 16,
    backgroundColor: '#ffffff',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  cardTitle: {
    marginLeft: 8,
    fontSize: 18,
    fontWeight: '600',
  },
  scoreContainer: {
    alignItems: 'center',
  },
  scoreNumber: {
    fontSize: 48,
    fontWeight: 'bold',
  },
  scoreLabel: {
    fontSize: 14,
    opacity: 0.7,
    marginTop: 4,
  },
  metricsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  metricItem: {
    alignItems: 'center',
    flex: 1,
  },
  metricValue: {
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 4,
    marginBottom: 2,
  },
  metricLabel: {
    fontSize: 12,
    opacity: 0.7,
  },
  activityGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    flexWrap: 'wrap',
  },
  activityItem: {
    alignItems: 'center',
    width: '48%',
    marginBottom: 16,
  },
  activityValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#10b981',
  },
  activityLabel: {
    fontSize: 14,
    opacity: 0.7,
    marginTop: 4,
  },
  mentalHealthGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    flexWrap: 'wrap',
    marginBottom: 16,
  },
  mentalHealthItem: {
    alignItems: 'center',
    width: '48%',
    marginBottom: 12,
  },
  mentalHealthLabel: {
    fontSize: 14,
    opacity: 0.7,
    marginBottom: 4,
  },
  mentalHealthValue: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  updateButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#3b82f6',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 12,
  },
  updateButtonText: {
    color: '#ffffff',
    fontWeight: '600',
    marginLeft: 8,
  },
  phq5Container: {
    alignItems: 'center',
    marginBottom: 16,
  },
  phq5Score: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#f59e0b',
  },
  phq5Description: {
    fontSize: 14,
    opacity: 0.7,
    marginTop: 4,
  },
  sleepGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    flexWrap: 'wrap',
  },
  sleepItem: {
    alignItems: 'center',
    width: '48%',
    marginBottom: 12,
  },
  sleepLabel: {
    fontSize: 14,
    opacity: 0.7,
    marginBottom: 4,
  },
  sleepValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#6366f1',
  },
  modalContainer: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    paddingTop: 60,
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  closeButton: {
    fontSize: 24,
    color: '#666',
  },
  modalContent: {
    flex: 1,
    padding: 20,
  },
  sliderContainer: {
    marginBottom: 24,
  },
  sliderLabel: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
  },
  sliderValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#3b82f6',
    textAlign: 'center',
    marginBottom: 8,
  },
  sliderButtons: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 20,
  },
  sliderButton: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#3b82f6',
    paddingHorizontal: 20,
    paddingVertical: 10,
    backgroundColor: '#eff6ff',
    borderRadius: 8,
  },
  notesContainer: {
    marginBottom: 24,
  },
  notesLabel: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
  },
  notesInput: {
    borderWidth: 1,
    borderColor: '#d1d5db',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    textAlignVertical: 'top',
  },
  submitButton: {
    backgroundColor: '#10b981',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  submitButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
}); 