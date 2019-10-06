// This will create an easy-to-use line and bar chart configuration for the accel, gyro,
// and mag sensors. It will return in the form of [lineChartConfig, barChartConfig]
function createImuChartConfigs(/* minRange = -100, maxRange = 100, */ yAxisLabel = 'Value') {
    const lineChartConfig = {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'X Axis',
                backgroundColor: chartColors.red,
                borderColor: chartColors.red,
                data: [],
                fill: false,
            }, {
                label: 'Y Axis',
                fill: false,
                backgroundColor: chartColors.blue,
                borderColor: chartColors.blue,
                data: [],
            }, {
                label: 'Z Axis',
                fill: false,
                backgroundColor: chartColors.green,
                borderColor: chartColors.green,
                data: [],
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
                    // ticks: {
                    //     min: minRange,
                    //     max: maxRange,
                    // },
                    scaleLabel: {
                        display: true,
                        labelString: yAxisLabel
                    }
                }]
            }
        }
    };

    const barChartConfig = {
        type: 'bar',
        data: {
            datasets: [{
                label: 'X Axis',
                backgroundColor: chartColors.red,
                borderColor: chartColors.red,
                data: [],
                fill: false,
            }, {
                label: 'Y Axis',
                fill: false,
                backgroundColor: chartColors.blue,
                borderColor: chartColors.blue,
                data: [],
            }, {
                label: 'Z Axis',
                fill: false,
                backgroundColor: chartColors.green,
                borderColor: chartColors.green,
                data: [],
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
                    // ticks: {
                    //     min: minRange,
                    //     max: maxRange,
                    // },
                    scaleLabel: {
                        display: true,
                        labelString: yAxisLabel
                    }
                }]
            }
        }
    };

    return [ lineChartConfig, barChartConfig ];
}