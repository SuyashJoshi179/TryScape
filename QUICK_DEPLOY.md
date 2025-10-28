# 🚀 Quick Deploy to Azure

Choose your deployment method and follow the steps below.

## ⚡ Method 1: Azure CLI (Fastest - 5 minutes)

**Best for**: Quick testing, development

### Prerequisites
- Azure CLI installed ([Install here](https://docs.microsoft.com/cli/azure/install-azure-cli))
- Azure account with active subscription
- Azure OpenAI resource with gpt-image-1 deployed

### Deploy Now

```bash
# 1. Make script executable
chmod +x deploy-azure.sh

# 2. Run deployment
./deploy-azure.sh
```

The script will:
- ✅ Log you into Azure (if needed)
- ✅ Ask for your Azure OpenAI credentials
- ✅ Create all necessary resources
- ✅ Deploy the application
- ✅ Give you the URL

**You'll need:**
- Azure OpenAI Endpoint: `https://your-resource.cognitiveservices.azure.com/`
- Azure OpenAI API Key: (from Azure Portal)
- Deployment Name: `gpt-image-1`

### After Deployment

```bash
# View your app
az webapp browse --name $APP_NAME --resource-group tryscape-rg

# Check logs
az webapp log tail --name $APP_NAME --resource-group tryscape-rg
```

---

## 🔄 Method 2: GitHub Actions (Automated - 10 minutes setup)

**Best for**: Production, continuous deployment

### Step 1: Create Service Principal

```bash
az ad sp create-for-rbac --name "tryscape-deploy" \
  --role contributor \
  --scopes /subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/tryscape-rg \
  --sdk-auth
```

Copy the entire JSON output.

### Step 2: Add GitHub Secrets

Go to: `GitHub Repo → Settings → Secrets → Actions → New repository secret`

Add these secrets:

| Secret Name | Value |
|------------|-------|
| `AZURE_CREDENTIALS` | Paste the full JSON from Step 1 |
| `AZURE_OPENAI_ENDPOINT` | `https://your-resource.cognitiveservices.azure.com/` |
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | `gpt-image-1` |

### Step 3: Create Azure Resources

```bash
# Create resource group
az group create --name tryscape-rg --location eastus

# Create App Service Plan
az appservice plan create \
  --name tryscape-plan \
  --resource-group tryscape-rg \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --name tryscape-app \
  --resource-group tryscape-rg \
  --plan tryscape-plan \
  --runtime "PYTHON:3.11"
```

### Step 4: Update Workflow

Edit `.github/workflows/azure-deploy.yml`:

```yaml
env:
  AZURE_WEBAPP_NAME: tryscape-app    # ← Your actual app name
```

### Step 5: Deploy

```bash
git add .
git commit -m "Deploy to Azure"
git push origin main
```

Or trigger manually from GitHub Actions tab.

---

## 📋 Quick Checklist

Before deploying, ensure you have:

- [ ] Azure account
- [ ] Azure CLI installed
- [ ] Azure OpenAI resource created
- [ ] `gpt-image-1` model deployed
- [ ] Endpoint URL and API key ready

---

## 🆘 Quick Troubleshooting

### App won't start?
```bash
# Check logs
az webapp log tail --name $APP_NAME --resource-group tryscape-rg

# Restart app
az webapp restart --name $APP_NAME --resource-group tryscape-rg
```

### Image generation fails?
```bash
# Verify credentials
az webapp config appsettings list \
  --name $APP_NAME \
  --resource-group tryscape-rg \
  --query "[?name=='AZURE_OPENAI_ENDPOINT' || name=='AZURE_OPENAI_API_KEY']"
```

### Need to update settings?
```bash
az webapp config appsettings set \
  --name $APP_NAME \
  --resource-group tryscape-rg \
  --settings AZURE_OPENAI_ENDPOINT="new-value"
```

---

## 💰 Cost Estimate

- **Azure App Service (B1)**: ~$13-15/month
- **Azure OpenAI (gpt-image-1)**: Pay per use (~60-120s per image)

Set budget alerts in Azure Portal!

---

## 📚 Detailed Guides

- **Full Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Checklist**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
- **Summary**: [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)

---

## ❌ Delete Everything

When you're done:

```bash
az group delete --name tryscape-rg --yes --no-wait
```

---

**Questions?** Check [DEPLOYMENT.md](DEPLOYMENT.md) or open an issue on GitHub.

**Ready to deploy?** Run `./deploy-azure.sh` now! 🚀
