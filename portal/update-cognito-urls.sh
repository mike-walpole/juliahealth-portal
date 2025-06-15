#!/bin/bash

# Update Cognito User Pool Client with production URLs
# Run this after deploying to AWS Amplify

REGION="eu-central-1"
USER_POOL_ID="eu-central-1_GFEq7NmJN"
CLIENT_ID="40aas3le2bf53c20vhj3q629so"

# Get your Amplify domain from the console and replace AMPLIFY_DOMAIN
AMPLIFY_DOMAIN="your-app-id.amplifyapp.com"  # Replace with actual domain
CUSTOM_DOMAIN="portal.juliahealth.eu"

echo "Updating Cognito callback URLs..."

aws cognito-idp update-user-pool-client \
  --region $REGION \
  --user-pool-id $USER_POOL_ID \
  --client-id $CLIENT_ID \
  --callback-urls \
    "https://$AMPLIFY_DOMAIN/auth/callback" \
    "https://$CUSTOM_DOMAIN/auth/callback" \
    "http://localhost:5173/auth/callback" \
  --logout-urls \
    "https://$AMPLIFY_DOMAIN/auth/logout" \
    "https://$CUSTOM_DOMAIN/auth/logout" \
    "http://localhost:5173/auth/logout" \
  --allowed-o-auth-flows "code" \
  --allowed-o-auth-scopes "email" "openid" "profile" \
  --allowed-o-auth-flows-user-pool-client \
  --supported-identity-providers "COGNITO"

if [ $? -eq 0 ]; then
    echo "✅ Cognito callback URLs updated successfully!"
    echo "Production URLs:"
    echo "  - https://$AMPLIFY_DOMAIN/auth/callback"
    echo "  - https://$CUSTOM_DOMAIN/auth/callback"
else
    echo "❌ Failed to update Cognito callback URLs"
    exit 1
fi 