#!/usr/bin/env python3
import os
import aws_cdk as cdk
from julia_health.julia_health_stack import JuliaHealthStack

app = cdk.App()

# Account and region configuration
account_id = "503561458783"
region = "eu-central-1"

# Environment configuration
env = cdk.Environment(
    account=account_id,
    region=region
)

# Create the main stack
julia_health_stack = JuliaHealthStack(
    app, 
    "JuliaHealthStack",
    env=env,
    description="JuliaHealth - Patient Recovery Platform Infrastructure"
)

# Add tags to all resources
cdk.Tags.of(app).add("Project", "JuliaHealth")
cdk.Tags.of(app).add("Environment", "Production")
cdk.Tags.of(app).add("Owner", "JuliaHealth-Team")
cdk.Tags.of(app).add("CostCenter", "Healthcare")

app.synth() 