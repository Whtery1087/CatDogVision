document.addEventListener('DOMContentLoaded', async () => {
    const form = document.querySelector('form');
    const photoContainer = document.querySelector('#photo-container');
    const result = document.querySelector('#result');
    const feedbackForm = document.querySelector('#feedback-form');

    if (form) {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(form);
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (result) {
                result.textContent = `Prediction: ${data.prediction}`;

                if (data.probability !== undefined) {
                    result.textContent += `, Probability: ${data.probability.toFixed(2)}%`;
                }
            }

            if (photoContainer) {
                const photoPreview = document.querySelector('#photo-preview');
                photoPreview.onload = () => {
                    photoContainer.style.display = 'block';

                    if (result) {
                        if (data.prediction === 'Cat') {
                            result.classList.add('cat');
                        } else if (data.prediction === 'Dog') {
                            result.classList.add('dog');
                        }
                    }

                    // Remove the 'hidden' attribute to show the feedback form
                    if (feedbackForm) {
                        feedbackForm.removeAttribute('hidden');
                    }
                };

                photoPreview.src = URL.createObjectURL(formData.get('file'));
            }
        });

        // Add a submit event listener to the feedback form
        feedbackForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(feedbackForm);

            // Use fetch to send feedback data to the server
            const feedbackResponse = await fetch('/feedback', {
                method: 'POST',
                body: formData
            });

            // Handle the feedback response as needed
            const feedbackData = await feedbackResponse.json();
            console.log(feedbackData);

            // Optionally, reset or hide the form after feedback submission
            feedbackForm.reset();
            feedbackForm.setAttribute('hidden', 'true');
        });
    }
});