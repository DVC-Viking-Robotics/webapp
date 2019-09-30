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
    for (let i = 0; i < arr.length; i++){
        data.push(arr[i][axis]);
    }
    return data;
}

// Sensor data request loop
const dataRequestLock = setInterval(function () {
    socket.emit('sensorDoF'); // used to request sensor data from server
}, 1000);

// Used to receive IMU's sensor(s) data from the raspberry pi
socket.on('sensorDoF-response', function (imuSenses) {
    console.log('imu sensors = ' + imuSenses);
    // imuSenses[0 - 2] = accel[x,y,z]
    // imuSenses[3 - 5] = gyro[x,y,z]
    // imuSenses[6 - 8] = mag[x,y,z]
    while (accel_data.length >= NUM_POINTS){
        // remove first element & rebase index accordingly
        accel_data.shift();
    }
    // add accelerometer data as array of [x, y, z]
    accel_data.push([imuSenses[0], imuSenses[1], imuSenses[2]])
    while (gyro_data.length >= NUM_POINTS){
        // remove first element & rebase index accordingly
        gyro_data.shift();
    }
    // add gyroscope data as array of [x, y, z]
    gyro_data.push([imuSenses[3], imuSenses[4], imuSenses[5]])
    while (mag_data.length >= NUM_POINTS){
        // remove first element & rebase index accordingly
        mag_data.shift();
    }
    // add magnetometer data as array of [x, y, z]
    mag_data.push([imuSenses[6], imuSenses[7], imuSenses[8]])
});