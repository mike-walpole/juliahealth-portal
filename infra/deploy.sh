#!/bin/bash

# JuliaHealth Infrastructure Deployment Script
set -e

echo "🏥 JuliaHealth Infrastructure Deployment"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ACCOUNT_ID="503561458783"
REGION="eu-central-1"
STACK_NAME="JuliaHealthStack"

# Functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if AWS CLI is installed
    if ! command -v aws &> /dev/null; then
        log_error "AWS CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check if CDK is installed
    if ! command -v cdk &> /dev/null; then
        log_error "AWS CDK is not installed. Please install it with: npm install -g aws-cdk"
        exit 1
    fi
    
    # Check if Python 3 is installed
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed. Please install it first."
        exit 1
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        log_error "AWS credentials not configured. Please run 'aws configure' first."
        exit 1
    fi
    
    log_success "All prerequisites met"
}

# Setup virtual environment
setup_venv() {
    log_info "Setting up Python virtual environment..."
    
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        log_success "Created virtual environment"
    else
        log_info "Virtual environment already exists"
    fi
    
    source .venv/bin/activate
    pip install -r requirements.txt
    log_success "Dependencies installed"
}

# Bootstrap CDK
bootstrap_cdk() {
    log_info "Checking CDK bootstrap status..."
    
    # Check if already bootstrapped
    if aws cloudformation describe-stacks --stack-name CDKToolkit --region $REGION &> /dev/null; then
        log_info "CDK already bootstrapped in $REGION"
    else
        log_info "Bootstrapping CDK in $REGION..."
        cdk bootstrap aws://$ACCOUNT_ID/$REGION
        log_success "CDK bootstrapped successfully"
    fi
}

# Deploy infrastructure
deploy_infrastructure() {
    log_info "Deploying JuliaHealth infrastructure..."
    
    # Synthesize first to check for errors
    log_info "Synthesizing CloudFormation template..."
    cdk synth
    
    # Deploy the stack
    log_info "Deploying stack..."
    cdk deploy --require-approval never
    
    log_success "Infrastructure deployed successfully!"
}

# Get outputs
get_outputs() {
    log_info "Retrieving deployment outputs..."
    
    # Get stack outputs
    OUTPUTS=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].Outputs' \
        --output json)
    
    echo ""
    echo "📋 Deployment Outputs:"
    echo "====================="
    
    # Parse and display outputs
    echo "$OUTPUTS" | jq -r '.[] | "• \(.OutputKey): \(.OutputValue)"'
    
    echo ""
    log_info "Configuration stored in SSM Parameter Store:"
    echo "• /julia-health/auth/user-pool-id"
    echo "• /julia-health/auth/web-client-id"
    echo "• /julia-health/auth/mobile-client-id"
    echo "• /julia-health/auth/identity-pool-id"
    echo "• /julia-health/auth/amplify-config"
}

# Create demo users
create_demo_users() {
    echo ""
    read -p "Would you like to create demo users? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Creating demo users..."
        python3 scripts/create-users.py create-demo
        log_success "Demo users created"
    else
        log_info "Skipping demo user creation"
        log_info "You can create them later with: python3 scripts/create-users.py create-demo"
    fi
}

# Show next steps
show_next_steps() {
    echo ""
    echo "🎉 Deployment Complete!"
    echo "======================"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Update your SvelteKit portal with the new auth configuration"
    echo "2. Update your Expo app with the new auth configuration"
    echo "3. Test authentication with the demo users"
    echo "4. Set up monitoring and alerting"
    echo ""
    echo "🔐 Demo User Credentials:"
    echo "• Email: dr.martinez@juliahealth.eu (Clinician)"
    echo "• Email: sarah.chen@email.com (Patient)"
    echo "• Password: TempPass123! (temporary - will be prompted to change)"
    echo ""
    echo "📚 Documentation:"
    echo "• Infrastructure: infra/README.md"
    echo "• User Management: python3 scripts/create-users.py list"
    echo ""
    echo "🔧 Useful Commands:"
    echo "• List users: python3 scripts/create-users.py list"
    echo "• View logs: aws logs tail /julia-health/auth --follow"
    echo "• Update stack: cdk deploy"
    echo "• Destroy stack: cdk destroy"
}

# Main execution
main() {
    # Change to script directory
    cd "$(dirname "$0")"
    
    # Run deployment steps
    check_prerequisites
    setup_venv
    bootstrap_cdk
    deploy_infrastructure
    get_outputs
    create_demo_users
    show_next_steps
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "destroy")
        log_warning "This will destroy all JuliaHealth infrastructure!"
        read -p "Are you sure? Type 'yes' to confirm: " -r
        if [[ $REPLY == "yes" ]]; then
            source .venv/bin/activate 2>/dev/null || true
            cdk destroy
            log_success "Infrastructure destroyed"
        else
            log_info "Destruction cancelled"
        fi
        ;;
    "diff")
        source .venv/bin/activate
        cdk diff
        ;;
    "synth")
        source .venv/bin/activate
        cdk synth
        ;;
    *)
        echo "Usage: $0 [deploy|destroy|diff|synth]"
        echo ""
        echo "Commands:"
        echo "  deploy  - Deploy the infrastructure (default)"
        echo "  destroy - Destroy the infrastructure"
        echo "  diff    - Show differences between deployed and local"
        echo "  synth   - Synthesize CloudFormation template"
        exit 1
        ;;
esac 