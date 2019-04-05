var video = document.getElementById("video");

socket.on('error', (error) => {
    console.log('Error:', error)
});

socket.on('disconnect', function() {
    // stop requesting for the feed
    clearInterval(webcamRequestLock);
    console.log('socket disconnected', socket.connected);
});

// Used to receive the live feed from the raspberry pi
socket.on('webcam-response', function(img_data) {
    var dec = new TextDecoder("utf-8");
    // console.log(img_data)
    video.src = "data:image/jpeg;base64," + dec.decode(img_data);
});

// Webcam request loop
var webcamRequestLock = setInterval(function() {
    socket.emit('webcam')
}, 250);

