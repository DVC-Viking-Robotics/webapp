var stream = document.getElementById("camera-stream");

socket.on('error', (error) => {
    console.log('Socket error:', error)
});

socket.on('disconnect', function() {
    // stop requesting for the feed
    clearInterval(webcamRequestLock);
    console.log('socket disconnected', socket.connected);
});

// Used to receive the live feed from the raspberry pi
socket.on('webcam-response', function(img_data) {
    var dec = new TextDecoder("utf-8");
    stream.src = "data:image/jpeg;base64," + dec.decode(img_data);
});

// Webcam request loop
var webcamRequestLock = setInterval(function() {
    socket.emit('webcam');
}, 100);

