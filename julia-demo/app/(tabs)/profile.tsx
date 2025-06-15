import React, { useState, useEffect } from 'react';
import { ScrollView, StyleSheet, View, TouchableOpacity, Alert, Switch } from 'react-native';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { IconSymbol } from '@/components/ui/IconSymbol';
import AsyncStorage from '@react-native-async-storage/async-storage';
import AppleHealthService from '../../services/AppleHealthService';

interface ProfileData {
  name: string;
  age: number;
  sobrietyDate: string;
  daysSober: number;
  treatmentProgram: string;
  emergencyContact: string;
  counselor: string;
  medications: string[];
  goals: string[];
  achievements: string[];
  preferences: {
    notifications: boolean;
    dailyReminders: boolean;
    shareData: boolean;
    crisisAlerts: boolean;
    appleHealthSync: boolean;
  };
}

export default function ProfileScreen() {
  const [profileData, setProfileData] = useState<ProfileData>({
    name: 'Sarah Chen',
    age: 28,
    sobrietyDate: '2024-01-15',
    daysSober: 127,
    treatmentProgram: 'Outpatient Recovery Program',
    emergencyContact: 'Mom - (555) 123-4567',
    counselor: 'Dr. Martinez',
    medications: ['Naltrexone 50mg', 'Sertraline 100mg'],
    goals: [
      'Complete 90-day milestone',
      'Attend all group sessions',
      'Improve sleep quality',
      'Build healthy relationships'
    ],
    achievements: [
      '30 days sober',
      '60 days sober',
      '90 days sober',
      'Completed first month of treatment',
      'Attended 20 group sessions'
    ],
    preferences: {
      notifications: true,
      dailyReminders: true,
      shareData: true,
      crisisAlerts: true,
      appleHealthSync: false
    }
  });

  useEffect(() => {
    loadProfileData();
  }, []);

  const loadProfileData = async () => {
    try {
      const stored = await AsyncStorage.getItem('profileData');
      if (stored) {
        setProfileData(JSON.parse(stored));
      }
    } catch (error) {
      console.error('Error loading profile data:', error);
    }
  };

  const saveProfileData = async (newData: ProfileData) => {
    try {
      await AsyncStorage.setItem('profileData', JSON.stringify(newData));
      setProfileData(newData);
    } catch (error) {
      console.error('Error saving profile data:', error);
    }
  };

  const updatePreference = (key: keyof ProfileData['preferences'], value: boolean) => {
    const updatedData = {
      ...profileData,
      preferences: {
        ...profileData.preferences,
        [key]: value
      }
    };
    saveProfileData(updatedData);
  };

  const calculateSobrietyDays = () => {
    const sobrietyDate = new Date(profileData.sobrietyDate);
    const today = new Date();
    const diffTime = Math.abs(today.getTime() - sobrietyDate.getTime());
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  };

  const getNextMilestone = () => {
    const days = calculateSobrietyDays();
    if (days < 30) return { target: 30, label: '30 days' };
    if (days < 60) return { target: 60, label: '60 days' };
    if (days < 90) return { target: 90, label: '90 days' };
    if (days < 180) return { target: 180, label: '6 months' };
    if (days < 365) return { target: 365, label: '1 year' };
    return { target: days + 365, label: 'Next year' };
  };

  const handleEmergencyContact = () => {
    Alert.alert(
      'Emergency Contact',
      'Call your emergency contact?',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Call', onPress: () => Alert.alert('Calling...', profileData.emergencyContact) }
      ]
    );
  };

  const handleCounselorContact = () => {
    Alert.alert(
      'Contact Counselor',
      'Reach out to your counselor?',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Call', onPress: () => Alert.alert('Calling...', profileData.counselor) },
        { text: 'Message', onPress: () => Alert.alert('Opening messages...') }
      ]
    );
  };

  const handleAppleHealthToggle = async (value: boolean) => {
    if (value) {
      // User wants to enable Apple Health
      try {
        const success = await AppleHealthService.initialize();
        if (success) {
          updatePreference('appleHealthSync', true);
          Alert.alert(
            'Apple Health Connected',
            'Your health data will now sync automatically.'
          );
        } else {
          Alert.alert(
            'Connection Failed',
            'Unable to connect to Apple Health. Please check your permissions.'
          );
        }
      } catch (error) {
        Alert.alert('Error', 'Failed to connect to Apple Health.');
      }
    } else {
      // User wants to disable Apple Health
      Alert.alert(
        'Disconnect Apple Health',
        'Are you sure you want to stop syncing with Apple Health?',
        [
          { text: 'Cancel', style: 'cancel' },
          { 
            text: 'Disconnect', 
            style: 'destructive',
            onPress: async () => {
              await AppleHealthService.disconnect();
              updatePreference('appleHealthSync', false);
            }
          }
        ]
      );
    }
  };

  const nextMilestone = getNextMilestone();
  const progressToNext = (calculateSobrietyDays() / nextMilestone.target) * 100;

  return (
    <ScrollView style={styles.container}>
      <ThemedView style={styles.header}>
        <View style={styles.profileImageContainer}>
          <ThemedText style={styles.profileInitials}>
            {profileData.name.split(' ').map(n => n[0]).join('')}
          </ThemedText>
        </View>
        <ThemedText type="title" style={styles.name}>{profileData.name}</ThemedText>
        <ThemedText style={styles.age}>Age {profileData.age}</ThemedText>
      </ThemedView>

      {/* Recovery Progress */}
      <ThemedView style={styles.card}>
        <View style={styles.cardHeader}>
          <IconSymbol name="calendar" size={24} color="#10b981" />
          <ThemedText type="subtitle" style={styles.cardTitle}>Recovery Journey</ThemedText>
        </View>
        
        <View style={styles.progressContainer}>
          <View style={styles.daysSoberContainer}>
            <ThemedText style={styles.daysSoberNumber}>{calculateSobrietyDays()}</ThemedText>
            <ThemedText style={styles.daysSoberLabel}>Days Sober</ThemedText>
            <ThemedText style={styles.sobrietyDate}>Since {new Date(profileData.sobrietyDate).toLocaleDateString()}</ThemedText>
          </View>
          
          <View style={styles.milestoneContainer}>
            <ThemedText style={styles.milestoneLabel}>Next Milestone</ThemedText>
            <ThemedText style={styles.milestoneTarget}>{nextMilestone.label}</ThemedText>
            <View style={styles.progressBar}>
              <View style={[styles.progressFill, { width: `${Math.min(progressToNext, 100)}%` }]} />
            </View>
            <ThemedText style={styles.progressText}>{Math.round(progressToNext)}% complete</ThemedText>
          </View>
        </View>
      </ThemedView>

      {/* Treatment Info */}
      <ThemedView style={styles.card}>
        <View style={styles.cardHeader}>
          <IconSymbol name="cross.case" size={24} color="#3b82f6" />
          <ThemedText type="subtitle" style={styles.cardTitle}>Treatment</ThemedText>
        </View>
        
        <View style={styles.treatmentInfo}>
          <View style={styles.infoRow}>
            <ThemedText style={styles.infoLabel}>Program</ThemedText>
            <ThemedText style={styles.infoValue}>{profileData.treatmentProgram}</ThemedText>
          </View>
          
          <View style={styles.infoRow}>
            <ThemedText style={styles.infoLabel}>Counselor</ThemedText>
            <TouchableOpacity onPress={handleCounselorContact}>
              <ThemedText style={[styles.infoValue, styles.contactLink]}>{profileData.counselor}</ThemedText>
            </TouchableOpacity>
          </View>
          
          <View style={styles.infoRow}>
            <ThemedText style={styles.infoLabel}>Medications</ThemedText>
            <View>
              {profileData.medications.map((med, index) => (
                <ThemedText key={index} style={styles.medicationItem}>{med}</ThemedText>
              ))}
            </View>
          </View>
        </View>
      </ThemedView>

      {/* Goals & Achievements */}
      <ThemedView style={styles.card}>
        <View style={styles.cardHeader}>
          <IconSymbol name="target" size={24} color="#f59e0b" />
          <ThemedText type="subtitle" style={styles.cardTitle}>Goals & Achievements</ThemedText>
        </View>
        
        <View style={styles.goalsSection}>
          <ThemedText style={styles.sectionTitle}>Current Goals</ThemedText>
          {profileData.goals.map((goal, index) => (
            <View key={index} style={styles.goalItem}>
              <IconSymbol name="circle" size={16} color="#f59e0b" />
              <ThemedText style={styles.goalText}>{goal}</ThemedText>
            </View>
          ))}
        </View>
        
        <View style={styles.achievementsSection}>
          <ThemedText style={styles.sectionTitle}>Achievements</ThemedText>
          {profileData.achievements.map((achievement, index) => (
            <View key={index} style={styles.achievementItem}>
              <IconSymbol name="checkmark.circle.fill" size={16} color="#10b981" />
              <ThemedText style={styles.achievementText}>{achievement}</ThemedText>
            </View>
          ))}
        </View>
      </ThemedView>

      {/* Emergency Contacts */}
      <ThemedView style={styles.card}>
        <View style={styles.cardHeader}>
          <IconSymbol name="phone.fill" size={24} color="#ef4444" />
          <ThemedText type="subtitle" style={styles.cardTitle}>Emergency Support</ThemedText>
        </View>
        
        <TouchableOpacity style={styles.emergencyButton} onPress={handleEmergencyContact}>
          <IconSymbol name="phone" size={20} color="#ffffff" />
          <ThemedText style={styles.emergencyButtonText}>{profileData.emergencyContact}</ThemedText>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.crisisButton}>
          <IconSymbol name="exclamationmark.triangle.fill" size={20} color="#ffffff" />
          <ThemedText style={styles.crisisButtonText}>Crisis Hotline: 988</ThemedText>
        </TouchableOpacity>
      </ThemedView>

      {/* Settings */}
      <ThemedView style={styles.card}>
        <View style={styles.cardHeader}>
          <IconSymbol name="gear" size={24} color="#6b7280" />
          <ThemedText type="subtitle" style={styles.cardTitle}>Settings</ThemedText>
        </View>
        
        <View style={styles.settingsContainer}>
          <View style={styles.settingRow}>
            <ThemedText style={styles.settingLabel}>Push Notifications</ThemedText>
            <Switch
              value={profileData.preferences.notifications}
              onValueChange={(value) => updatePreference('notifications', value)}
            />
          </View>
          
          <View style={styles.settingRow}>
            <ThemedText style={styles.settingLabel}>Daily Check-in Reminders</ThemedText>
            <Switch
              value={profileData.preferences.dailyReminders}
              onValueChange={(value) => updatePreference('dailyReminders', value)}
            />
          </View>
          
          <View style={styles.settingRow}>
            <ThemedText style={styles.settingLabel}>Share Data with Care Team</ThemedText>
            <Switch
              value={profileData.preferences.shareData}
              onValueChange={(value) => updatePreference('shareData', value)}
            />
          </View>
          
          <View style={styles.settingRow}>
            <ThemedText style={styles.settingLabel}>Crisis Alert System</ThemedText>
            <Switch
              value={profileData.preferences.crisisAlerts}
              onValueChange={(value) => updatePreference('crisisAlerts', value)}
            />
          </View>
          
          <View style={styles.settingRow}>
            <ThemedText style={styles.settingLabel}>Apple Health Sync</ThemedText>
            <Switch
              value={profileData.preferences.appleHealthSync}
              onValueChange={handleAppleHealthToggle}
            />
          </View>
        </View>
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
    alignItems: 'center',
    padding: 20,
    paddingTop: 60,
    backgroundColor: '#ffffff',
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  profileImageContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#3b82f6',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 12,
  },
  profileInitials: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  age: {
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
    flex: 1,
  },
  daysSoberNumber: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#10b981',
  },
  daysSoberLabel: {
    fontSize: 14,
    opacity: 0.7,
    marginTop: 4,
  },
  sobrietyDate: {
    fontSize: 12,
    opacity: 0.5,
    marginTop: 2,
  },
  milestoneContainer: {
    flex: 1,
    alignItems: 'center',
  },
  milestoneLabel: {
    fontSize: 14,
    opacity: 0.7,
    marginBottom: 4,
  },
  milestoneTarget: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#f59e0b',
    marginBottom: 8,
  },
  progressBar: {
    width: '100%',
    height: 8,
    backgroundColor: '#e5e7eb',
    borderRadius: 4,
    overflow: 'hidden',
    marginBottom: 4,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#f59e0b',
  },
  progressText: {
    fontSize: 12,
    opacity: 0.7,
  },
  treatmentInfo: {
    gap: 12,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  infoLabel: {
    fontSize: 14,
    opacity: 0.7,
    flex: 1,
  },
  infoValue: {
    fontSize: 14,
    fontWeight: '500',
    flex: 2,
    textAlign: 'right',
  },
  contactLink: {
    color: '#3b82f6',
  },
  medicationItem: {
    fontSize: 14,
    fontWeight: '500',
    textAlign: 'right',
    marginBottom: 2,
  },
  goalsSection: {
    marginBottom: 20,
  },
  achievementsSection: {
    marginTop: 20,
    paddingTop: 20,
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 12,
  },
  goalItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  goalText: {
    fontSize: 14,
    marginLeft: 8,
  },
  achievementItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  achievementText: {
    fontSize: 14,
    marginLeft: 8,
    opacity: 0.8,
  },
  emergencyButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#ef4444',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 12,
    marginBottom: 12,
  },
  emergencyButtonText: {
    color: '#ffffff',
    fontWeight: '600',
    marginLeft: 8,
  },
  crisisButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#dc2626',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 12,
  },
  crisisButtonText: {
    color: '#ffffff',
    fontWeight: '600',
    marginLeft: 8,
  },
  settingsContainer: {
    gap: 16,
  },
  settingRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  settingLabel: {
    fontSize: 16,
    flex: 1,
  },
}); 