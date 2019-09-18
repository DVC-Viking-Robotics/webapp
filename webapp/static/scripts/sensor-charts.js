function toggleView(viewType) {
    var btnRobotView = document.getElementById('btn-robot-view');
    var btnRawDataView = document.getElementById('btn-raw-data');

    var robotView = document.getElementById('robot-view');
    var rawDataView = document.getElementById('raw-data-view');

    switch (viewType) {
        case 'robot-view':
            btnRobotView.classList.add('is-info');
            btnRawDataView.classList.remove('is-link');

            rawDataView.style.display = 'none';
            robotView.style.display = 'initial';
            break;
        case 'raw-data':
            btnRobotView.classList.remove('is-info');
            btnRawDataView.classList.add('is-link');

            rawDataView.style.display = 'initial';
            robotView.style.display = 'none';
            break;
    }
}

toggleView('raw-data');

var accelLineCtx = document.getElementById('accelerometer-line-chart').getContext('2d');
var accelLineChart = new Chart(accelLineCtx, configAccelLineChart);

var accelBarCtx = document.getElementById('accelerometer-bar-chart').getContext('2d');
var accelBarChart = new Chart(accelBarCtx, configAccelBarChart);

var gyroLineCtx = document.getElementById('gyroscope-line-chart').getContext('2d');
var gyroLineChart = new Chart(gyroLineCtx, configGyroLineChart);

var gyroBarCtx = document.getElementById('gyroscope-bar-chart').getContext('2d');
var gyroBarChart = new Chart(gyroBarCtx, configGyroBarChart);

var magLineCtx = document.getElementById('magnetometer-line-chart').getContext('2d');
var magLineChart = new Chart(magLineCtx, configMagLineChart);

var magBarCtx = document.getElementById('magnetometer-bar-chart').getContext('2d');
var magBarChart = new Chart(magBarCtx, configMagBarChart);