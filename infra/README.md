# JuliaHealth Infrastructure

This directory contains the AWS CDK infrastructure code for the JuliaHealth patient recovery platform.

## Architecture Overview

The infrastructure includes:

- **AWS Cognito User Pool**: Authentication for clinicians and patients
- **AWS Cognito Identity Pool**: AWS resource access management
- **IAM Roles**: Role-based access control for different user types
- **CloudWatch Logs**: Authentication and application logging
- **SSM Parameter Store**: Configuration management

## Prerequisites

1. **AWS CLI configured** with your credentials
2. **AWS CDK installed**: `npm install -g aws-cdk`
3. **Python 3.8+** installed
4. **Virtual environment** (recommended)

## Setup

### 1. Create Virtual Environment

```bash
cd infra
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Bootstrap CDK (First time only)

```bash
cdk bootstrap aws://503561458783/eu-central-1
```

## Deployment

### 1. Synthesize CloudFormation Template

```bash
cdk synth
```

### 2. Deploy Infrastructure

```bash
cdk deploy
```

### 3. View Outputs

After deployment, note the outputs:
- `UserPoolId`: For Amplify configuration
- `WebClientId`: For SvelteKit portal
- `MobileClientId`: For Expo app
- `IdentityPoolId`: For AWS resource access

## Configuration

### Environment Variables

The stack is configured for:
- **Account**: 503561458783
- **Region**: eu-central-1

### User Pool Configuration

- **Password Policy**: 12+ characters, mixed case, numbers, symbols
- **MFA**: Optional (SMS and TOTP)
- **Advanced Security**: Enabled
- **Self Sign-up**: Disabled (admin-managed for healthcare)

### Custom Attributes

- `custom:role`: "clinician" or "patient"
- `custom:patient_id`: Links to patient records
- `custom:clinician_id`: Links to clinician records
- `custom:department`: Clinician department

## Integration

### SvelteKit Portal

```javascript
// src/lib/auth.js
import { Amplify } from 'aws-amplify';

Amplify.configure({
  Auth: {
    Cognito: {
      userPoolId: 'eu-central-1_XXXXXXXXX',
      userPoolClientId: 'XXXXXXXXXXXXXXXXXXXXXXXXXX',
      identityPoolId: 'eu-central-1:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX',
    }
  }
});
```

### Expo Mobile App

```javascript
// services/auth.js
import { Amplify } from 'aws-amplify';

Amplify.configure({
  Auth: {
    Cognito: {
      userPoolId: 'eu-central-1_XXXXXXXXX',
      userPoolClientId: 'XXXXXXXXXXXXXXXXXXXXXXXXXX',
      identityPoolId: 'eu-central-1:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX',
    }
  }
});
```

## User Management

### Creating Users

Users must be created by administrators:

```bash
aws cognito-idp admin-create-user \
  --user-pool-id eu-central-1_XXXXXXXXX \
  --username "clinician@juliahealth.eu" \
  --user-attributes Name=email,Value="clinician@juliahealth.eu" \
                    Name=given_name,Value="Dr. Sarah" \
                    Name=family_name,Value="Johnson" \
                    Name=custom:role,Value="clinician" \
                    Name=custom:clinician_id,Value="CLIN001" \
                    Name=custom:department,Value="Addiction Medicine" \
  --temporary-password "TempPass123!" \
  --message-action SUPPRESS
```

### Patient User Creation

```bash
aws cognito-idp admin-create-user \
  --user-pool-id eu-central-1_XXXXXXXXX \
  --username "patient@email.com" \
  --user-attributes Name=email,Value="patient@email.com" \
                    Name=given_name,Value="Sarah" \
                    Name=family_name,Value="Chen" \
                    Name=custom:role,Value="patient" \
                    Name=custom:patient_id,Value="PAT001" \
  --temporary-password "TempPass123!" \
  --message-action SUPPRESS
```

## Security Features

### Password Policy
- Minimum 12 characters
- Requires uppercase, lowercase, numbers, symbols
- Temporary password expires in 1 day

### Advanced Security
- Risk-based authentication
- Device tracking
- Compromised credentials detection

### MFA Options
- SMS-based MFA
- TOTP (Time-based One-Time Password)
- Optional but recommended for healthcare

## Monitoring

### CloudWatch Logs
- Authentication events: `/julia-health/auth`
- Application logs: `/julia-health/app`

### Metrics
- Sign-in success/failure rates
- MFA usage
- Risk events

## Cleanup

To destroy the infrastructure:

```bash
cdk destroy
```

**Warning**: This will delete all authentication data. Ensure you have backups if needed.

## Troubleshooting

### Common Issues

1. **Bootstrap Error**: Ensure CDK is bootstrapped in the correct region
2. **Permission Denied**: Check AWS credentials and IAM permissions
3. **Resource Limits**: Verify account limits for Cognito resources

### Support

For infrastructure issues, check:
1. CloudFormation events in AWS Console
2. CDK deployment logs
3. CloudWatch logs for runtime issues

## Next Steps

After deployment:
1. Configure applications with the output values
2. Create initial admin users
3. Set up monitoring and alerting
4. Configure backup and disaster recovery 