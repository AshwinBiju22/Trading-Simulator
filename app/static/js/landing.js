// Fetch live prices every 2 seconds
async function fetchPrices() {
    const symbols = ["btcusdt", "ethusdt"];
    for (let symbol of symbols) {
        const response = await fetch(`/bars?symbol=${symbol}&limit=1`);
        const data = await response.json();
        const price = data[0]?.close || 0;
        if (symbol === "btcusdt") document.getElementById("btc-price").textContent = `$${price.toFixed(2)}`;
        if (symbol === "ethusdt") document.getElementById("eth-price").textContent = `$${price.toFixed(2)}`;
    }
}

// Fetch BTC prediction every 5 seconds
async function fetchPrediction() {
    const response = await fetch("/prediction?symbol=btcusdt");
    const data = await response.json();
    document.getElementById("btc-prediction").textContent = `$${data.next_close?.toFixed(2) || 0}`;
}

// Setup charts
const priceCtx = document.getElementById("priceChart").getContext("2d");
const priceChart = new Chart(priceCtx, {
    type: "line",
    data: {
        labels: [],
        datasets: [{
            label: "BTC/USD",
            data: [],
            borderColor: "#58a6ff",
            backgroundColor: "rgba(88,166,255,0.2)",
            tension: 0.3,
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { labels: { color: "#c9d1d9" } } },
        scales: {
            x: { ticks: { color: "#c9d1d9" } },
            y: { ticks: { color: "#c9d1d9" } }
        }
    }
});

async function updateChart() {
    const response = await fetch("/bars?symbol=btcusdt&limit=50");
    const data = await response.json();
    priceChart.data.labels = data.map(d => new Date(d.time).toLocaleTimeString());
    priceChart.data.datasets[0].data = data.map(d => d.close);
    priceChart.update();
}

// Initial load
fetchPrices();
fetchPrediction();
updateChart();

// Auto-refresh intervals
setInterval(fetchPrices, 2000);
setInterval(fetchPrediction, 5000);
setInterval(updateChart, 5000);
