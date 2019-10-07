// This is for toggling between the inertial data view and the robot view
function toggleView(viewType) {
    const btnRobotView = document.getElementById('btn-robot-view');
    const btnImuDataView = document.getElementById('btn-imu-data');

    const robotView = document.getElementById('robot-view');
    const rawDataView = document.getElementById('imu-data-view');

    switch (viewType) {
        case 'robot-view':
            btnRobotView.classList.add('is-info');
            btnImuDataView.classList.remove('is-link');

            rawDataView.style.display = 'none';
            robotView.style.display = 'initial';
            break;
        case 'imu-data':
            btnRobotView.classList.remove('is-info');
            btnImuDataView.classList.add('is-link');

            rawDataView.style.display = 'initial';
            robotView.style.display = 'none';
            break;
    }
}

// Initially show the sensor charts
toggleView('imu-data');


// Sensor data arrays
var accel_data = [];
var gyro_data = [];
var mag_data = [];


// Accelerometer chart initialization
const [ accelLineChartConfig, accelBarChartConfig ] = createImuChartConfigs("m/s^2");

const accelLineCtx = document.getElementById('accelerometer-line-chart').getContext('2d');
const accelLineChart = new Chart(accelLineCtx, accelLineChartConfig);

const accelBarCtx = document.getElementById('accelerometer-bar-chart').getContext('2d');
const accelBarChart = new Chart(accelBarCtx, accelBarChartConfig);

// Gyroscope chart initialization
const [ gyroLineChartConfig, gyroBarChartConfig ] = createImuChartConfigs("degrees/sec");

const gyroLineCtx = document.getElementById('gyroscope-line-chart').getContext('2d');
const gyroLineChart = new Chart(gyroLineCtx, gyroLineChartConfig);

const gyroBarCtx = document.getElementById('gyroscope-bar-chart').getContext('2d');
const gyroBarChart = new Chart(gyroBarCtx, gyroBarChartConfig);

// Magnetometer chart initialization
const [ magLineChartConfig, magBarChartConfig ] = createImuChartConfigs("gauss");

const magLineCtx = document.getElementById('magnetometer-line-chart').getContext('2d');
const magLineChart = new Chart(magLineCtx, magLineChartConfig);

const magBarCtx = document.getElementById('magnetometer-bar-chart').getContext('2d');
const magBarChart = new Chart(magBarCtx, magBarChartConfig);


// Sensor data request loop
const dataRequestLock = setInterval(function () {
    socket.emit('sensorDoF'); // used to request sensor data from server
}, 1000);

// Used to receive IMU's sensor(s) data from the raspberry pi
socket.on('sensorDoF-response', function(imuSenses) {
    // imuSenses[0] = accel[x,y,z]
    // imuSenses[1] = gyro[x,y,z]
    // imuSenses[2] = mag[x,y,z]

    // console.log('IMU sensors:');
    // console.log(imuSenses);


    // Handle the accelerometer data
    while (accel_data.length >= MAX_NUM_POINTS) {
        // Remove first element & rebase index accordingly
        accel_data.shift();
    }

    // Add accelerometer data as array of [x, y, z]
    accel_data.push(imuSenses[0]);

    // Update accel charts accordingly
    updateImuLineChart(accelLineChart, accel_data);
    updateImuBarChart(accelBarChart, accel_data);


    // Handle the gyroscope data
    while (gyro_data.length >= MAX_NUM_POINTS) {
        // Remove first element & rebase index accordingly
        gyro_data.shift();
    }

    // Add gyroscope data as array of [x, y, z]
    gyro_data.push(imuSenses[1]);

    // Update gyro charts accordingly
    updateImuLineChart(gyroLineChart, gyro_data);
    updateImuBarChart(gyroBarChart, gyro_data);


    // Handle the magnetometer data
    while (mag_data.length >= MAX_NUM_POINTS) {
        // Remove first element & rebase index accordingly
        mag_data.shift();
    }

    // Add magnetometer data as array of [x, y, z]
    mag_data.push(imuSenses[2]);

    // Update mag charts accordingly
    updateImuLineChart(magLineChart, mag_data);
    updateImuBarChart(magBarChart, mag_data);
});