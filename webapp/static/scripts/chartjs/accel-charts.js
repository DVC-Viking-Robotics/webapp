const configAccelLineChart = {
    type: 'line',
    data: {
        labels: [...range(1, accel_data.length)].map(i => -(accel_data.length - i)),
        datasets: [{
            label: 'X Axis',
            backgroundColor: chartColors.red,
            borderColor: chartColors.red,
            data: extractAxis(accel_data, 0),
            fill: false,
        }, {
            label: 'Y Axis',
            fill: false,
            backgroundColor: chartColors.blue,
            borderColor: chartColors.blue,
            data: extractAxis(accel_data, 1),
        }, {
            label: 'Z Axis',
            fill: false,
            backgroundColor: chartColors.green,
            borderColor: chartColors.green,
            data: extractAxis(accel_data, 2),
        }]
    },
    options: {
        aspectRatio: 3,
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Time Elapsed'
                }
            }],
            yAxes: [{
                display: true,
                ticks: {
                    min: -100,
                    max: 100,
                },
            }]
        }
    }
};

const configAccelBarChart = {
    type: 'bar',
    data: {
        datasets: [{
            label: 'X Axis',
            backgroundColor: chartColors.red,
            borderColor: chartColors.red,
            data: extractLastPoint(accel_data, 0),
            fill: false,
        }, {
            label: 'Y Axis',
            fill: false,
            backgroundColor: chartColors.blue,
            borderColor: chartColors.blue,
            data: extractLastPoint(accel_data, 1),
        }, {
            label: 'Z Axis',
            fill: false,
            backgroundColor: chartColors.green,
            borderColor: chartColors.green,
            data: extractLastPoint(accel_data, 2),
        }]
    },
    options: {
        aspectRatio: 1.4,
        tooltips: {
            mode: 'dataset',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            yAxes: [{
                display: true,
                ticks: {
                    min: -100,
                    max: 100,
                },
            }]
        }
    }
};