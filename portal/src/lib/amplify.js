import { Amplify } from 'aws-amplify';

const amplifyConfig = {
  Auth: {
    Cognito: {
      userPoolId: 'eu-central-1_GFEq7NmJN',
      userPoolClientId: '40aas3le2bf53c20vhj3q629so',
      identityPoolId: 'eu-central-1:4787a40b-cada-42ed-9998-ce8a64ffcd98',
      loginWith: {
        email: true
      },
      signUpVerificationMethod: 'code',
      userAttributes: {
        email: {
          required: true
        }
      },
      allowGuestAccess: false,
      passwordFormat: {
        minLength: 12,
        requireLowercase: true,
        requireUppercase: true,
        requireNumbers: true,
        requireSpecialCharacters: true
      }
    }
  },
  API: {
    GraphQL: {
      endpoint: 'https://api.juliahealth.eu/graphql',
      region: 'eu-central-1',
      defaultAuthMode: 'userPool'
    }
  }
};

Amplify.configure(amplifyConfig);

export default amplifyConfig; 