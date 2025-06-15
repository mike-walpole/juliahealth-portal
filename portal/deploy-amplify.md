# Deploy JuliaHealth Portal to AWS Amplify

## Prerequisites

1. **AWS CLI configured** with appropriate permissions
2. **GitHub repository** with your code
3. **Domain configured** (juliahealth.eu)

## Step 1: Create Amplify App

```bash
# Navigate to AWS Amplify Console
# https://console.aws.amazon.com/amplify/

# Or use AWS CLI
aws amplify create-app \
  --name "JuliaHealth-Portal" \
  --description "JuliaHealth Clinician Portal" \
  --repository "https://github.com/yourusername/juliahealth-portal" \
  --platform "WEB" \
  --region "eu-central-1"
```

## Step 2: Configure Build Settings

In the Amplify Console:

1. **Connect Repository**: Link your GitHub repo
2. **Branch**: Select `main` or `production` branch
3. **Build Settings**: Use the provided `amplify.yml` file
4. **Environment Variables**: Add if needed

## Step 3: Domain Configuration

1. **Add Domain**: `juliahealth.eu`
2. **Subdomain**: `portal.juliahealth.eu`
3. **SSL Certificate**: Auto-provisioned by Amplify
4. **DNS Configuration**: Update your domain's DNS to point to Amplify

### DNS Records

Add these records to your domain provider:

```
Type: CNAME
Name: portal
Value: [amplify-domain-from-console]

Type: CNAME  
Name: www.portal
Value: [amplify-domain-from-console]
```

## Step 4: Environment Variables (if needed)

In Amplify Console > App Settings > Environment Variables:

```
NODE_VERSION = 18
```

## Step 5: Build and Deploy

1. **Trigger Build**: Push to your connected branch
2. **Monitor Build**: Check build logs in Amplify Console
3. **Test Deployment**: Visit `https://portal.juliahealth.eu`

## Step 6: Configure Cognito Callbacks

Update your Cognito User Pool settings:

```bash
# Update callback URLs to include your Amplify domain
aws cognito-idp update-user-pool-client \
  --user-pool-id eu-central-1_GFEq7NmJN \
  --client-id 40aas3le2bf53c20vhj3q629so \
  --callback-urls "https://portal.juliahealth.eu/auth/callback" "http://localhost:5173/auth/callback" \
  --logout-urls "https://portal.juliahealth.eu/auth/logout" "http://localhost:5173/auth/logout"
```

## Step 7: Test Authentication

1. **Visit Portal**: `https://portal.juliahealth.eu`
2. **Login**: Use demo credentials:
   - Email: `dr.martinez@juliahealth.eu`
   - Password: `TempPass123!` (will prompt for new password)
3. **Verify**: Check that authentication works and redirects properly

## Troubleshooting

### Build Failures

- Check Node.js version compatibility
- Verify all dependencies are in package.json
- Check build logs for specific errors

### Authentication Issues

- Verify Cognito callback URLs match exactly
- Check browser console for CORS errors
- Ensure HTTPS is working properly

### Domain Issues

- DNS propagation can take up to 48 hours
- Verify SSL certificate is active
- Check domain configuration in Amplify Console

## Security Considerations

1. **HTTPS Only**: Ensure all traffic uses HTTPS
2. **CSP Headers**: Content Security Policy configured in amplify.yml
3. **HSTS**: HTTP Strict Transport Security enabled
4. **Cognito Security**: Advanced security features enabled

## Monitoring

- **CloudWatch**: Monitor application performance
- **Amplify Console**: Build and deployment logs
- **Cognito Metrics**: Authentication success/failure rates

## Cost Optimization

- **Amplify Pricing**: Pay per build minute and data transfer
- **CloudFront**: Included CDN for global distribution
- **SSL Certificate**: Free with Amplify

## Next Steps

1. Set up custom domain with your DNS provider
2. Configure monitoring and alerting
3. Set up staging environment for testing
4. Implement CI/CD pipeline for automated deployments 