import React, { useState, useEffect } from 'react';
import { View, StyleSheet, TouchableOpacity, Alert, Platform } from 'react-native';
import { ThemedText } from './ThemedText';
import { ThemedView } from './ThemedView';
import { IconSymbol } from './ui/IconSymbol';
import AppleHealthService from '../services/AppleHealthService';

interface AppleHealthCardProps {
  onDataSync?: (data: any) => void;
  showFullFeatures?: boolean;
}

export default function AppleHealthCard({ onDataSync, showFullFeatures = false }: AppleHealthCardProps) {
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [lastSyncTime, setLastSyncTime] = useState<string | null>(null);

  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    try {
      const connected = await AppleHealthService.isAppleHealthConnected();
      setIsConnected(connected);
    } catch (error) {
      console.error('Error checking Apple Health connection:', error);
    }
  };

  const handleConnect = async () => {
    if (Platform.OS !== 'ios') {
      Alert.alert(
        'Not Available',
        'Apple Health is only available on iOS devices.'
      );
      return;
    }

    setIsLoading(true);
    try {
      const success = await AppleHealthService.initialize();
      if (success) {
        setIsConnected(true);
        setLastSyncTime(new Date().toLocaleTimeString());
        
        Alert.alert(
          'Apple Health Connected! 🎉',
          'Your health data will now sync automatically to provide better insights for your recovery journey.',
          [{ text: 'Great!', onPress: () => handleSync() }]
        );
      } else {
        Alert.alert(
          'Connection Failed',
          'Unable to connect to Apple Health. Please make sure you have the Health app installed and grant the necessary permissions.'
        );
      }
    } catch (error) {
      console.error('Error connecting to Apple Health:', error);
      Alert.alert('Error', 'Failed to connect to Apple Health. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSync = async () => {
    if (!isConnected) return;

    setIsLoading(true);
    try {
      const healthData = await AppleHealthService.getComprehensiveHealthData();
      if (healthData) {
        setLastSyncTime(new Date().toLocaleTimeString());
        onDataSync?.(healthData);
        
        if (showFullFeatures) {
          Alert.alert(
            'Sync Complete ✅',
            `Updated health data:\n• Heart Rate: ${healthData.heartRateResting || 'N/A'} bpm\n• Sleep: ${healthData.sleepDurationHours || 'N/A'} hours\n• Steps: ${healthData.steps || 'N/A'}`
          );
        }
      } else {
        Alert.alert(
          'Sync Issue',
          'No recent health data found. Make sure your Apple Watch is synced and try again.'
        );
      }
    } catch (error) {
      console.error('Error syncing health data:', error);
      Alert.alert('Sync Error', 'Failed to sync health data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDisconnect = () => {
    Alert.alert(
      'Disconnect Apple Health',
      'Are you sure you want to stop syncing with Apple Health? You can reconnect anytime.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Disconnect',
          style: 'destructive',
          onPress: async () => {
            await AppleHealthService.disconnect();
            setIsConnected(false);
            setLastSyncTime(null);
          }
        }
      ]
    );
  };

  const writeMindfulnessSession = async () => {
    if (!isConnected) return;

    Alert.alert(
      'Log Mindfulness Session',
      'How long was your mindfulness or meditation session?',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: '5 minutes', onPress: () => logMindfulness(5) },
        { text: '10 minutes', onPress: () => logMindfulness(10) },
        { text: '15 minutes', onPress: () => logMindfulness(15) },
        { text: '20 minutes', onPress: () => logMindfulness(20) }
      ]
    );
  };

  const logMindfulness = async (duration: number) => {
    try {
      const success = await AppleHealthService.writeMindfulnessSession(duration);
      if (success) {
        Alert.alert(
          'Session Logged! 🧘‍♀️',
          `Your ${duration}-minute mindfulness session has been added to Apple Health.`
        );
      } else {
        Alert.alert('Error', 'Failed to log mindfulness session.');
      }
    } catch (error) {
      console.error('Error logging mindfulness session:', error);
      Alert.alert('Error', 'Failed to log mindfulness session.');
    }
  };

  if (Platform.OS !== 'ios') {
    return (
      <ThemedView style={styles.card}>
        <View style={styles.cardHeader}>
          <IconSymbol name="heart.text.square" size={24} color="#ff2d92" />
          <ThemedText type="subtitle" style={styles.cardTitle}>Apple Health</ThemedText>
        </View>
        <ThemedText style={styles.unavailableText}>
          Apple Health integration is only available on iOS devices.
        </ThemedText>
      </ThemedView>
    );
  }

  return (
    <ThemedView style={styles.card}>
      <View style={styles.cardHeader}>
        <IconSymbol name="heart.text.square" size={24} color="#ff2d92" />
        <ThemedText type="subtitle" style={styles.cardTitle}>Apple Health</ThemedText>
        {isConnected && (
          <View style={styles.connectedBadge}>
            <IconSymbol name="checkmark.circle.fill" size={16} color="#10b981" />
          </View>
        )}
      </View>

      {isConnected ? (
        <View style={styles.connectedContainer}>
          <View style={styles.statusRow}>
            <IconSymbol name="checkmark.circle.fill" size={20} color="#10b981" />
            <ThemedText style={styles.connectedText}>Connected & Syncing</ThemedText>
            {isLoading && (
              <ThemedText style={styles.loadingText}>Syncing...</ThemedText>
            )}
          </View>

          {lastSyncTime && (
            <ThemedText style={styles.lastSyncText}>
              Last sync: {lastSyncTime}
            </ThemedText>
          )}

          <ThemedText style={styles.description}>
            Automatically syncing biometric data from your Apple Watch and iPhone
          </ThemedText>

          <View style={styles.buttonRow}>
            <TouchableOpacity 
              style={styles.syncButton} 
              onPress={handleSync}
              disabled={isLoading}
            >
              <IconSymbol name="arrow.clockwise" size={16} color="#3b82f6" />
              <ThemedText style={styles.syncButtonText}>Sync Now</ThemedText>
            </TouchableOpacity>

            {showFullFeatures && (
              <TouchableOpacity 
                style={styles.mindfulnessButton} 
                onPress={writeMindfulnessSession}
              >
                <IconSymbol name="brain.head.profile" size={16} color="#8b5cf6" />
                <ThemedText style={styles.mindfulnessButtonText}>Log Mindfulness</ThemedText>
              </TouchableOpacity>
            )}
          </View>

          {showFullFeatures && (
            <TouchableOpacity 
              style={styles.disconnectButton} 
              onPress={handleDisconnect}
            >
              <ThemedText style={styles.disconnectButtonText}>Disconnect</ThemedText>
            </TouchableOpacity>
          )}
        </View>
      ) : (
        <View style={styles.disconnectedContainer}>
          <ThemedText style={styles.description}>
            Connect to Apple Health to automatically sync your biometric data and get personalized recovery insights.
          </ThemedText>

          <View style={styles.benefitsList}>
            <View style={styles.benefitItem}>
              <IconSymbol name="heart" size={16} color="#ef4444" />
              <ThemedText style={styles.benefitText}>Heart rate & HRV tracking</ThemedText>
            </View>
            <View style={styles.benefitItem}>
              <IconSymbol name="moon" size={16} color="#6366f1" />
              <ThemedText style={styles.benefitText}>Sleep analysis</ThemedText>
            </View>
            <View style={styles.benefitItem}>
              <IconSymbol name="figure.walk" size={16} color="#10b981" />
              <ThemedText style={styles.benefitText}>Activity & fitness data</ThemedText>
            </View>
            <View style={styles.benefitItem}>
              <IconSymbol name="brain.head.profile" size={16} color="#8b5cf6" />
              <ThemedText style={styles.benefitText}>Mindfulness sessions</ThemedText>
            </View>
          </View>

          <TouchableOpacity 
            style={styles.connectButton} 
            onPress={handleConnect}
            disabled={isLoading}
          >
            <IconSymbol name="plus.circle.fill" size={20} color="#ffffff" />
            <ThemedText style={styles.connectButtonText}>
              {isLoading ? 'Connecting...' : 'Connect Apple Health'}
            </ThemedText>
          </TouchableOpacity>
        </View>
      )}
    </ThemedView>
  );
}

const styles = StyleSheet.create({
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
    flex: 1,
  },
  connectedBadge: {
    marginLeft: 8,
  },
  connectedContainer: {
    alignItems: 'center',
  },
  disconnectedContainer: {
    alignItems: 'center',
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  connectedText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#10b981',
    marginLeft: 8,
  },
  loadingText: {
    fontSize: 12,
    color: '#6b7280',
    marginLeft: 8,
  },
  lastSyncText: {
    fontSize: 12,
    color: '#6b7280',
    marginBottom: 8,
  },
  description: {
    fontSize: 14,
    textAlign: 'center',
    opacity: 0.7,
    marginBottom: 16,
  },
  buttonRow: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 12,
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
  mindfulnessButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f3f4f6',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
  },
  mindfulnessButtonText: {
    color: '#8b5cf6',
    fontWeight: '500',
    marginLeft: 4,
  },
  disconnectButton: {
    paddingVertical: 8,
    paddingHorizontal: 16,
  },
  disconnectButtonText: {
    color: '#ef4444',
    fontSize: 14,
    textDecorationLine: 'underline',
  },
  benefitsList: {
    alignSelf: 'stretch',
    marginBottom: 16,
  },
  benefitItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  benefitText: {
    fontSize: 14,
    marginLeft: 8,
    opacity: 0.8,
  },
  connectButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#ff2d92',
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 12,
  },
  connectButtonText: {
    color: '#ffffff',
    fontWeight: '600',
    marginLeft: 8,
  },
  unavailableText: {
    fontSize: 14,
    textAlign: 'center',
    opacity: 0.7,
  },
}); 