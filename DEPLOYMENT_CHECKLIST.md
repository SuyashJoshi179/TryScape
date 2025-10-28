# TryScape Deployment Checklist

Use this checklist to ensure a successful deployment to Azure.

## Pre-Deployment Checklist

### Azure Resources
- [ ] Azure account created and active
- [ ] Azure CLI installed and configured (`az --version`)
- [ ] Logged into Azure (`az login`)
- [ ] Azure OpenAI resource created
- [ ] `gpt-image-1` model deployed in Azure OpenAI
- [ ] Azure OpenAI endpoint URL available
- [ ] Azure OpenAI API key available

### GitHub Setup (for GitHub Actions)
- [ ] Repository is on GitHub
- [ ] GitHub Actions enabled for repository
- [ ] Service principal created for GitHub Actions
- [ ] GitHub Secrets configured:
  - [ ] `AZURE_CREDENTIALS`
  - [ ] `AZURE_OPENAI_ENDPOINT`
  - [ ] `AZURE_OPENAI_API_KEY`
  - [ ] `AZURE_OPENAI_DEPLOYMENT_NAME`

### Local Environment
- [ ] Code tested locally
- [ ] All dependencies listed in `requirements.txt`
- [ ] `.env` file configured (not committed to Git)
- [ ] `verify_installation.py` passes

## Deployment Method Selection

### Option A: Azure CLI Deployment
**Best for:** Quick deployment, testing, manual control

**Steps:**
1. [ ] Run `./deploy-azure.sh`
2. [ ] Provide Azure OpenAI credentials when prompted
3. [ ] Note the deployed URL
4. [ ] Test the application

### Option B: GitHub Actions Deployment
**Best for:** CI/CD, automated deployments, production

**Steps:**
1. [ ] Configure GitHub Secrets (see above)
2. [ ] Create Azure Web App manually
3. [ ] Update `.github/workflows/azure-deploy.yml` with app name
4. [ ] Push to main branch or trigger workflow manually
5. [ ] Monitor deployment in GitHub Actions tab
6. [ ] Test the application

## Post-Deployment Checklist

### Verification
- [ ] Application URL is accessible
- [ ] Home page loads correctly
- [ ] Can upload user photo
- [ ] Can upload clothing image
- [ ] Image generation works (test with sample images)
- [ ] Generated image displays correctly
- [ ] No errors in browser console
- [ ] No errors in application logs

### Configuration
- [ ] All environment variables set correctly
- [ ] HTTPS enabled (`https-only`)
- [ ] Correct Python runtime version (3.11)
- [ ] Startup command configured (`python run.py`)
- [ ] Port configuration correct (`4000`)
- [ ] Application logging enabled

### Performance
- [ ] App Service tier appropriate for load (B1 for dev, S1+ for prod)
- [ ] Image generation completes within timeout (60-120 seconds)
- [ ] No memory issues
- [ ] No CPU throttling

### Security
- [ ] API keys stored in App Settings (not in code)
- [ ] `.env` file in `.gitignore`
- [ ] HTTPS only enabled
- [ ] No secrets in logs
- [ ] Network access restrictions configured (if needed)

### Monitoring
- [ ] Application logs viewable (`az webapp log tail`)
- [ ] Application Insights configured (optional)
- [ ] Budget alerts set up
- [ ] Error alerts configured

## Testing Checklist

### Functional Tests
- [ ] Upload PNG image → Success
- [ ] Upload JPEG image → Success
- [ ] Upload large image (>5MB) → Success or appropriate error
- [ ] Invalid file type → Appropriate error message
- [ ] Missing required fields → Validation error
- [ ] Image generation with simple prompt → Success
- [ ] Image generation with complex prompt → Success
- [ ] Generated image quality acceptable

### Load Tests (Production)
- [ ] Multiple concurrent requests handled
- [ ] No timeout errors under normal load
- [ ] Memory usage stable
- [ ] CPU usage acceptable

### Error Handling
- [ ] Invalid Azure credentials → Clear error message
- [ ] Network timeout → User-friendly error
- [ ] Large file upload → Size limit enforced
- [ ] Missing environment variables → Startup fails with clear message

## Rollback Plan

If deployment fails or issues are found:

### Immediate Actions
- [ ] Check application logs: `az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP`
- [ ] Verify environment variables: `az webapp config appsettings list --name $APP_NAME --resource-group $RESOURCE_GROUP`
- [ ] Restart app: `az webapp restart --name $APP_NAME --resource-group $RESOURCE_GROUP`

### Rollback Options
- [ ] Redeploy previous version from GitHub
- [ ] Restore from deployment slot (if configured)
- [ ] Delete and recreate Web App
- [ ] Fall back to local development environment

## Cost Monitoring

- [ ] Review Azure pricing for chosen tier
- [ ] Estimate Azure OpenAI costs (gpt-image-1 usage)
- [ ] Set up cost alerts in Azure Portal
- [ ] Monitor daily/weekly costs
- [ ] Plan for scaling down during off-hours

## Documentation

- [ ] Update `README.md` with deployment URL
- [ ] Document any custom configurations
- [ ] Share access credentials with team (securely)
- [ ] Update runbook with production-specific details

## Final Steps

- [ ] Inform stakeholders of deployment
- [ ] Share application URL
- [ ] Schedule follow-up review (1 week)
- [ ] Monitor for 24-48 hours post-deployment
- [ ] Gather user feedback
- [ ] Plan next iteration/improvements

---

## Quick Commands Reference

### View logs
```bash
az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP
```

### Restart app
```bash
az webapp restart --name $APP_NAME --resource-group $RESOURCE_GROUP
```

### Update environment variable
```bash
az webapp config appsettings set --name $APP_NAME --resource-group $RESOURCE_GROUP --settings KEY=VALUE
```

### Scale up
```bash
az appservice plan update --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku S1
```

### Enable HTTPS
```bash
az webapp update --name $APP_NAME --resource-group $RESOURCE_GROUP --https-only true
```

### Delete resources
```bash
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

---

## Support Contacts

- **Azure Support**: https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade
- **GitHub Actions**: https://docs.github.com/actions
- **Project Issues**: https://github.com/SuyashJoshi179/TryScape/issues

---

**Last Updated**: October 27, 2025
