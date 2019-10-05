from .inputs.check_platform import ON_WINDOWS

import os
import subprocess

if not ON_WINDOWS:
    import pty          # docs @ https://docs.python.org/3/library/pty.html
    import termios      # used to set the window size (look up "TIOCSWINSZ" in https://linux.die.net/man/4/tty_ioctl)
    import fcntl        # I/O for file descriptors; used for setting terminal window size
    import struct       # struct library to pack data into bytearrays for setting terminal window size
    import select       # async I/O for file descriptors; used for retrieving terminal output
    import shlex        # used to shell-escape commands to prevent unsafe multi-commands (like "ls -l somefile; rm -rf ~")


OUTPUT_SLEEP_DURATION = 0.01        # Amount of time to sleep between calls to read the terminal output buffer
MAX_OUTPUT_READ_BYTES = 1024 * 20   # Maximum number of bytes to read from the terminal output buffer


# This class is for abstracting the virtual terminal capabilities. Note that this does not work for windows
class VTerminal:
    def __init__(self, socketio_inst):
        if ON_WINDOWS:
            raise Exception('Unable to create virtual terminal on Windows!')

        # We need a copy of the socketio app instance for asynchronously reading the terminal output
        self.socket_inst = socketio_inst
        self.fd = None          # The "file descriptor", essentially used as an I/O handle
        self.child_pid = None   # The child process ID; used to avoid starting multiple processes for the same task
        self.bg_thread = None   # The background thread that listens for terminal output.
        self.running_flag = False   # Flag indicating if the loop in the background thread is running or now
        self.output_listeners = []  # An array of output listeners, that allows the developer to perform various actions to the terminal output.

    # Check if the virtual terminal is initialized and ready to start doing I/O
    @property
    def initialized(self):
        return self.fd is not None

    # Check if the virtual terminal is doing I/O as of now
    @property
    def running(self):
        return self.bg_thread is not None

    # Create the
    def init_connect(self, term_cmd=["bash"], init_rows=50, init_cols=50):
        # print(self.child_pid, self.fd)
        if self.child_pid:
            # Already started child process, don't start another
            return  # Maybe needed to manage multiple client sessions across 1 server

        # Create child process attached to a pty we can read from and write to
        (self.child_pid, self.fd) = pty.fork()  # read docs for this https://docs.python.org/3/library/pty.html#pty.fork
        # print('what')
        # print(self.child_pid, self.fd)

        # now child_pid == 0, and fd == 'invalid'
        if self.child_pid == 0:
            # This is the child process fork. Anything printed here will show up in the pty, including the output of this subprocess
            # Docs for subprocess.run @ https://docs.python.org/3/library/subprocess.html#subprocess.run
            subprocess.run(term_cmd)  # `term_cmd` is a list of arguments that (in our case) get passed to
            # subprocess.Popen(); Docs @ https://docs.python.org/3/library/subprocess.html#subprocess.Popen
            # Docs say term_cmd can be a simple string which (in our case) would be a little easier as long as
            # We don't need to add more args to the `bash` program's starting call

            # NOTE: `multiprocessing` module has subprocess.run() functionality abstracted into their `Process` class
        else:
            # This is the parent process fork
            self.resize_terminal(init_rows, init_cols)

            # Now concatenate the term_cmd list into a " " delimited string for
            # outputting in the debugging print() cmds. See also previous comment after Popen() docs link
            term_cmd = " ".join(shlex.quote(c) for c in term_cmd)
            print("Terminal thread's Process ID is", self.child_pid)
            print(
                f"Starting background task with command `{term_cmd}` to continously read "
                "and forward pty output to client..."
            )

            if not self.running:
                self.running_flag = True
                # Docs for start_background_task @ https://flask-socketio.readthedocs.io/en/latest/#flask_socketio.SocketIO.start_background_task
                self.bg_thread = self.socket_inst.start_background_task(target=self._read_and_forward_pty_output)
                # Since this method returns a `threading.Thread` object that is already start()-ed, we can
                # simply capture the thread's instance for the multiprocessing module, but not until I (2bndy5) know how
                print("Output listener thread for terminal started")
            else:
                print("Output listener thread for terminal already started!")

    # Stop the background task and clean up after ourselves
    def cleanup(self):
        if self.initialized:
            if self.running:
                self.running_flag = False
            self.remove_all_listeners()

    # Helper function for resizing the virtual terminal
    def _set_winsize(self, row, col, xpix=0, ypix=0):
        # `ioctl` will only accept window size parameters as a bytearray
        winsize = struct.pack("HHHH", row, col, xpix, ypix)  # contruct the bytearray

        # NOTE: This method does *not* take keyword arguments!
        # Docs for this @ https://docs.python.org/3/library/fcntl.html#fcntl.ioctl
        fcntl.ioctl(self.fd, termios.TIOCSWINSZ, winsize)

    # Add a virtual terminal output listener for processing output text
    def register_output_listener(self, listener):
        self.output_listeners.append(listener)

    # Remove all virtual terminal output listeners
    def remove_all_listeners(self):
        self.output_listeners = []

    # Write some text input into the virtual terminal
    def write_input(self, str_input):
        if self.initialized:
            os.write(self.fd, str_input)

    # Resize the virtual terminal via the new numbers of rows and columns
    def resize_terminal(self, rows, cols):
        if self.initialized:
            self._set_winsize(self.fd, rows, cols)

    # A background task function that polls for any output from the virtual terminal every 10 ms
    # and calls the output listeners with the given output
    def _read_and_forward_pty_output(self):
        while self.running_flag:
            self.socket_inst.sleep(OUTPUT_SLEEP_DURATION)
            if self.initialized:
                # Docs: https://docs.python.org/3/library/select.html
                # The optional timeout argument specifies a time-out as a floating point number in seconds.
                # When the timeout argument is omitted the function blocks until at least one file descriptor is ready.
                # A time-out value of zero specifies a poll and never blocks.
                timeout_sec = 0
                (data_ready, _, _) = select.select([self.fd], [], [], timeout_sec)
                if data_ready:
                    # For invalid characters, print out the hex representation (as indicated by errors='backslashreplace')
                    output = os.read(self.fd, MAX_OUTPUT_READ_BYTES).decode(encoding='utf-8', errors='backslashreplace')
                    print('output', output)

                    # NOTE: Even though we are using the 'event'-based approach, note that these calls are still synchronous and blocking.
                    # Ideally we'd like them to be non-blocking, but it's not a huge priority for now.
                    # self.socket_inst.emit("terminal-output", {"output": output}, namespace="/pty")
                    for listener in self.output_listeners:
                        listener(output)
