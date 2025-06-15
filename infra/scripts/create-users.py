#!/usr/bin/env python3
"""
Script to create initial users for JuliaHealth platform
"""

import boto3
import json
import sys
from typing import Dict, List

class JuliaHealthUserManager:
    def __init__(self, user_pool_id: str, region: str = 'eu-central-1'):
        self.user_pool_id = user_pool_id
        self.region = region
        self.cognito = boto3.client('cognito-idp', region_name=region)
    
    def create_clinician(self, email: str, given_name: str, family_name: str, 
                        clinician_id: str, department: str, temp_password: str = None) -> Dict:
        """Create a clinician user"""
        
        if not temp_password:
            temp_password = "TempPass123!"
        
        user_attributes = [
            {'Name': 'email', 'Value': email},
            {'Name': 'given_name', 'Value': given_name},
            {'Name': 'family_name', 'Value': family_name},
            {'Name': 'custom:role', 'Value': 'clinician'},
            {'Name': 'custom:clinician_id', 'Value': clinician_id},
            {'Name': 'custom:department', 'Value': department}
        ]
        
        try:
            response = self.cognito.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=email,
                UserAttributes=user_attributes,
                TemporaryPassword=temp_password,
                MessageAction='SUPPRESS'  # Don't send welcome email
            )
            
            print(f"✅ Created clinician: {email}")
            print(f"   Temporary password: {temp_password}")
            print(f"   Department: {department}")
            return response
            
        except Exception as e:
            print(f"❌ Failed to create clinician {email}: {str(e)}")
            return None
    
    def create_patient(self, email: str, given_name: str, family_name: str, 
                      patient_id: str, temp_password: str = None) -> Dict:
        """Create a patient user"""
        
        if not temp_password:
            temp_password = "TempPass123!"
        
        user_attributes = [
            {'Name': 'email', 'Value': email},
            {'Name': 'given_name', 'Value': given_name},
            {'Name': 'family_name', 'Value': family_name},
            {'Name': 'custom:role', 'Value': 'patient'},
            {'Name': 'custom:patient_id', 'Value': patient_id}
        ]
        
        try:
            response = self.cognito.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=email,
                UserAttributes=user_attributes,
                TemporaryPassword=temp_password,
                MessageAction='SUPPRESS'  # Don't send welcome email
            )
            
            print(f"✅ Created patient: {email}")
            print(f"   Temporary password: {temp_password}")
            print(f"   Patient ID: {patient_id}")
            return response
            
        except Exception as e:
            print(f"❌ Failed to create patient {email}: {str(e)}")
            return None
    
    def list_users(self) -> List[Dict]:
        """List all users in the user pool"""
        
        try:
            response = self.cognito.list_users(UserPoolId=self.user_pool_id)
            return response.get('Users', [])
        except Exception as e:
            print(f"❌ Failed to list users: {str(e)}")
            return []
    
    def delete_user(self, username: str) -> bool:
        """Delete a user from the user pool"""
        
        try:
            self.cognito.admin_delete_user(
                UserPoolId=self.user_pool_id,
                Username=username
            )
            print(f"✅ Deleted user: {username}")
            return True
        except Exception as e:
            print(f"❌ Failed to delete user {username}: {str(e)}")
            return False

def get_user_pool_id_from_ssm() -> str:
    """Get User Pool ID from SSM Parameter Store"""
    
    ssm = boto3.client('ssm', region_name='eu-central-1')
    
    try:
        response = ssm.get_parameter(
            Name='/julia-health/auth/user-pool-id'
        )
        return response['Parameter']['Value']
    except Exception as e:
        print(f"❌ Failed to get User Pool ID from SSM: {str(e)}")
        print("Make sure you've deployed the infrastructure first!")
        sys.exit(1)

def create_demo_users():
    """Create demo users for testing"""
    
    print("🏥 JuliaHealth User Creation Script")
    print("=" * 40)
    
    # Get User Pool ID
    user_pool_id = get_user_pool_id_from_ssm()
    print(f"Using User Pool: {user_pool_id}")
    print()
    
    # Initialize user manager
    user_manager = JuliaHealthUserManager(user_pool_id)
    
    # Create demo clinicians
    print("Creating Clinicians:")
    print("-" * 20)
    
    clinicians = [
        {
            'email': 'dr.martinez@juliahealth.eu',
            'given_name': 'Dr. Elena',
            'family_name': 'Martinez',
            'clinician_id': 'CLIN001',
            'department': 'Addiction Medicine'
        },
        {
            'email': 'dr.johnson@juliahealth.eu',
            'given_name': 'Dr. Michael',
            'family_name': 'Johnson',
            'clinician_id': 'CLIN002',
            'department': 'Psychiatry'
        },
        {
            'email': 'nurse.williams@juliahealth.eu',
            'given_name': 'Sarah',
            'family_name': 'Williams',
            'clinician_id': 'CLIN003',
            'department': 'Recovery Support'
        }
    ]
    
    for clinician in clinicians:
        user_manager.create_clinician(**clinician)
    
    print()
    
    # Create demo patients
    print("Creating Patients:")
    print("-" * 20)
    
    patients = [
        {
            'email': 'sarah.chen@email.com',
            'given_name': 'Sarah',
            'family_name': 'Chen',
            'patient_id': 'PAT001'
        },
        {
            'email': 'marcus.rodriguez@email.com',
            'given_name': 'Marcus',
            'family_name': 'Rodriguez',
            'patient_id': 'PAT002'
        },
        {
            'email': 'jessica.thompson@email.com',
            'given_name': 'Jessica',
            'family_name': 'Thompson',
            'patient_id': 'PAT003'
        },
        {
            'email': 'robert.williams@email.com',
            'given_name': 'Robert',
            'family_name': 'Williams',
            'patient_id': 'PAT004'
        }
    ]
    
    for patient in patients:
        user_manager.create_patient(**patient)
    
    print()
    print("✅ Demo users created successfully!")
    print()
    print("📋 Next Steps:")
    print("1. Users can sign in with their email and temporary password")
    print("2. They'll be prompted to set a permanent password on first login")
    print("3. Consider enabling MFA for additional security")
    print()
    print("🔐 Default temporary password: TempPass123!")

def list_all_users():
    """List all users in the user pool"""
    
    user_pool_id = get_user_pool_id_from_ssm()
    user_manager = JuliaHealthUserManager(user_pool_id)
    
    users = user_manager.list_users()
    
    print(f"📋 Users in User Pool ({len(users)} total):")
    print("=" * 50)
    
    for user in users:
        username = user['Username']
        status = user['UserStatus']
        
        # Extract attributes
        attributes = {attr['Name']: attr['Value'] for attr in user['Attributes']}
        
        role = attributes.get('custom:role', 'Unknown')
        email = attributes.get('email', 'No email')
        name = f"{attributes.get('given_name', '')} {attributes.get('family_name', '')}"
        
        print(f"👤 {name.strip()}")
        print(f"   Email: {email}")
        print(f"   Role: {role}")
        print(f"   Status: {status}")
        print(f"   Username: {username}")
        print()

def main():
    """Main function"""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python create-users.py create-demo    # Create demo users")
        print("  python create-users.py list           # List all users")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'create-demo':
        create_demo_users()
    elif command == 'list':
        list_all_users()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main() 