# TryScape Usage Examples

This document provides examples of how to use the TryScape application.

## Basic Usage Through Web Interface

1. Start the application:
   ```bash
   python run.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Fill in the form:
   - **Upload Your Photo**: Choose a clear photo of yourself
   - **Describe Yourself** (optional): Add details like "young adult with brown hair"
   - **Upload Clothing Image** (optional): Upload a photo of the clothing you want to wear
   - **Describe the Outfit**: Describe the clothing (e.g., "blue denim jacket and white t-shirt")
   - **Describe the Location**: Specify the location (e.g., "Eiffel Tower in Paris at sunset")

4. Click "Generate TryScape" and wait 10-30 seconds for the AI to generate your image

## Example Scenarios

### Scenario 1: Vacation Planning
**Use Case**: You want to see how you'd look in casual beachwear at a tropical destination

**Input**:
- User Description: "person with long dark hair"
- Clothing Description: "white linen shirt and khaki shorts"
- Location Description: "tropical beach in Maldives with turquoise water and white sand"

**Result**: AI-generated image showing you in beachwear at a tropical beach

### Scenario 2: Special Event
**Use Case**: Planning what to wear for a formal event in a specific venue

**Input**:
- User Description: "young professional"
- Clothing Description: "elegant black suit with red tie"
- Location Description: "grand ballroom with crystal chandeliers and marble floors"

**Result**: AI-generated image showing you in formal attire in the ballroom

### Scenario 3: Travel Outfit Planning
**Use Case**: Visualize yourself in travel outfits at famous landmarks

**Input**:
- User Description: "traveler"
- Clothing Description: "casual denim jacket, jeans, and comfortable sneakers"
- Location Description: "Times Square in New York City at night with bright neon lights"

**Result**: AI-generated image showing you in casual attire at Times Square

### Scenario 4: Fashion Experiment
**Use Case**: Try out bold fashion choices in different settings

**Input**:
- User Description: "fashion-forward individual"
- Clothing Description: "vibrant red dress with floral patterns"
- Location Description: "art museum with modern architecture and natural lighting"

**Result**: AI-generated image showing you in the dress at the museum

## API Usage Examples

If you want to integrate TryScape into your own application, you can use the REST API:

### Generate Image via API

```python
import requests

url = 'http://localhost:5000/generate'

# Prepare form data
files = {
    'user_image': open('path/to/your/photo.jpg', 'rb'),
}

data = {
    'user_description': 'young adult with brown hair',
    'clothing_description': 'blue denim jacket and white t-shirt',
    'location_description': 'Eiffel Tower in Paris at sunset'
}

# Send request
response = requests.post(url, files=files, data=data)

if response.status_code == 200:
    result = response.json()
    print(f"Generated image URL: {result['generated_image_url']}")
else:
    print(f"Error: {response.json()['error']}")
```

### Health Check

```python
import requests

response = requests.get('http://localhost:5000/health')
print(response.json())
# Output: {'status': 'healthy', 'service': 'TryScape', 'timestamp': '...'}
```

## Tips for Best Results

1. **Clear Photos**: Use clear, well-lit photos of yourself
2. **Detailed Descriptions**: The more detailed your descriptions, the better the results
3. **Realistic Expectations**: AI-generated images may not be 100% accurate
4. **Lighting Conditions**: Specify lighting conditions in location descriptions for better atmosphere
5. **Specific Locations**: Be specific about locations (e.g., "Golden Gate Bridge at sunset" vs just "bridge")

## Common Use Cases

- **Travel Planning**: Visualize yourself at destinations before booking
- **Outfit Selection**: See how different outfits look in various settings
- **Event Planning**: Plan outfits for weddings, parties, or professional events
- **Fashion Experimentation**: Try bold fashion choices without commitment
- **Social Media Content**: Create unique content for social media
- **Virtual Tourism**: Experience famous landmarks virtually

## Limitations

- Generated images are AI-created and may not perfectly match reality
- The AI interprets descriptions, so results may vary
- Processing takes 10-30 seconds per image
- Quality depends on input image quality and description detail
- Some complex scenarios may not generate perfectly

## Cost Management

Each image generation uses Azure OpenAI credits. To manage costs:
- Generate images thoughtfully rather than repeatedly
- Use clear descriptions to minimize regeneration needs
- Monitor your Azure OpenAI usage in the Azure Portal
- Set up budget alerts in Azure

## Troubleshooting

### Image Generation Takes Too Long
- This is normal; DALL-E 3 typically takes 10-30 seconds
- Check your internet connection
- Verify Azure OpenAI service is operational

### Generated Image Doesn't Match Expectations
- Try more detailed descriptions
- Be specific about colors, styles, and lighting
- Ensure your user photo is clear and well-lit

### Upload Fails
- Check file size (max 16MB)
- Ensure file format is supported (PNG, JPG, JPEG, GIF, WEBP)
- Try a different browser if issues persist
