const chartColors = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};

// generator that returns an iterator from start to end
function* range(start, end) {
    for (let i = start; i <= end; i++)
        yield i;
}

// extract axis element from 2D array IMU data
function extractAxis(arr, axis) {
    data = [];
    for (let i = 0; i < arr.length; i++)
        data.push(arr[i][axis]);
    return data;
}

function extractLastPoint(arr, axis) {
    return (arr.length > 0 ? arr[arr.length - 1][axis] : 0);
}

function updateLineChart(lineChart, currentData) {
    // Clean up the labels
    lineChart.data.labels = [...range(1, currentData.length)].map(i => -(currentData.length - i));

    // Update the chart data on each axis
    lineChart.data.datasets.forEach((dataset, i) => {
        dataset.data = extractAxis(currentData, i);
    });

    lineChart.update();
}

function updateBarChart(barChart, currentData) {
    // Update the chart data on each axis
    barChart.data.datasets.forEach((dataset, i) => {
        dataset.data = [extractLastPoint(currentData, i)];
    });

    barChart.update();
}