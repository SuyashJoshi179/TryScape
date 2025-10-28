#!/bin/bash

# TryScape Azure Deployment Script
# This script deploys the TryScape application to Azure App Service using Azure CLI

set -e  # Exit on error

# Azure CLI path
AZ_CMD="/opt/homebrew/bin/az"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration variables (you can modify these)
RESOURCE_GROUP="${RESOURCE_GROUP:-tryscape-rg}"
LOCATION="${LOCATION:-eastus2}"
APP_NAME="${APP_NAME:-tryscape-app-$RANDOM}"
APP_SERVICE_PLAN="${APP_SERVICE_PLAN:-tryscape-plan}"
SKU="${SKU:-B1}"  # Basic tier
RUNTIME="${RUNTIME:-PYTHON:3.11}"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}TryScape Azure Deployment${NC}"
echo -e "${GREEN}========================================${NC}"

# Check if Azure CLI is installed
if ! command -v $AZ_CMD &> /dev/null; then
    echo -e "${RED}Error: Azure CLI is not installed${NC}"
    echo "Please install Azure CLI: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Check if logged in to Azure
echo -e "${YELLOW}Checking Azure login status...${NC}"
$AZ_CMD account show &> /dev/null || {
    echo -e "${YELLOW}Not logged in to Azure. Logging in...${NC}"
    $AZ_CMD login
}

# Get current subscription
SUBSCRIPTION_ID=$($AZ_CMD account show --query id -o tsv)
echo -e "${GREEN}Using subscription: ${SUBSCRIPTION_ID}${NC}"

# Prompt for environment variables if not set
echo -e "${YELLOW}Please provide the following Azure OpenAI credentials:${NC}"
read -p "Azure OpenAI Endpoint (e.g., https://your-resource.cognitiveservices.azure.com/): " AZURE_OPENAI_ENDPOINT
read -sp "Azure OpenAI API Key: " AZURE_OPENAI_API_KEY
echo ""
read -p "Azure OpenAI Deployment Name [gpt-image-1]: " AZURE_OPENAI_DEPLOYMENT_NAME
AZURE_OPENAI_DEPLOYMENT_NAME=${AZURE_OPENAI_DEPLOYMENT_NAME:-gpt-image-1}
read -p "Azure OpenAI API Version [2025-04-01-preview]: " AZURE_OPENAI_API_VERSION
AZURE_OPENAI_API_VERSION=${AZURE_OPENAI_API_VERSION:-2025-04-01-preview}

# Create resource group
echo -e "${YELLOW}Creating resource group: ${RESOURCE_GROUP}${NC}"
$AZ_CMD group create --name "$RESOURCE_GROUP" --location "$LOCATION" || {
    echo -e "${GREEN}Resource group already exists${NC}"
}

# Create App Service Plan
echo -e "${YELLOW}Creating App Service Plan: ${APP_SERVICE_PLAN}${NC}"
$AZ_CMD appservice plan create \
    --name "$APP_SERVICE_PLAN" \
    --resource-group "$RESOURCE_GROUP" \
    --location "$LOCATION" \
    --sku "$SKU" \
    --is-linux || {
    echo -e "${GREEN}App Service Plan already exists${NC}"
}

# Create Web App
echo -e "${YELLOW}Creating Web App: ${APP_NAME}${NC}"
$AZ_CMD webapp create \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --plan "$APP_SERVICE_PLAN" \
    --runtime "$RUNTIME" || {
    echo -e "${RED}Failed to create Web App${NC}"
    exit 1
}

# Configure Web App settings
echo -e "${YELLOW}Configuring Web App settings...${NC}"
$AZ_CMD webapp config appsettings set \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --settings \
        AZURE_OPENAI_ENDPOINT="$AZURE_OPENAI_ENDPOINT" \
        AZURE_OPENAI_API_KEY="$AZURE_OPENAI_API_KEY" \
        AZURE_OPENAI_DEPLOYMENT_NAME="$AZURE_OPENAI_DEPLOYMENT_NAME" \
        AZURE_OPENAI_API_VERSION="$AZURE_OPENAI_API_VERSION" \
        FLASK_ENV="production" \
        FLASK_DEBUG="False" \
        FLASK_RUN_HOST="0.0.0.0" \
        FLASK_RUN_PORT="4000" \
        ENABLE_SORA="false" \
        SCM_DO_BUILD_DURING_DEPLOYMENT="true" \
        WEBSITES_PORT="4000"

# Configure startup command
echo -e "${YELLOW}Configuring startup command...${NC}"
$AZ_CMD webapp config set \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --startup-file "python run.py"

# Enable logging
echo -e "${YELLOW}Enabling application logging...${NC}"
$AZ_CMD webapp log config \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --application-logging filesystem \
    --level information

# Deploy code
echo -e "${YELLOW}Deploying application code...${NC}"
$AZ_CMD webapp up \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --runtime "$RUNTIME" \
    --sku "$SKU"

# Get the URL
APP_URL=$($AZ_CMD webapp show --name "$APP_NAME" --resource-group "$RESOURCE_GROUP" --query defaultHostName -o tsv)

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}App Name: ${APP_NAME}${NC}"
echo -e "${GREEN}URL: https://${APP_URL}${NC}"
echo -e "${GREEN}Resource Group: ${RESOURCE_GROUP}${NC}"
echo ""
echo -e "${YELLOW}To view logs:${NC}"
echo "$AZ_CMD webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP"
echo ""
echo -e "${YELLOW}To browse the app:${NC}"
echo "$AZ_CMD webapp browse --name $APP_NAME --resource-group $RESOURCE_GROUP"
echo ""
echo -e "${YELLOW}To delete resources:${NC}"
echo "$AZ_CMD group delete --name $RESOURCE_GROUP --yes --no-wait"
