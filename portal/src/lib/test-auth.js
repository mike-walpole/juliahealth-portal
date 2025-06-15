// Simple test to check if Amplify is configured correctly
import { Amplify } from 'aws-amplify';

console.log('🔧 Testing Amplify configuration...');

try {
  const config = Amplify.getConfig();
  console.log('📋 Amplify config:', config);
  
  if (config.Auth?.Cognito) {
    console.log('✅ Cognito configuration found');
    console.log('🏠 User Pool ID:', config.Auth.Cognito.userPoolId);
    console.log('🔑 Client ID:', config.Auth.Cognito.userPoolClientId);
  } else {
    console.log('❌ No Cognito configuration found');
  }
} catch (error) {
  console.error('💥 Error checking Amplify config:', error);
}

export function testAmplifyConfig() {
  console.log('🧪 Running Amplify config test...');
  return Amplify.getConfig();
} 