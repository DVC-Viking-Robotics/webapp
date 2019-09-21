const btnRobotView = document.getElementById('btn-robot-view');
const btnRawDataView = document.getElementById('btn-raw-data');

const robotView = document.getElementById('robot-view');
const rawDataView = document.getElementById('raw-data-view');

function toggleView(viewType) {
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

const accelLineCtx = document.getElementById('accelerometer-line-chart').getContext('2d');
const accelLineChart = new Chart(accelLineCtx, configAccelLineChart);

const accelBarCtx = document.getElementById('accelerometer-bar-chart').getContext('2d');
const accelBarChart = new Chart(accelBarCtx, configAccelBarChart);

const gyroLineCtx = document.getElementById('gyroscope-line-chart').getContext('2d');
const gyroLineChart = new Chart(gyroLineCtx, configGyroLineChart);

const gyroBarCtx = document.getElementById('gyroscope-bar-chart').getContext('2d');
const gyroBarChart = new Chart(gyroBarCtx, configGyroBarChart);

const magLineCtx = document.getElementById('magnetometer-line-chart').getContext('2d');
const magLineChart = new Chart(magLineCtx, configMagLineChart);

const magBarCtx = document.getElementById('magnetometer-bar-chart').getContext('2d');
const magBarChart = new Chart(magBarCtx, configMagBarChart);