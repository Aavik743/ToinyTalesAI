// DOM Elements
const storyForm = document.getElementById('storyForm');
const storyOutput = document.getElementById('storyOutput');
const generatedStory = document.getElementById('generatedStory');
const storyAudio = document.getElementById('storyAudio');
const storyImage = document.getElementById('storyImage');

// Form submission handler
storyForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Get form values
    const childName = document.getElementById('childName').value.trim();
    const childAge = document.getElementById('childAge').value;
    const favoriteCharacters = document.getElementById('favoriteCharacters').value.trim();
    const interests = document.getElementById('interests').value.trim();

    // Basic validation
    if (!childName || !childAge) {
        alert('Please fill in required fields');
        return;
    }

    // Show loading state
    storyForm.querySelector('button').disabled = true;
    storyForm.querySelector('button').textContent = 'Creating Magic... ✨';

    try {
        // Prepare the prompt
        const prompt = `Create a captivating short story for a ${childAge}-year-old named ${childName}. Incorporate their favorite characters: ${favoriteCharacters || 'magical creatures'}, and set the adventure in a place that reflects their interests: ${interests || 'a fantastical world'}. Ensure the story is engaging, age-appropriate, and sparks their imagination.`;

        // Make API call to FastAPI backend
        const response = await fetch('/generate-story', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt }),
        });

        if (!response.ok) {
            throw new Error('Failed to generate story');
        }

        const data = await response.json();
        const storyText = data.story;

        // Display story
        generatedStory.textContent = storyText;

        // Set audio and image sources
        storyAudio.src = data.audio_url;
        storyImage.src = `http://localhost:8000${data.image_url}`;

        // Add error event listener to audio
        storyAudio.addEventListener('error', (e) => {
            console.log('Audio playback error:', e);
        });

        storyOutput.style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        alert('Oops! Something went wrong. Please try again later.');
    } finally {
        storyForm.querySelector('button').disabled = false;
        storyForm.querySelector('button').textContent = 'Create Magical Story 🌟';
    }
});

// Initialize form reset on page load
window.addEventListener('load', () => {
    storyForm.reset();
});