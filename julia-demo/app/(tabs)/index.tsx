import React, { useState, useEffect } from 'react';
import { ScrollView, StyleSheet, View, Text, TouchableOpacity, Alert } from 'react-native';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { IconSymbol } from '@/components/ui/IconSymbol';
import AsyncStorage from '@react-native-async-storage/async-storage';
import AppleHealthService from '../../services/AppleHealthService';

interface PatientData {
  name: string;
  daysSober: number;
  currentRisk: number;
  currentMood: number;
  currentAnxiety: number;
  currentCravings: number;
  sleepHours: number;
  stressLevel: number;
  heartRate: number;
  lastUpdate: string;
}

export default function DashboardScreen() {
  const [patientData, setPatientData] = useState<PatientData>({
    name: 'Sarah Chen',
    daysSober: 127,
    currentRisk: 0.35,
    currentMood: 7.2,
    currentAnxiety: 4.1,
    currentCravings: 2.8,
    sleepHours: 7.5,
    stressLevel: 3.2,
    heartRate: 68,
    lastUpdate: new Date().toLocaleDateString()
  });

  const [todayLogged, setTodayLogged] = useState(false);
  const [appleHealthConnected, setAppleHealthConnected] = useState(false);
  const [isLoadingHealthData, setIsLoadingHealthData] = useState(false);

  useEffect(() => {
    loadPatientData();
    checkTodayLogged();
    checkAppleHealthConnection();
  }, []);

  const loadPatientData = async () => {
    try {
      const stored = await AsyncStorage.getItem('patientData');
      if (stored) {
        setPatientData(JSON.parse(stored));
      }
    } catch (error) {
      console.error('Error loading patient data:', error);
    }
  };

  const checkTodayLogged = async () => {
    try {
      const lastLogged = await AsyncStorage.getItem('lastMoodLog');
      const today = new Date().toDateString();
      setTodayLogged(lastLogged === today);
    } catch (error) {
      console.error('Error checking mood log:', error);
    }
  };

  const checkAppleHealthConnection = async () => {
    try {
      const connected = await AppleHealthService.isAppleHealthConnected();
      setAppleHealthConnected(connected);
      
      if (connected) {
        syncAppleHealthData();
      }
    } catch (error) {
      console.error('Error checking Apple Health connection:', error);
    }
  };

  const syncAppleHealthData = async () => {
    if (!appleHealthConnected) return;
    
    setIsLoadingHealthData(true);
    try {
      const healthData = await AppleHealthService.getComprehensiveHealthData();
      if (healthData) {
        const updatedData = {
          ...patientData,
          heartRate: healthData.heartRateResting || patientData.heartRate,
          sleepHours: healthData.sleepDurationHours || patientData.sleepHours,
          stressLevel: healthData.stressScore || patientData.stressLevel,
          lastUpdate: new Date().toLocaleDateString()
        };
        setPatientData(updatedData);
        await AsyncStorage.setItem('patientData', JSON.stringify(updatedData));
      }
    } catch (error) {
      console.error('Error syncing Apple Health data:', error);
    } finally {
      setIsLoadingHealthData(false);
    }
  };

  const handleConnectAppleHealth = async () => {
    try {
      const success = await AppleHealthService.initialize();
      if (success) {
        setAppleHealthConnected(true);
        Alert.alert(
          'Apple Health Connected!',
          'Your health data will now sync automatically to provide better insights.',
          [{ text: 'OK', onPress: () => syncAppleHealthData() }]
        );
      } else {
        Alert.alert(
          'Connection Failed',
          'Unable to connect to Apple Health. Please check your permissions and try again.'
        );
      }
    } catch (error) {
      console.error('Error connecting to Apple Health:', error);
      Alert.alert('Error', 'Failed to connect to Apple Health.');
    }
  };

  const getRiskColor = (risk: number) => {
    if (risk >= 0.8) return '#ef4444';
    if (risk >= 0.6) return '#f59e0b';
    if (risk >= 0.4) return '#3b82f6';
    return '#10b981';
  };

  const getRiskLabel = (risk: number) => {
    if (risk >= 0.8) return 'Critical';
    if (risk >= 0.6) return 'Elevated';
    if (risk >= 0.4) return 'Moderate';
    return 'Stable';
  };

  const handleQuickMoodLog = () => {
    Alert.alert(
      'Quick Mood Check',
      'How are you feeling right now?',
      [
        { text: 'Great 😊', onPress: () => logMood(8) },
        { text: 'Good 🙂', onPress: () => logMood(7) },
        { text: 'Okay 😐', onPress: () => logMood(5) },
        { text: 'Not Great 😔', onPress: () => logMood(3) },
        { text: 'Cancel', style: 'cancel' }
      ]
    );
  };

  const logMood = async (mood: number) => {
    try {
      const today = new Date().toDateString();
      await AsyncStorage.setItem('lastMoodLog', today);
      setTodayLogged(true);
      
      // Update patient data
      const updatedData = { ...patientData, currentMood: mood, lastUpdate: new Date().toLocaleDateString() };
      setPatientData(updatedData);
      await AsyncStorage.setItem('patientData', JSON.stringify(updatedData));
      
      Alert.alert('Thanks!', 'Your mood has been logged.');
    } catch (error) {
      console.error('Error logging mood:', error);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <ThemedView style={styles.header}>
        <ThemedText type="title" style={styles.greeting}>
          Hello, {patientData.name.split(' ')[0]}! 👋
        </ThemedText>
        <ThemedText style={styles.subtitle}>
          Here's your recovery progress
        </ThemedText>
      </ThemedView>

      {/* Recovery Progress Card */}
      <ThemedView style={styles.card}>
        <View style={styles.cardHeader}>
          <IconSymbol name="calendar" size={24} color="#10b981" />
          <ThemedText type="subtitle" style={styles.cardTitle}>Recovery Progress</ThemedText>
        </View>
        
        <View style={styles.progressContainer}>
          <View style={styles.daysSoberContainer}>
            <ThemedText style={styles.daysSoberNumber}>{patientData.daysSober}</ThemedText>
            <ThemedText style={styles.daysSoberLabel}>Days Sober</ThemedText>
          </View>
          
          <View style={styles.riskContainer}>
            <View style={[styles.riskBadge, { backgroundColor: getRiskColor(patientData.currentRisk) + '20' }]}>
              <ThemedText style={[styles.riskText, { color: getRiskColor(patientData.currentRisk) }]}>
                {getRiskLabel(patientData.currentRisk)}
              </ThemedText>
            </View>
            <ThemedText style={styles.riskScore}>
              Risk: {(patientData.currentRisk * 100).toFixed(0)}%
            </ThemedText>
          </View>
        </View>
      </ThemedView>

      {/* Today's Stats */}
      <ThemedView style={styles.card}>
        <View style={styles.cardHeader}>
          <IconSymbol name="chart.bar" size={24} color="#3b82f6" />
          <ThemedText type="subtitle" style={styles.cardTitle}>Today's Stats</ThemedText>
        </View>
        
        <View style={styles.statsGrid}>
          <View style={styles.statItem}>
            <IconSymbol name="heart" size={20} color="#ef4444" />
            <ThemedText style={styles.statValue}>{patientData.heartRate}</ThemedText>
            <ThemedText style={styles.statLabel}>Heart Rate</ThemedText>
          </View>
          
          <View style={styles.statItem}>
            <IconSymbol name="moon" size={20} color="#6366f1" />
            <ThemedText style={styles.statValue}>{patientData.sleepHours}h</ThemedText>
            <ThemedText style={styles.statLabel}>Sleep</ThemedText>
          </View>
          
          <View style={styles.statItem}>
            <IconSymbol name="bolt" size={20} color="#f59e0b" />
            <ThemedText style={styles.statValue}>{patientData.stressLevel.toFixed(1)}</ThemedText>
            <ThemedText style={styles.statLabel}>Stress</ThemedText>
          </View>
          
          <View style={styles.statItem}>
            <IconSymbol name="face.smiling" size={20} color="#10b981" />
            <ThemedText style={styles.statValue}>{patientData.currentMood.toFixed(1)}</ThemedText>
            <ThemedText style={styles.statLabel}>Mood</ThemedText>
          </View>
        </View>
      </ThemedView>

      {/* Mental Health Check */}
      <ThemedView style={styles.card}>
        <View style={styles.cardHeader}>
          <IconSymbol name="brain.head.profile" size={24} color="#8b5cf6" />
          <ThemedText type="subtitle" style={styles.cardTitle}>Mental Health</ThemedText>
        </View>
        
        <View style={styles.mentalHealthGrid}>
          <View style={styles.mentalHealthItem}>
            <ThemedText style={styles.mentalHealthLabel}>Anxiety</ThemedText>
            <ThemedText style={styles.mentalHealthValue}>{patientData.currentAnxiety.toFixed(1)}/10</ThemedText>
          </View>
          
          <View style={styles.mentalHealthItem}>
            <ThemedText style={styles.mentalHealthLabel}>Cravings</ThemedText>
            <ThemedText style={styles.mentalHealthValue}>{patientData.currentCravings.toFixed(1)}/10</ThemedText>
          </View>
        </View>
      </ThemedView>

      {/* Quick Actions */}
      <ThemedView style={styles.card}>
        <View style={styles.cardHeader}>
          <IconSymbol name="bolt.fill" size={24} color="#f59e0b" />
          <ThemedText type="subtitle" style={styles.cardTitle}>Quick Actions</ThemedText>
        </View>
        
        <View style={styles.actionsContainer}>
          <TouchableOpacity 
            style={[styles.actionButton, todayLogged && styles.actionButtonDisabled]} 
            onPress={handleQuickMoodLog}
            disabled={todayLogged}
          >
            <IconSymbol name="face.smiling" size={20} color={todayLogged ? "#9ca3af" : "#ffffff"} />
            <ThemedText style={[styles.actionButtonText, todayLogged && styles.actionButtonTextDisabled]}>
              {todayLogged ? 'Mood Logged ✓' : 'Log Mood'}
            </ThemedText>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.actionButton}>
            <IconSymbol name="message" size={20} color="#ffffff" />
            <ThemedText style={styles.actionButtonText}>Chat with Julia</ThemedText>
          </TouchableOpacity>
        </View>
      </ThemedView>

      {/* Apple Health Integration */}
      <ThemedView style={styles.card}>
        <View style={styles.cardHeader}>
          <IconSymbol name="heart.text.square" size={24} color="#ff2d92" />
          <ThemedText type="subtitle" style={styles.cardTitle}>Apple Health</ThemedText>
        </View>
        
        {appleHealthConnected ? (
          <View style={styles.healthConnectedContainer}>
            <View style={styles.healthStatusRow}>
              <IconSymbol name="checkmark.circle.fill" size={20} color="#10b981" />
              <ThemedText style={styles.healthConnectedText}>Connected & Syncing</ThemedText>
              {isLoadingHealthData && (
                <ThemedText style={styles.syncingText}>Syncing...</ThemedText>
              )}
            </View>
            <ThemedText style={styles.healthDescription}>
              Your health data is automatically syncing from Apple Health
            </ThemedText>
            <TouchableOpacity style={styles.syncButton} onPress={syncAppleHealthData}>
              <IconSymbol name="arrow.clockwise" size={16} color="#3b82f6" />
              <ThemedText style={styles.syncButtonText}>Sync Now</ThemedText>
            </TouchableOpacity>
          </View>
        ) : (
          <View style={styles.healthDisconnectedContainer}>
            <ThemedText style={styles.healthDescription}>
              Connect to Apple Health to automatically sync your biometric data and get personalized insights.
            </ThemedText>
            <TouchableOpacity style={styles.connectHealthButton} onPress={handleConnectAppleHealth}>
              <IconSymbol name="plus.circle.fill" size={20} color="#ffffff" />
              <ThemedText style={styles.connectHealthButtonText}>Connect Apple Health</ThemedText>
            </TouchableOpacity>
          </View>
        )}
      </ThemedView>

      {/* Emergency Support */}
      <ThemedView style={[styles.card, styles.emergencyCard]}>
        <View style={styles.cardHeader}>
          <IconSymbol name="exclamationmark.triangle.fill" size={24} color="#ef4444" />
          <ThemedText type="subtitle" style={[styles.cardTitle, styles.emergencyTitle]}>Need Help?</ThemedText>
        </View>
        
        <ThemedText style={styles.emergencyText}>
          If you're experiencing cravings or need immediate support, reach out now.
        </ThemedText>
        
        <TouchableOpacity style={styles.emergencyButton}>
          <IconSymbol name="phone.fill" size={20} color="#ffffff" />
          <ThemedText style={styles.emergencyButtonText}>Crisis Hotline</ThemedText>
        </TouchableOpacity>
      </ThemedView>
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
  greeting: {
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
  progressContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  daysSoberContainer: {
    alignItems: 'center',
  },
  daysSoberNumber: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#10b981',
  },
  daysSoberLabel: {
    fontSize: 14,
    opacity: 0.7,
    marginTop: 4,
  },
  riskContainer: {
    alignItems: 'center',
  },
  riskBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    marginBottom: 8,
  },
  riskText: {
    fontSize: 14,
    fontWeight: '600',
  },
  riskScore: {
    fontSize: 12,
    opacity: 0.7,
  },
  statsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  statItem: {
    alignItems: 'center',
    flex: 1,
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 4,
    marginBottom: 2,
  },
  statLabel: {
    fontSize: 12,
    opacity: 0.7,
  },
  mentalHealthGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  mentalHealthItem: {
    alignItems: 'center',
  },
  mentalHealthLabel: {
    fontSize: 14,
    opacity: 0.7,
    marginBottom: 4,
  },
  mentalHealthValue: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  actionsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 12,
  },
  actionButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#3b82f6',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 12,
  },
  actionButtonDisabled: {
    backgroundColor: '#e5e7eb',
  },
  actionButtonText: {
    color: '#ffffff',
    fontWeight: '600',
    marginLeft: 8,
  },
  actionButtonTextDisabled: {
    color: '#9ca3af',
  },
  emergencyCard: {
    backgroundColor: '#fef2f2',
    borderColor: '#fecaca',
    borderWidth: 1,
  },
  emergencyTitle: {
    color: '#dc2626',
  },
  emergencyText: {
    fontSize: 14,
    opacity: 0.8,
    marginBottom: 16,
    textAlign: 'center',
  },
  emergencyButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#dc2626',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 12,
  },
  emergencyButtonText: {
    color: '#ffffff',
    fontWeight: '600',
    marginLeft: 8,
  },
  healthConnectedContainer: {
    alignItems: 'center',
  },
  healthDisconnectedContainer: {
    alignItems: 'center',
  },
  healthStatusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  healthConnectedText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#10b981',
    marginLeft: 8,
  },
  syncingText: {
    fontSize: 12,
    color: '#6b7280',
    marginLeft: 8,
  },
  healthDescription: {
    fontSize: 14,
    textAlign: 'center',
    opacity: 0.7,
    marginBottom: 16,
  },
  syncButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#eff6ff',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
  },
  syncButtonText: {
    color: '#3b82f6',
    fontWeight: '500',
    marginLeft: 4,
  },
  connectHealthButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#ff2d92',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 12,
  },
  connectHealthButtonText: {
    color: '#ffffff',
    fontWeight: '600',
    marginLeft: 8,
  },
});
