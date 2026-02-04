document.getElementById('get-recommendation').addEventListener('click', async () => {
    const location = document.getElementById('location').value.trim();
    const budget = document.getElementById('budget').value.trim();

    if (!location || !budget) {
        alert('Please enter both location and budget.');
        return;
    }

    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    const recommendationText = document.getElementById('recommendation-text');

    // Show loading, hide result
    loadingDiv.classList.remove('hidden');
    resultDiv.classList.add('hidden');

    try {
        const response = await fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                location: location,
                budget: budget
            })
        });

        const data = await response.json();

        if (response.ok) {
            recommendationText.innerText = data.recommendation;
            resultDiv.classList.remove('hidden');
        } else {
            alert('Error: ' + (data.error || 'Something went wrong'));
        }
    } catch (error) {
        console.error('Fetch error:', error);
        alert('Failed to connect to the server.');
    } finally {
        loadingDiv.classList.add('hidden');
    }
});
