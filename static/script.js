// globals
chart = null;

function getscores() {
    let promise = new Promise((resolve, reject) => {
        $.get("/api/score", (data) => {
            if (data.success) {
                resolve(data.scores);
            } else {
                reject(data.error);
            }
        });
    });
    return promise
} 

function update() {
    getscores().then((data) => {
        newdata = ["Omimi", "Aoraki", "Clayton", "Toroa"]
        data.forEach(el => {
            index = newdata.indexOf(el.partyname)
            if (index >= 0) {
                newdata[index] = el
            } else {
                alert("Please specify the order correctly")
            }
        })
        data = newdata
        scores = data.map(el => el.score)
        names = data.map(el => el.partyname)
        colours = data.map(el => {
            switch(el.partyname) {
                case "Aoraki":
                    return 'rgba(235,0,0,1)'
                case "Omimi":
                    return 'rgba(255,230,0,1)'
                case "Toroa":
                    return 'rgba(10,235,10,1)'
                case "Clayton":
                    return 'rgba(0,0,235,1)'
                default:
                    return 'rgba(0,0,0,1)'
            }
        });
        data = {
            labels: names,
            datasets: [{
                label: 'Score',
                data: scores,
                backgroundColor: colours,
                borderColor: colours,
                borderWidth: 1,
            }]
        }
        // refresh
        chart.data = data;
        top_of_chart = Math.floor(Math.max(...scores) + 50)
        chart.options.scales.yAxes[0].ticks.max = top_of_chart;
        chart.update();
    });
}

$(document).ready(() => {
    console.log("Creating chart")
    data = {
        labels: [],
        datasets: [{
            label: 'Scores',
            data: [],
            backgroundColor: [],
            borderColor: [],
            borderWidth: 1,
        }]
    }
    const config = {
        type: 'bar',
        data: data,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        min: 0,
                        fontColor: '#fff',
                    },
                    gridLines: {
                        color: '#666666'
                    }
                }],
                xAxes: [{
                    ticks: {
                        fontColor: '#fff'
                    }
                }]
            },
            interaction: {
                showTooltips: false,
                mode: 'tooltip'
            },
            legend: {
                display: false
            },
            tooltips: {
                enabled: false
            },
            plugins: {
                datalabels: {
                    display: true,
                    color: "#eeeeee",
                    anchor: 'end',
                    align: 'top',
                }
            }
        },
    }
    Chart.plugins.register(ChartDataLabels);
    Chart.defaults.global.defaultFontSize = 25;
    Chart.defaults.global.animation.duration = 0;
    chart = new Chart(
        document.getElementById('scores'),
        config
    );
    setInterval(update, 1000);
});
