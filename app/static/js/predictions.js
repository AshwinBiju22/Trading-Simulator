const ctxPred = document.getElementById('predictionChart').getContext('2d');
const predChart = new Chart(ctxPred, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            { label: 'Actual Close', data: [], borderColor: '#4bc0c0', fill: false },
            { label: 'Prediction', data: [], borderColor: '#ff6384', fill: false, borderDash: [5,5] }
        ]
    },
    options: { responsive: true }
});

async function fetchPredictionData() {
    const barsRes = await fetch('/bars?limit=50');
    const bars = await barsRes.json();

    const predRes = await fetch('/prediction');
    const pred = await predRes.json();

    document.getElementById('prediction').innerText = `Prediction: ${pred.next_close?.toFixed(2) || "N/A"}`;

    predChart.data.labels = bars.map(b => new Date(b.open_time).toLocaleTimeString());
    predChart.data.datasets[0].data = bars.map(b => b.close);
    predChart.data.datasets[1].data = [...bars.map(() => null), pred.next_close];
    predChart.update();
}

setInterval(fetchPredictionData, 2000);
fetchPredictionData();
