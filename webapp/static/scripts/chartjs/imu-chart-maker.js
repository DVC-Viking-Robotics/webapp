function createImuChartConfigs() {
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
                    ticks: {
                        min: -100,
                        max: 100,
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
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
                    ticks: {
                        min: -100,
                        max: 100,
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
                    }
                }]
            }
        }
    };

    return [ lineChartConfig, barChartConfig ];
}