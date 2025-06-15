from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    aws_cognito as cognito,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_logs as logs,
    CfnOutput
)
from constructs import Construct
import json

class JuliaHealthStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create Cognito User Pool for authentication
        self.user_pool = self._create_user_pool()
        
        # Create User Pool Clients for SvelteKit and Expo
        self.web_client = self._create_web_client()
        self.mobile_client = self._create_mobile_client()
        
        # Create Identity Pool for AWS resource access
        self.identity_pool = self._create_identity_pool()
        
        # Create IAM roles for authenticated and unauthenticated users
        self.authenticated_role, self.unauthenticated_role = self._create_iam_roles()
        
        # Attach roles to Identity Pool
        self._attach_roles_to_identity_pool()
        
        # Create CloudWatch Log Group for authentication logs
        self.log_group = self._create_log_group()
        
        # Store configuration in SSM Parameter Store
        self._create_ssm_parameters()
        
        # Output important values
        self._create_outputs()

    def _create_user_pool(self) -> cognito.UserPool:
        """Create Cognito User Pool with healthcare-specific configuration"""
        
        return cognito.UserPool(
            self, "JuliaHealthUserPool",
            user_pool_name="julia-health-users",
            
            # Sign-in configuration
            sign_in_aliases=cognito.SignInAliases(
                email=True,
                username=False,
                phone=False
            ),
            
            # Self sign-up disabled for healthcare security
            self_sign_up_enabled=False,
            
            # Password policy for healthcare compliance
            password_policy=cognito.PasswordPolicy(
                min_length=12,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=True,
                temp_password_validity=Duration.days(1)
            ),
            
            # Account recovery
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            
            # Email configuration
            email=cognito.UserPoolEmail.with_cognito(
                reply_to="noreply@juliahealth.eu"
            ),
            
            # Standard attributes
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(
                    required=True,
                    mutable=True
                ),
                given_name=cognito.StandardAttribute(
                    required=True,
                    mutable=True
                ),
                family_name=cognito.StandardAttribute(
                    required=True,
                    mutable=True
                )
            ),
            
            # Custom attributes for role-based access
            custom_attributes={
                "role": cognito.StringAttribute(
                    min_len=1,
                    max_len=20,
                    mutable=False
                ),
                "patient_id": cognito.StringAttribute(
                    min_len=1,
                    max_len=50,
                    mutable=True
                ),
                "clinician_id": cognito.StringAttribute(
                    min_len=1,
                    max_len=50,
                    mutable=True
                ),
                "department": cognito.StringAttribute(
                    min_len=1,
                    max_len=100,
                    mutable=True
                )
            },
            
            # MFA configuration
            mfa=cognito.Mfa.OPTIONAL,
            mfa_second_factor=cognito.MfaSecondFactor(
                sms=True,
                otp=True
            ),
            
            # Advanced security
            advanced_security_mode=cognito.AdvancedSecurityMode.ENFORCED,
            
            # Device tracking
            device_tracking=cognito.DeviceTracking(
                challenge_required_on_new_device=True,
                device_only_remembered_on_user_prompt=True
            ),
            
            # Lambda triggers for custom logic
            lambda_triggers=cognito.UserPoolTriggers(
                # We'll add these later if needed
            ),
            
            # Deletion protection
            removal_policy=RemovalPolicy.RETAIN
        )

    def _create_web_client(self) -> cognito.UserPoolClient:
        """Create User Pool Client for SvelteKit web application"""
        
        return self.user_pool.add_client(
            "JuliaHealthWebClient",
            user_pool_client_name="julia-health-web-client",
            
            # OAuth configuration for web
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(
                    authorization_code_grant=True,
                    implicit_code_grant=False
                ),
                scopes=[
                    cognito.OAuthScope.EMAIL,
                    cognito.OAuthScope.OPENID,
                    cognito.OAuthScope.PROFILE
                ],
                callback_urls=[
                    "http://localhost:5173/auth/callback",  # Development
                    "https://portal.juliahealth.eu/auth/callback"  # Production
                ],
                logout_urls=[
                    "http://localhost:5173/auth/logout",  # Development
                    "https://portal.juliahealth.eu/auth/logout"  # Production
                ]
            ),
            
            # Auth flows
            auth_flows=cognito.AuthFlow(
                user_password=True,
                user_srp=True,
                admin_user_password=True
            ),
            
            # Token validity
            access_token_validity=Duration.hours(1),
            id_token_validity=Duration.hours(1),
            refresh_token_validity=Duration.days(30),
            
            # Security
            generate_secret=False,  # Web clients don't need secrets
            prevent_user_existence_errors=True,
            
            # Supported identity providers
            supported_identity_providers=[
                cognito.UserPoolClientIdentityProvider.COGNITO
            ]
        )

    def _create_mobile_client(self) -> cognito.UserPoolClient:
        """Create User Pool Client for Expo mobile application"""
        
        return self.user_pool.add_client(
            "JuliaHealthMobileClient",
            user_pool_client_name="julia-health-mobile-client",
            
            # OAuth configuration for mobile
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(
                    authorization_code_grant=True,
                    implicit_code_grant=False
                ),
                scopes=[
                    cognito.OAuthScope.EMAIL,
                    cognito.OAuthScope.OPENID,
                    cognito.OAuthScope.PROFILE
                ],
                callback_urls=[
                    "juliahealth://auth/callback",  # Deep link for mobile
                    "exp://192.168.0.34:8081/--/auth/callback"  # Expo development
                ],
                logout_urls=[
                    "juliahealth://auth/logout",
                    "exp://192.168.0.34:8081/--/auth/logout"
                ]
            ),
            
            # Auth flows
            auth_flows=cognito.AuthFlow(
                user_password=True,
                user_srp=True
            ),
            
            # Token validity
            access_token_validity=Duration.hours(1),
            id_token_validity=Duration.hours(1),
            refresh_token_validity=Duration.days(30),
            
            # Security
            generate_secret=False,  # Mobile clients don't need secrets
            prevent_user_existence_errors=True,
            
            # Supported identity providers
            supported_identity_providers=[
                cognito.UserPoolClientIdentityProvider.COGNITO
            ]
        )

    def _create_identity_pool(self) -> cognito.CfnIdentityPool:
        """Create Cognito Identity Pool for AWS resource access"""
        
        return cognito.CfnIdentityPool(
            self, "JuliaHealthIdentityPool",
            identity_pool_name="julia_health_identity_pool",
            allow_unauthenticated_identities=False,
            
            # Cognito Identity Providers
            cognito_identity_providers=[
                cognito.CfnIdentityPool.CognitoIdentityProviderProperty(
                    client_id=self.web_client.user_pool_client_id,
                    provider_name=self.user_pool.user_pool_provider_name,
                    server_side_token_check=True
                ),
                cognito.CfnIdentityPool.CognitoIdentityProviderProperty(
                    client_id=self.mobile_client.user_pool_client_id,
                    provider_name=self.user_pool.user_pool_provider_name,
                    server_side_token_check=True
                )
            ]
        )

    def _create_iam_roles(self) -> tuple:
        """Create IAM roles for authenticated and unauthenticated users"""
        
        # Authenticated user role
        authenticated_role = iam.Role(
            self, "JuliaHealthAuthenticatedRole",
            role_name="JuliaHealth-Authenticated-Role",
            assumed_by=iam.FederatedPrincipal(
                "cognito-identity.amazonaws.com",
                conditions={
                    "StringEquals": {
                        "cognito-identity.amazonaws.com:aud": self.identity_pool.ref
                    },
                    "ForAnyValue:StringLike": {
                        "cognito-identity.amazonaws.com:amr": "authenticated"
                    }
                },
                assume_role_action="sts:AssumeRoleWithWebIdentity"
            ),
            description="Role for authenticated JuliaHealth users"
        )
        
        # Authenticated user permissions
        authenticated_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    # CloudWatch Logs for application logging
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                    "logs:DescribeLogStreams",
                    
                    # S3 for file uploads (patient documents, etc.)
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject"
                ],
                resources=[
                    f"arn:aws:logs:eu-central-1:503561458783:log-group:/julia-health/*",
                    f"arn:aws:s3:::julia-health-patient-data-*/*"
                ]
            )
        )
        
        # Role-based permissions using conditions
        authenticated_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "execute-api:Invoke"
                ],
                resources=[
                    f"arn:aws:execute-api:eu-central-1:503561458783:*/*/patient/*"
                ],
                conditions={
                    "StringEquals": {
                        "cognito-identity.amazonaws.com:aud": self.identity_pool.ref
                    }
                }
            )
        )
        
        # Unauthenticated user role (minimal permissions)
        unauthenticated_role = iam.Role(
            self, "JuliaHealthUnauthenticatedRole",
            role_name="JuliaHealth-Unauthenticated-Role",
            assumed_by=iam.FederatedPrincipal(
                "cognito-identity.amazonaws.com",
                conditions={
                    "StringEquals": {
                        "cognito-identity.amazonaws.com:aud": self.identity_pool.ref
                    },
                    "ForAnyValue:StringLike": {
                        "cognito-identity.amazonaws.com:amr": "unauthenticated"
                    }
                },
                assume_role_action="sts:AssumeRoleWithWebIdentity"
            ),
            description="Role for unauthenticated JuliaHealth users"
        )
        
        # Minimal permissions for unauthenticated users
        unauthenticated_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "cognito-identity:GetId",
                    "cognito-identity:GetCredentialsForIdentity"
                ],
                resources=["*"]
            )
        )
        
        return authenticated_role, unauthenticated_role

    def _attach_roles_to_identity_pool(self):
        """Attach IAM roles to the Identity Pool"""
        
        # Create the role attachment without complex role mappings first
        # We'll use a simpler approach that works with CDK
        cognito.CfnIdentityPoolRoleAttachment(
            self, "JuliaHealthIdentityPoolRoleAttachment",
            identity_pool_id=self.identity_pool.ref,
            roles={
                "authenticated": self.authenticated_role.role_arn,
                "unauthenticated": self.unauthenticated_role.role_arn
            }
            # Note: Role mappings removed to fix CDK synthesis issue
            # Role-based access control will be handled at the application level
        )

    def _create_log_group(self) -> logs.LogGroup:
        """Create CloudWatch Log Group for authentication events"""
        
        return logs.LogGroup(
            self, "JuliaHealthAuthLogGroup",
            log_group_name="/julia-health/auth",
            retention=logs.RetentionDays.SIX_MONTHS,
            removal_policy=RemovalPolicy.RETAIN
        )

    def _create_ssm_parameters(self):
        """Store configuration in SSM Parameter Store for applications"""
        
        # User Pool configuration
        ssm.StringParameter(
            self, "UserPoolIdParameter",
            parameter_name="/julia-health/auth/user-pool-id",
            string_value=self.user_pool.user_pool_id,
            description="JuliaHealth Cognito User Pool ID"
        )
        
        ssm.StringParameter(
            self, "UserPoolArnParameter",
            parameter_name="/julia-health/auth/user-pool-arn",
            string_value=self.user_pool.user_pool_arn,
            description="JuliaHealth Cognito User Pool ARN"
        )
        
        # Web client configuration
        ssm.StringParameter(
            self, "WebClientIdParameter",
            parameter_name="/julia-health/auth/web-client-id",
            string_value=self.web_client.user_pool_client_id,
            description="JuliaHealth Web Client ID"
        )
        
        # Mobile client configuration
        ssm.StringParameter(
            self, "MobileClientIdParameter",
            parameter_name="/julia-health/auth/mobile-client-id",
            string_value=self.mobile_client.user_pool_client_id,
            description="JuliaHealth Mobile Client ID"
        )
        
        # Identity Pool configuration
        ssm.StringParameter(
            self, "IdentityPoolIdParameter",
            parameter_name="/julia-health/auth/identity-pool-id",
            string_value=self.identity_pool.ref,
            description="JuliaHealth Identity Pool ID"
        )
        
        # Region configuration
        ssm.StringParameter(
            self, "RegionParameter",
            parameter_name="/julia-health/auth/region",
            string_value=self.region,
            description="JuliaHealth AWS Region"
        )
        
        # Complete Amplify configuration as JSON
        amplify_config = {
            "Auth": {
                "Cognito": {
                    "userPoolId": self.user_pool.user_pool_id,
                    "userPoolClientId": self.web_client.user_pool_client_id,
                    "identityPoolId": self.identity_pool.ref,
                    "loginWith": {
                        "email": True
                    },
                    "signUpVerificationMethod": "code",
                    "userAttributes": {
                        "email": {
                            "required": True
                        }
                    },
                    "allowGuestAccess": False,
                    "passwordFormat": {
                        "minLength": 12,
                        "requireLowercase": True,
                        "requireUppercase": True,
                        "requireNumbers": True,
                        "requireSpecialCharacters": True
                    }
                }
            },
            "API": {
                "GraphQL": {
                    "endpoint": f"https://api.juliahealth.eu/graphql",
                    "region": "eu-central-1",
                    "defaultAuthMode": "userPool"
                }
            }
        }
        
        ssm.StringParameter(
            self, "AmplifyConfigParameter",
            parameter_name="/julia-health/auth/amplify-config",
            string_value=json.dumps(amplify_config, indent=2),
            description="Complete Amplify configuration for JuliaHealth applications"
        )

    def _create_outputs(self):
        """Create CloudFormation outputs for easy access to resource IDs"""
        
        CfnOutput(
            self, "UserPoolId",
            value=self.user_pool.user_pool_id,
            description="JuliaHealth Cognito User Pool ID",
            export_name="JuliaHealth-UserPool-Id"
        )
        
        CfnOutput(
            self, "UserPoolArn",
            value=self.user_pool.user_pool_arn,
            description="JuliaHealth Cognito User Pool ARN",
            export_name="JuliaHealth-UserPool-Arn"
        )
        
        CfnOutput(
            self, "WebClientId",
            value=self.web_client.user_pool_client_id,
            description="JuliaHealth Web Client ID",
            export_name="JuliaHealth-WebClient-Id"
        )
        
        CfnOutput(
            self, "MobileClientId",
            value=self.mobile_client.user_pool_client_id,
            description="JuliaHealth Mobile Client ID",
            export_name="JuliaHealth-MobileClient-Id"
        )
        
        CfnOutput(
            self, "IdentityPoolId",
            value=self.identity_pool.ref,
            description="JuliaHealth Identity Pool ID",
            export_name="JuliaHealth-IdentityPool-Id"
        )
        
        CfnOutput(
            self, "Region",
            value=self.region,
            description="JuliaHealth AWS Region",
            export_name="JuliaHealth-Region"
        )
        
        CfnOutput(
            self, "AuthenticatedRoleArn",
            value=self.authenticated_role.role_arn,
            description="JuliaHealth Authenticated Role ARN",
            export_name="JuliaHealth-AuthenticatedRole-Arn"
        ) 