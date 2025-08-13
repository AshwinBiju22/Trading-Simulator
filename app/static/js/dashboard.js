const ctx = document.getElementById('priceChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            { label: 'Close Price', data: [], borderColor: '#4bc0c0', fill: false }
        ]
    },
    options: {
        responsive: true,
        scales: { x: { display: true }, y: { display: true } }
    }
});

async function fetchBars() {
    const res = await fetch('/bars?limit=50');
    const bars = await res.json();
    chart.data.labels = bars.map(b => new Date(b.open_time).toLocaleTimeString());
    chart.data.datasets[0].data = bars.map(b => b.close);
    chart.update();
}

setInterval(fetchBars, 2000);
fetchBars();
