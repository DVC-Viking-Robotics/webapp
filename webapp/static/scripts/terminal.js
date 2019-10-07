Terminal.applyAddon(fit);
Terminal.applyAddon(webLinks);

const term = new Terminal({
    cursorBlink: true,
    macOptionIsMeta: true,
    scrollback: 1000,
});

term.open(document.getElementById('terminal'));

term.fit();
term.resize(15, 35);
console.log(`size: ${term.cols} columns, ${term.rows} rows`);
term.fit();

function resizeTerm(rows, cols) {
    termSocket.emit("terminal-resize", { "cols": cols, "rows": rows });
}

function sendTermInput(input) {
    termSocket.emit("terminal-input", { "input": input });
}

function displayTermOutput(output) {
    term.write(output);
}

term.on('key', (key, ev) => {
    // console.log("pressed key", key);
    // console.log("event", ev);
    sendTermInput(key);
});

const termSocket = io.connect('/pty', { transports: ['websocket'] });

const status = document.getElementById("status");

termSocket.on("terminal-output", function (data) {
    // console.log("new output", data);
    displayTermOutput(data.output);
});

termSocket.on("connect", () => {
    fitToscreen();
    status.innerHTML = '<span class="has-text-weight-bold has-text-success">connected!</span>';
});

termSocket.on("disconnect", () => {
    status.innerHTML = '<span class="has-text-weight-bold has-text-danger">disconnected!</span>';
});

function fitToscreen() {
    term.fit();
    resizeTerm(term.rows, term.cols);
}

function debounce(func, wait_ms) {
    let timeout;
    return function (...args) {
        const context = this;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), wait_ms);
    }
}

const wait_ms = 50;
window.onresize = debounce(fitToscreen, wait_ms);