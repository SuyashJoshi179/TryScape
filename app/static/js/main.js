// TryScape JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('tryscape-form');
    const userImageInput = document.getElementById('user_image');
    const clothingImageInput = document.getElementById('clothing_image');
    const userFilename = document.getElementById('user-filename');
    const clothingFilename = document.getElementById('clothing-filename');
    const loadingOverlay = document.getElementById('loading');
    const resultCard = document.getElementById('result');
    const generatedImage = document.getElementById('generated-image');
    const errorDiv = document.getElementById('error');
    const errorText = document.getElementById('error-text');
    const newGenerationBtn = document.getElementById('new-generation-btn');
    const dismissErrorBtn = document.getElementById('dismiss-error-btn');

    // Update filename display when user selects a file
    userImageInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            userFilename.textContent = this.files[0].name;
        } else {
            userFilename.textContent = 'No file chosen';
        }
    });

    clothingImageInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            clothingFilename.textContent = this.files[0].name;
        } else {
            clothingFilename.textContent = 'No file chosen (optional)';
        }
    });

    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Validate form
        if (!userImageInput.files || !userImageInput.files[0]) {
            showError('Please select a photo of yourself');
            return;
        }

        // Hide previous results/errors
        hideError();
        resultCard.style.display = 'none';

        // Show loading overlay
        loadingOverlay.style.display = 'flex';

        // Prepare form data
        const formData = new FormData(form);

        try {
            // Send request to generate image
            const response = await fetch('/generate', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Show generated image
                generatedImage.src = data.generated_image_url;
                resultCard.style.display = 'block';
                
                // Scroll to result
                resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                showError(data.error || 'Failed to generate image. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Network error. Please check your connection and try again.');
        } finally {
            // Hide loading overlay
            loadingOverlay.style.display = 'none';
        }
    });

    // Handle new generation button
    newGenerationBtn.addEventListener('click', function() {
        resultCard.style.display = 'none';
        form.scrollIntoView({ behavior: 'smooth' });
    });

    // Handle error dismiss
    dismissErrorBtn.addEventListener('click', function() {
        hideError();
    });

    function showError(message) {
        errorText.textContent = message;
        errorDiv.style.display = 'block';
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function hideError() {
        errorDiv.style.display = 'none';
    }
});
