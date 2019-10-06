const chartColors = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};

// Generator that returns an iterator from start to end
function* range(start, end) {
    for (let i = start; i <= end; i++)
        yield i;
}

// Extract an (x/y/z) axis element from the IMU data (2D array)
function extractAxis(arr, axis) {
    data = [];
    for (let i = 0; i < arr.length; i++)
        data.push(arr[i][axis]);
    return data;
}

// Extract the latest data point from the IMU data (2D array)
function extractLatestPoint(arr, axis) {
    return (arr.length > 0 ? arr[arr.length - 1][axis] : 0);
}

// Update an IMU line chart with latest data
function updateImuLineChart(lineChart, currentData) {
    // Clean up the labels
    lineChart.data.labels = [...range(1, currentData.length)].map(i => -(currentData.length - i));

    // Update the chart data on each axis
    lineChart.data.datasets.forEach((dataset, i) => {
        dataset.data = extractAxis(currentData, i);
    });

    lineChart.update();
}

// Update an IMU bar chart with latest data
function updateImuBarChart(barChart, currentData) {
    // Update the chart data on each axis
    barChart.data.datasets.forEach((dataset, i) => {
        dataset.data = [extractLatestPoint(currentData, i)];
    });

    barChart.update();
}