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

                    if (feedbackForm) {
                        feedbackForm.removeAttribute('hidden');
                    }
                };

                photoPreview.src = URL.createObjectURL(formData.get('file'));
            }
        });

        feedbackForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(feedbackForm);

            const feedbackResponse = await fetch('/feedback', {
                method: 'POST',
                body: formData
            });

            const feedbackData = await feedbackResponse.json();
            console.log(feedbackData);

            feedbackForm.reset();
            feedbackForm.setAttribute('hidden', 'true');
        });
    }
});