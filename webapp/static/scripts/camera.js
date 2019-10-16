const stream = document.getElementById("camera-stream");

socket.emit('webcam-init');

socket.on('error', (error) => {
    console.log('Socket error:', error)
});

window.onbeforeunload = function() {
    clearInterval(webcamRequestLock);
    socket.emit('webcam-cleanup');
}

socket.on('disconnect', function() {
    // stop requesting for the feed
    clearInterval(webcamRequestLock);
    // console.log('socket disconnected', socket.connected);
});

// Used to receive the live feed from the raspberry pi
socket.on('webcam-response', function(img_data) {
    const dec = new TextDecoder("utf-8");
    stream.src = "data:image/jpeg;base64," + dec.decode(img_data);
});

// Webcam request loop
const webcamRequestLock = setInterval(function() {
    socket.emit('webcam');
}, 100);

