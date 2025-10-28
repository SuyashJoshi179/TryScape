# TryScape

**See yourself in any outfit, anywhere.** TryScape uses Azure OpenAI's gpt-image-1 to generate photorealistic images of you wearing specific outfits in any location you can imagine.

## Features

- 🖼️ **Photo Upload**: Upload your photo and clothing images
- 🎨 **AI-Powered Image Editing**: Uses Azure OpenAI gpt-image-1 for high-quality image generation
- 📍 **Any Location**: Visualize yourself at any location in the world
- 👔 **Outfit Visualization**: See how different outfits look on you
- 🌐 **Web Interface**: Easy-to-use web application

## Prerequisites

- Python 3.8 or higher
- Azure OpenAI Service subscription
- gpt-image-1 deployment in Azure OpenAI

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/SuyashJoshi179/TryScape.git
cd TryScape
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Azure OpenAI

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Azure OpenAI credentials:
   ```
   AZURE_OPENAI_ENDPOINT=https://tryscape.cognitiveservices.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key-here
   AZURE_OPENAI_API_VERSION=2025-04-01-preview
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-image-1
   ```

3. To get these credentials:
   - Go to [Azure Portal](https://portal.azure.com)
   - Navigate to your Azure OpenAI resource
   - Under "Keys and Endpoint", copy the endpoint and one of the keys
   - Ensure you have a gpt-image-1 model deployed

### 5. Run the Application

```bash
python run.py
```

The application will start on `http://localhost:5000`

## Usage

1. **Upload Your Photo**: Select a clear photo of yourself
2. **Describe Yourself** (optional): Add details like "young adult with brown hair"
3. **Upload Clothing Image** (optional): Upload a photo of the clothing
4. **Describe the Outfit**: Describe what you want to wear (e.g., "blue denim jacket and white t-shirt")
5. **Describe the Location**: Specify where you want to be (e.g., "Eiffel Tower in Paris at sunset")
6. **Generate**: Click the "Generate TryScape" button and wait 10-30 seconds

The AI will create a photorealistic image combining all these elements!

## Project Structure

```
TryScape/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   ├── uploads/          # User-uploaded images
│   │   └── generated/        # AI-generated images
│   ├── templates/
│   │   └── index.html
│   ├── utils/
│   │   ├── image_utils.py    # Image processing utilities
│   │   └── file_utils.py     # File handling utilities
│   ├── app.py                # Main Flask application
│   ├── azure_service.py      # Azure OpenAI integration
│   └── config.py             # Configuration management
├── .env.example              # Example environment variables
├── .gitignore
├── requirements.txt
├── run.py                    # Application entry point
└── README.md
```

## API Endpoints

### POST /generate
Generates a virtual try-on image by editing the user's photo with the selected clothing item.

**Request:**
- Content-Type: `multipart/form-data`
- Parameters:
  - `user_image`: User's photo (image file)
  - `cloth_image`: Clothing item image (image file)
  - `prompt`: Description of desired outfit transformation (text)

**Response:**
```json
{
  "success": true,
  "generated_media_url": "/static/generated/generated_<id>.png",
  "media_type": "image"
}
```

**Processing Time:** 60-120 seconds per request

### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "service": "TryScape",
  "timestamp": "2024-01-01T12:00:00"
}
```

## Technology Stack

- **Backend**: Python, Flask
- **AI Service**: Azure OpenAI (gpt-image-1)
- **Image Processing**: Pillow
- **Frontend**: HTML, CSS, JavaScript
- **Configuration**: python-dotenv

## Cost Considerations

Azure OpenAI gpt-image-1 is a paid service. Each image generation incurs a cost based on the API usage. Check [Azure OpenAI Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) for current rates.

**Note**: Image generation with gpt-image-1 typically takes 60-120 seconds to complete.

## Limitations

- Generated images are AI-created and may not be perfectly accurate
- Quality depends on the clarity of input descriptions
- Processing time varies (typically 10-30 seconds)
- Uploaded images should be clear and well-lit for best results

## Troubleshooting

### "Missing required environment variables" error
- Ensure `.env` file exists and contains all required variables
- Check that your Azure OpenAI endpoint and API key are correct

### "Failed to generate image" error
- Verify your Azure OpenAI deployment name is correct
- Ensure you have a gpt-image-1 deployment in your Azure OpenAI resource
- Check your API key has not expired
- Verify you have sufficient quota/credits

### Images not uploading
- Check file size (max 16MB)
- Ensure file format is supported (PNG, JPG, JPEG, GIF, WEBP)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.

## Acknowledgments

- Powered by Azure OpenAI Service
- Uses gpt-image-1 for image editing and generation
- Built with Flask web framework
