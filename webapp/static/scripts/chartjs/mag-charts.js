const configMagLineChart = {
    type: 'line',
    data: {
        labels: [...range(1, NUM_POINTS)].map(i => -(NUM_POINTS - i)),
        datasets: [{
            label: 'X Axis',
            backgroundColor: chartColors.red,
            borderColor: chartColors.red,
            data: extractAxis(mag_data, 0),
            fill: false,
        }, {
            label: 'Y Axis',
            fill: false,
            backgroundColor: chartColors.blue,
            borderColor: chartColors.blue,
            data: extractAxis(mag_data, 1),
        }, {
            label: 'Z Axis',
            fill: false,
            backgroundColor: chartColors.green,
            borderColor: chartColors.green,
            data: extractAxis(mag_data, 2),
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
                scaleLabel: {
                    display: true,
                    labelString: 'Value'
                }
            }]
        }
    }
};

const configMagBarChart = {
    type: 'bar',
    data: {
        datasets: [{
            label: 'X Axis',
            backgroundColor: chartColors.red,
            borderColor: chartColors.red,
            data: (mag_data.length ? mag_data[mag_data.length - 1] : 0),
            fill: false,
        }, {
            label: 'Y Axis',
            fill: false,
            backgroundColor: chartColors.blue,
            borderColor: chartColors.blue,
            data: (mag_data.length ? mag_data[mag_data.length - 1] : 0),
        }, {
            label: 'Z Axis',
            fill: false,
            backgroundColor: chartColors.green,
            borderColor: chartColors.green,
            data: (mag_data.length ? mag_data[mag_data.length - 1] : 0),
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