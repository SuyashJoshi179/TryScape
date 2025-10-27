# TryScape Quick Start Guide

Get up and running with TryScape in just a few minutes!

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Python 3.8 or higher installed
- [ ] An Azure account
- [ ] Azure OpenAI Service created
- [ ] DALL-E 3 model deployed in Azure OpenAI

## 5-Minute Setup

### Step 1: Install Python (if needed)

Check if Python is installed:
```bash
python --version
```

If not installed, download from [python.org](https://www.python.org/downloads/)

### Step 2: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/SuyashJoshi179/TryScape.git
cd TryScape

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Azure OpenAI

1. **Create .env file**:
   ```bash
   cp .env.example .env
   ```

2. **Get Azure OpenAI credentials**:
   - Go to [Azure Portal](https://portal.azure.com)
   - Navigate to your Azure OpenAI resource
   - Click "Keys and Endpoint"
   - Copy the endpoint URL and API key

3. **Edit .env file** with your credentials:
   ```
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key-here
   AZURE_OPENAI_DEPLOYMENT_NAME=dall-e-3
   ```

### Step 4: Verify Installation

```bash
python verify_installation.py
```

You should see all green checkmarks ✓

### Step 5: Run the Application

```bash
python run.py
```

Open your browser to `http://localhost:5000`

## First Image Generation

1. **Prepare a photo** of yourself (any format: JPG, PNG, etc.)

2. **Open TryScape** in your browser (`http://localhost:5000`)

3. **Fill the form**:
   - Upload your photo
   - Clothing: "casual blue jeans and white t-shirt"
   - Location: "Central Park in New York with fall colors"

4. **Click "Generate TryScape"** and wait ~20 seconds

5. **View your result!** 🎉

## Next Steps

- Read [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for more scenarios
- Check [README.md](README.md) for detailed documentation
- Explore different outfit and location combinations

## Common Issues

### "Missing required environment variables"
→ Make sure you copied `.env.example` to `.env` and filled in your Azure credentials

### "Failed to generate image"
→ Verify your deployment name matches your Azure OpenAI DALL-E 3 deployment

### Dependencies won't install
→ Make sure you're using Python 3.8+ and have activated your virtual environment

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for usage examples
- Open an issue on GitHub if you encounter problems

## Azure OpenAI Setup Guide

If you don't have Azure OpenAI set up yet:

1. **Create Azure Account** at [azure.microsoft.com](https://azure.microsoft.com)

2. **Request Azure OpenAI Access**:
   - Go to [Azure OpenAI Access Request](https://aka.ms/oai/access)
   - Fill out the form and wait for approval (usually 1-2 business days)

3. **Create Azure OpenAI Resource**:
   - In Azure Portal, click "Create a resource"
   - Search for "Azure OpenAI"
   - Click "Create" and follow the wizard
   - Choose a region and pricing tier

4. **Deploy DALL-E 3 Model**:
   - In your Azure OpenAI resource, go to "Model deployments"
   - Click "Create new deployment"
   - Select "dall-e-3" model
   - Give it a name (e.g., "dall-e-3")
   - Click "Create"

5. **Get Credentials**:
   - Click "Keys and Endpoint" in the left menu
   - Copy your endpoint URL and one of the keys
   - Use these in your `.env` file

That's it! You're ready to use TryScape! 🚀
