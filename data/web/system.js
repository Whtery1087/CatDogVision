const form = document.querySelector('form');
const photoContainer = document.querySelector('#photo-container');
const photoPreview = document.querySelector('#photo-preview');
const result = document.querySelector('#result');
form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const response = await fetch('/predict', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    result.textContent = `Prediction: ${data.prediction}`;

    if (data.probability !== undefined) {
        result.textContent += `, Probability: ${data.probability.toFixed(2)}%`;
    }

    photoContainer.style.display = 'block';
    photoPreview.src = URL.createObjectURL(formData.get('file'));

    if (data.prediction === 'Cat') {
        result.classList.add('cat');
    } else if (data.prediction === 'Dog') {
        result.classList.add('dog');
    }
});