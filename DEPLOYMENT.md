# TryScape Azure Deployment Guide

This guide provides step-by-step instructions for deploying TryScape to Azure using either Azure CLI or GitHub Actions.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Option 1: Deploy with Azure CLI Script](#option-1-deploy-with-azure-cli-script)
- [Option 2: Deploy with GitHub Actions](#option-2-deploy-with-github-actions)
- [Post-Deployment Configuration](#post-deployment-configuration)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

1. **Azure Account**
   - Active Azure subscription
   - Azure CLI installed: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

2. **Azure OpenAI Service**
   - Azure OpenAI resource created
   - `gpt-image-1` model deployed
   - Endpoint URL and API key available

3. **GitHub Account** (for GitHub Actions deployment)
   - Repository access
   - Ability to add secrets

---

## Option 1: Deploy with Azure CLI Script

### Step 1: Prepare Environment

```bash
# Clone the repository (if not already done)
git clone https://github.com/SuyashJoshi179/TryScape.git
cd TryScape

# Make the deployment script executable
chmod +x deploy-azure.sh
```

### Step 2: Run Deployment Script

```bash
./deploy-azure.sh
```

The script will:
1. Check if you're logged into Azure (and log you in if not)
2. Prompt for your Azure OpenAI credentials:
   - **Endpoint**: `https://your-resource.cognitiveservices.azure.com/`
   - **API Key**: Your Azure OpenAI API key
   - **Deployment Name**: `gpt-image-1` (default)
   - **API Version**: `2025-04-01-preview` (default)
3. Create necessary Azure resources:
   - Resource Group: `tryscape-rg`
   - App Service Plan: `tryscape-plan` (B1 tier)
   - Web App: `tryscape-app-XXXXX`
4. Configure application settings
5. Deploy the application code

### Step 3: Verify Deployment

After successful deployment, the script will output:
```
========================================
Deployment completed successfully!
========================================
App Name: tryscape-app-12345
URL: https://tryscape-app-12345.azurewebsites.net
Resource Group: tryscape-rg
```

Visit the URL to access your deployed application.

### Customization Options

You can customize the deployment by setting environment variables:

```bash
# Custom configuration
export RESOURCE_GROUP="my-tryscape-rg"
export LOCATION="westus2"
export APP_NAME="my-tryscape-app"
export APP_SERVICE_PLAN="my-plan"
export SKU="S1"  # Standard tier for better performance

# Run deployment
./deploy-azure.sh
```

---

## Option 2: Deploy with GitHub Actions

### Step 1: Create Azure Service Principal

```bash
# Login to Azure
az login

# Create a service principal
az ad sp create-for-rbac --name "tryscape-github-actions" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
  --sdk-auth

# This will output JSON - save it for the next step
```

### Step 2: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add the following secrets:

1. **AZURE_CREDENTIALS**
   ```json
   {
     "clientId": "...",
     "clientSecret": "...",
     "subscriptionId": "...",
     "tenantId": "..."
   }
   ```
   (Paste the entire JSON output from Step 1)

2. **AZURE_OPENAI_ENDPOINT**
   ```
   https://your-resource.cognitiveservices.azure.com/
   ```

3. **AZURE_OPENAI_API_KEY**
   ```
   your-azure-openai-api-key
   ```

4. **AZURE_OPENAI_DEPLOYMENT_NAME**
   ```
   gpt-image-1
   ```

### Step 3: Create Azure Web App

Before running the GitHub Action, create the Web App manually:

```bash
# Set variables
RESOURCE_GROUP="tryscape-rg"
LOCATION="eastus"
APP_NAME="tryscape-app"
APP_SERVICE_PLAN="tryscape-plan"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service Plan
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --runtime "PYTHON:3.11"

# Configure startup command
az webapp config set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --startup-file "python run.py"
```

### Step 4: Update Workflow Configuration

Edit `.github/workflows/azure-deploy.yml` and update:

```yaml
env:
  AZURE_WEBAPP_NAME: tryscape-app    # Your actual app name
  PYTHON_VERSION: '3.11'
```

### Step 5: Deploy

Push to the main branch or manually trigger the workflow:

**Automatic Deployment:**
```bash
git add .
git commit -m "Deploy to Azure"
git push origin main
```

**Manual Trigger:**
- Go to GitHub Actions tab
- Select "Deploy to Azure App Service"
- Click "Run workflow"

### Step 6: Monitor Deployment

- Go to GitHub → Actions tab
- Watch the deployment progress
- Check for any errors in the logs

---

## Post-Deployment Configuration

### Enable Continuous Deployment Logs

```bash
az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP
```

### Configure Custom Domain (Optional)

```bash
# Add custom domain
az webapp config hostname add \
  --webapp-name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --hostname www.yourdomain.com

# Enable HTTPS
az webapp update \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --https-only true
```

### Scale the Application

```bash
# Scale up (increase instance size)
az appservice plan update \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --sku S1

# Scale out (increase instance count)
az appservice plan update \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --number-of-workers 2
```

### Configure Persistent Storage (Optional)

For uploaded and generated images:

```bash
# Enable Azure Files for persistent storage
az webapp config storage-account add \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --custom-id uploads \
  --storage-type AzureFiles \
  --share-name tryscape-uploads \
  --account-name mystorageaccount \
  --mount-path /app/app/static/uploads \
  --access-key $STORAGE_ACCESS_KEY
```

---

## Troubleshooting

### Common Issues

#### 1. Application Not Starting

**Check logs:**
```bash
az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP
```

**Common causes:**
- Missing environment variables
- Incorrect startup command
- Python version mismatch

**Solution:**
```bash
# Verify app settings
az webapp config appsettings list \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP

# Update startup command
az webapp config set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --startup-file "python run.py"
```

#### 2. Image Generation Fails

**Causes:**
- Incorrect Azure OpenAI credentials
- Network connectivity issues
- Quota limits exceeded

**Solution:**
```bash
# Verify environment variables
az webapp config appsettings list \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "[?name=='AZURE_OPENAI_ENDPOINT' || name=='AZURE_OPENAI_API_KEY']"

# Update if needed
az webapp config appsettings set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings AZURE_OPENAI_ENDPOINT="https://your-resource.cognitiveservices.azure.com/"
```

#### 3. Timeout Issues

For gpt-image-1's 60-120 second processing time:

```bash
# Increase timeout
az webapp config set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --web-sockets-enabled true

# Or upgrade to a higher tier with better performance
az appservice plan update \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --sku S1
```

#### 4. Storage Issues

If uploaded images are lost after restart:

**Enable persistent storage** (see Post-Deployment Configuration above)

Or use **Azure Blob Storage**:
- Update `app/utils/file_utils.py` to use Azure Blob Storage
- Add `azure-storage-blob` to requirements.txt

#### 5. GitHub Actions Deployment Fails

**Check:**
- Service principal credentials are correct
- Web App exists before deployment
- All required secrets are set
- Branch protection rules aren't blocking deployment

**Re-create service principal:**
```bash
az ad sp create-for-rbac --name "tryscape-github-actions" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
  --sdk-auth
```

---

## Monitoring and Maintenance

### View Application Insights

```bash
# Enable Application Insights
az monitor app-insights component create \
  --app tryscape-insights \
  --location $LOCATION \
  --resource-group $RESOURCE_GROUP \
  --application-type web

# Link to Web App
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app tryscape-insights \
  --resource-group $RESOURCE_GROUP \
  --query instrumentationKey -o tsv)

az webapp config appsettings set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY=$INSTRUMENTATION_KEY
```

### Set Up Alerts

```bash
# Alert on high CPU usage
az monitor metrics alert create \
  --name high-cpu-alert \
  --resource-group $RESOURCE_GROUP \
  --scopes /subscriptions/{subscription-id}/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Web/sites/$APP_NAME \
  --condition "avg Percentage CPU > 80" \
  --description "Alert when CPU exceeds 80%"
```

---

## Cleanup

### Delete All Resources

```bash
# Delete entire resource group (THIS WILL DELETE EVERYTHING)
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

### Delete Specific Resources

```bash
# Delete only the Web App
az webapp delete --name $APP_NAME --resource-group $RESOURCE_GROUP

# Delete App Service Plan
az appservice plan delete --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP
```

---

## Cost Optimization

1. **Use Basic (B1) tier for development/testing**
2. **Use Standard (S1) or Premium for production**
3. **Scale down during off-hours:**
   ```bash
   az appservice plan update --name $APP_SERVICE_PLAN --sku B1
   ```
4. **Monitor Azure OpenAI usage** - gpt-image-1 processing costs
5. **Set up budget alerts** in Azure Portal

---

## Security Best Practices

1. **Never commit secrets to Git**
   - Use Azure Key Vault for production
   - Use GitHub Secrets for CI/CD

2. **Enable HTTPS only:**
   ```bash
   az webapp update --name $APP_NAME --https-only true
   ```

3. **Restrict network access:**
   ```bash
   az webapp config access-restriction add \
     --name $APP_NAME \
     --resource-group $RESOURCE_GROUP \
     --rule-name "allow-office" \
     --action Allow \
     --ip-address "YOUR_IP/32" \
     --priority 100
   ```

4. **Enable managed identity:**
   ```bash
   az webapp identity assign --name $APP_NAME --resource-group $RESOURCE_GROUP
   ```

---

## Support

- **Azure Documentation**: https://docs.microsoft.com/azure/app-service/
- **GitHub Actions**: https://docs.github.com/actions
- **Azure OpenAI**: https://learn.microsoft.com/azure/ai-services/openai/

For application-specific issues, check the [main README](README.md) or open an issue on GitHub.
