function toggleView(viewType) {
    const btnRobotView = document.getElementById('btn-robot-view');
    const btnRawDataView = document.getElementById('btn-imu-data');

    const robotView = document.getElementById('robot-view');
    const rawDataView = document.getElementById('imu-data-view');

    switch (viewType) {
        case 'robot-view':
            btnRobotView.classList.add('is-info');
            btnRawDataView.classList.remove('is-link');

            rawDataView.style.display = 'none';
            robotView.style.display = 'initial';
            break;
        case 'imu-data':
            btnRobotView.classList.remove('is-info');
            btnRawDataView.classList.add('is-link');

            rawDataView.style.display = 'initial';
            robotView.style.display = 'none';
            break;
    }
}

toggleView('imu-data');

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

// Sensor data request loop
const dataRequestLock = setInterval(function () {
    socket.emit('sensorDoF'); // used to request sensor data from server
}, 1000);

// Used to receive IMU's sensor(s) data from the raspberry pi
socket.on('sensorDoF-response', function (imuSenses) {
    console.log('IMU sensors:');
    console.log(imuSenses);
    // imuSenses[0] = accel[x,y,z]
    // imuSenses[1] = gyro[x,y,z]
    // imuSenses[2] = mag[x,y,z]

    while (accel_data.length >= MAX_NUM_POINTS) {
        // remove first element & rebase index accordingly
        accel_data.shift();
    }

    // add accelerometer data as array of [x, y, z]
    accel_data.push(imuSenses[0]);
    updateLineChart(accelLineChart, accel_data);
    updateBarChart(accelBarChart, accel_data);

    while (gyro_data.length >= MAX_NUM_POINTS) {
        // remove first element & rebase index accordingly
        gyro_data.shift();
    }

    // add gyroscope data as array of [x, y, z]
    gyro_data.push(imuSenses[1]);
    updateLineChart(gyroLineChart, gyro_data);
    updateBarChart(gyroBarChart, gyro_data);

    while (mag_data.length >= MAX_NUM_POINTS) {
        // remove first element & rebase index accordingly
        mag_data.shift();
    }

    // add magnetometer data as array of [x, y, z]
    mag_data.push(imuSenses[2]);
    updateLineChart(magLineChart, mag_data);
    updateBarChart(magBarChart, mag_data);
});