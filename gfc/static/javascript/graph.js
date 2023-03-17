/*
    Creates a chart using the data provided
*/
function setChart(chartDataset, chartLabels, yAxisLabel="", xAxisLabel="", chartType="line", yBeginsAtZero=false, xBeginsAtZero=false) {
    const ctx = document.getElementById("chart"+ chartName);

    if (ctx.attributes.length > 1) { // if there is a chart in the canvas.
          Chart.getChart(ctx).destroy(); // clear the canvas
    }

    Chart.defaults.color = '{{primary}} !IMPORTANT';
    if (chartType == "line"| chartType == "bar") {
      setLineChart(ctx, chartDataset, chartLabels, yAxisLabel, xAxisLabel, yBeginsAtZero, xBeginsAtZero)
    }
    else if (chartType == "pie" || chartType == "doughnut") {
        setRoundChart(ctx, chartType, chartLabels, yAxisLabel, chartDataset)
    }
}

/*
    Creates a line graph using the data provided
*/
function setLineChart(ctx, chartDataset, chartLabels, yAxisLabel="", xAxisLabel="", yBeginsAtZero=false, xBeginsAtZero=false) {
    new Chart(ctx, {
        type: "line",
        data: {
            labels: chartLabels,
            datasets: chartDataset
        },
        options: {
            scales: {
            y: {
                title: {
                    display: true,
                    text: yAxisLabel,
                    },
                beginAtZero: yBeginsAtZero
            },
            x: {
                title: {
                    display: true,
                    text: xAxisLabel,
                    },
                beginAtZero: xBeginsAtZero
            }
            },
            aspectRatio: 1.7
        }
    });
}

/*
    Creates a rounded chart using the data provided
*/
function setRoundChart(ctx, chartType, chartLabels, dataLabels, chartDataset) {
    new Chart(ctx, {
        type: chartType,
        data: {
            labels: chartLabels,
            datasets: [{
            label: dataLabels,
            data: chartDataset,
            borderWidth: 1
            }]
        },
    });
}