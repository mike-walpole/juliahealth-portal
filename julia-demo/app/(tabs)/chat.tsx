import React, { useState, useEffect, useCallback } from 'react';
import { View, StyleSheet, Alert, TouchableOpacity } from 'react-native';
import { GiftedChat, IMessage, Send, Bubble, InputToolbar } from 'react-native-gifted-chat';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { IconSymbol } from '@/components/ui/IconSymbol';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface ChatMessage extends IMessage {
  sentiment?: number;
  crisisFlag?: boolean;
  category?: string;
}

export default function ChatScreen() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isTyping, setIsTyping] = useState(false);

  useEffect(() => {
    loadChatHistory();
    setInitialMessages();
  }, []);

  const setInitialMessages = () => {
    setMessages([
      {
        _id: 1,
        text: "Hi! I'm Julia, your AI recovery companion. I'm here to support you on your journey. How are you feeling today?",
        createdAt: new Date(),
        user: {
          _id: 2,
          name: 'Julia AI',
          avatar: '🤖',
        },
        sentiment: 0.8,
        category: 'greeting'
      },
    ]);
  };

  const loadChatHistory = async () => {
    try {
      const stored = await AsyncStorage.getItem('chatHistory');
      if (stored) {
        const history = JSON.parse(stored);
        setMessages(history);
      }
    } catch (error) {
      console.error('Error loading chat history:', error);
    }
  };

  const saveChatHistory = async (newMessages: ChatMessage[]) => {
    try {
      await AsyncStorage.setItem('chatHistory', JSON.stringify(newMessages));
    } catch (error) {
      console.error('Error saving chat history:', error);
    }
  };

  const analyzeMessage = (text: string) => {
    const lowerText = text.toLowerCase();
    
    // Crisis detection keywords
    const crisisKeywords = ['suicide', 'kill myself', 'end it all', 'can\'t go on', 'want to die', 'relapse', 'using again'];
    const crisisFlag = crisisKeywords.some(keyword => lowerText.includes(keyword));
    
    // Sentiment analysis (simplified)
    const positiveWords = ['good', 'great', 'happy', 'better', 'strong', 'confident', 'grateful', 'hopeful'];
    const negativeWords = ['bad', 'terrible', 'sad', 'worse', 'weak', 'anxious', 'depressed', 'hopeless'];
    
    const positiveCount = positiveWords.filter(word => lowerText.includes(word)).length;
    const negativeCount = negativeWords.filter(word => lowerText.includes(word)).length;
    
    let sentiment = 0.5; // neutral
    if (positiveCount > negativeCount) {
      sentiment = 0.7 + (positiveCount * 0.1);
    } else if (negativeCount > positiveCount) {
      sentiment = 0.3 - (negativeCount * 0.1);
    }
    
    sentiment = Math.max(0, Math.min(1, sentiment));
    
    // Category detection
    let category = 'general';
    if (lowerText.includes('mood') || lowerText.includes('feeling')) category = 'mood';
    if (lowerText.includes('craving') || lowerText.includes('urge')) category = 'cravings';
    if (lowerText.includes('stress') || lowerText.includes('anxiety')) category = 'stress';
    if (lowerText.includes('sleep') || lowerText.includes('tired')) category = 'sleep';
    if (lowerText.includes('meeting') || lowerText.includes('group')) category = 'treatment';
    
    return { sentiment, crisisFlag, category };
  };

  const generateJuliaResponse = (userMessage: string, analysis: any): string => {
    const { sentiment, crisisFlag, category } = analysis;
    
    if (crisisFlag) {
      return "I'm concerned about what you're sharing. Your safety is important. Please reach out to your counselor or call the crisis hotline immediately. You don't have to go through this alone. 💙";
    }
    
    if (sentiment < 0.3) {
      const responses = [
        "I hear that you're going through a tough time. Remember that difficult feelings are temporary. What's one small thing that might help you feel a bit better right now?",
        "It sounds like you're struggling today. That's okay - recovery has ups and downs. What coping strategies have helped you before?",
        "I'm sorry you're feeling this way. You've shown strength by reaching out. What support do you need right now?"
      ];
      return responses[Math.floor(Math.random() * responses.length)];
    }
    
    if (sentiment > 0.7) {
      const responses = [
        "That's wonderful to hear! 🌟 It sounds like you're doing really well. What's been helping you feel so positive?",
        "I'm so glad you're feeling good! These positive moments are important to celebrate. Keep up the great work! 💪",
        "Your positive energy is inspiring! What would you like to focus on to maintain this momentum?"
      ];
      return responses[Math.floor(Math.random() * responses.length)];
    }
    
    // Category-specific responses
    switch (category) {
      case 'cravings':
        return "Cravings can be challenging. Remember the HALT technique - are you Hungry, Angry, Lonely, or Tired? Try some deep breathing or call your sponsor. You've got this! 💪";
      case 'stress':
        return "Stress is tough, but you have tools to handle it. Try the 4-7-8 breathing technique: breathe in for 4, hold for 7, out for 8. What usually helps you manage stress?";
      case 'sleep':
        return "Good sleep is so important for recovery. Try to maintain a consistent bedtime routine. How has your sleep been affecting your mood and energy?";
      case 'treatment':
        return "Staying connected with your treatment program is great! How are you finding the meetings? Remember, every day you show up is a victory. 🎯";
      default:
        const generalResponses = [
          "Thanks for sharing that with me. How can I support you today?",
          "I appreciate you checking in. What's on your mind?",
          "How are you taking care of yourself today?",
          "What's one thing you're grateful for right now?"
        ];
        return generalResponses[Math.floor(Math.random() * generalResponses.length)];
    }
  };

  const onSend = useCallback((newMessages: ChatMessage[] = []) => {
    const userMessage = newMessages[0];
    const analysis = analyzeMessage(userMessage.text);
    
    // Add analysis data to user message
    const enhancedUserMessage = {
      ...userMessage,
      sentiment: analysis.sentiment,
      crisisFlag: analysis.crisisFlag,
      category: analysis.category
    };
    
    // Show crisis alert if needed
    if (analysis.crisisFlag) {
      Alert.alert(
        'Crisis Support',
        'Your message indicates you may need immediate support. Please consider reaching out to your counselor or calling the crisis hotline.',
        [
          { text: 'Call Crisis Hotline', onPress: () => {} },
          { text: 'Contact Counselor', onPress: () => {} },
          { text: 'I\'m OK', style: 'cancel' }
        ]
      );
    }
    
    setMessages(previousMessages => {
      const updatedMessages = GiftedChat.append(previousMessages, [enhancedUserMessage]);
      saveChatHistory(updatedMessages);
      return updatedMessages;
    });
    
    // Generate Julia's response
    setIsTyping(true);
    setTimeout(() => {
      const juliaResponse: ChatMessage = {
        _id: Math.round(Math.random() * 1000000),
        text: generateJuliaResponse(userMessage.text, analysis),
        createdAt: new Date(),
        user: {
          _id: 2,
          name: 'Julia AI',
          avatar: '🤖',
        },
        sentiment: 0.8,
        category: 'response'
      };
      
      setMessages(previousMessages => {
        const updatedMessages = GiftedChat.append(previousMessages, [juliaResponse]);
        saveChatHistory(updatedMessages);
        return updatedMessages;
      });
      setIsTyping(false);
    }, 1000 + Math.random() * 2000); // Random delay to simulate thinking
  }, []);

  const renderBubble = (props: any) => {
    return (
      <Bubble
        {...props}
        wrapperStyle={{
          right: {
            backgroundColor: '#3b82f6',
          },
          left: {
            backgroundColor: '#f3f4f6',
          },
        }}
        textStyle={{
          right: {
            color: '#ffffff',
          },
          left: {
            color: '#1f2937',
          },
        }}
      />
    );
  };

  const renderSend = (props: any) => {
    return (
      <Send {...props}>
        <View style={styles.sendButton}>
          <IconSymbol name="arrow.up" size={20} color="#ffffff" />
        </View>
      </Send>
    );
  };

  const renderInputToolbar = (props: any) => {
    return (
      <InputToolbar
        {...props}
        containerStyle={styles.inputToolbar}
        primaryStyle={styles.inputPrimary}
      />
    );
  };

  const handleQuickResponse = (response: string) => {
    const message: ChatMessage = {
      _id: Math.round(Math.random() * 1000000),
      text: response,
      createdAt: new Date(),
      user: {
        _id: 1,
        name: 'You',
      },
    };
    onSend([message]);
  };

  return (
    <ThemedView style={styles.container}>
      <View style={styles.header}>
        <ThemedText type="title" style={styles.title}>Chat with Julia</ThemedText>
        <ThemedText style={styles.subtitle}>Your AI recovery companion</ThemedText>
      </View>
      
      {/* Quick Response Buttons */}
      <View style={styles.quickResponses}>
        <TouchableOpacity 
          style={styles.quickButton} 
          onPress={() => handleQuickResponse("I'm feeling good today!")}
        >
          <ThemedText style={styles.quickButtonText}>😊 Feeling Good</ThemedText>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={styles.quickButton} 
          onPress={() => handleQuickResponse("I'm having cravings")}
        >
          <ThemedText style={styles.quickButtonText}>⚠️ Having Cravings</ThemedText>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={styles.quickButton} 
          onPress={() => handleQuickResponse("I need support")}
        >
          <ThemedText style={styles.quickButtonText}>🤝 Need Support</ThemedText>
        </TouchableOpacity>
      </View>
      
      <GiftedChat
        messages={messages}
        onSend={onSend}
        user={{
          _id: 1,
          name: 'You',
        }}
        renderBubble={renderBubble}
        renderSend={renderSend}
        renderInputToolbar={renderInputToolbar}
        isTyping={isTyping}
        placeholder="Type your message..."
        alwaysShowSend
        showUserAvatar={false}
      />
    </ThemedView>
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
    backgroundColor: '#ffffff',
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 14,
    opacity: 0.7,
  },
  quickResponses: {
    flexDirection: 'row',
    padding: 16,
    gap: 8,
    backgroundColor: '#ffffff',
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  quickButton: {
    flex: 1,
    backgroundColor: '#eff6ff',
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 20,
    alignItems: 'center',
  },
  quickButtonText: {
    fontSize: 12,
    color: '#3b82f6',
    fontWeight: '500',
  },
  sendButton: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#3b82f6',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 8,
    marginBottom: 8,
  },
  inputToolbar: {
    backgroundColor: '#ffffff',
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
    paddingHorizontal: 8,
  },
  inputPrimary: {
    alignItems: 'center',
  },
}); 