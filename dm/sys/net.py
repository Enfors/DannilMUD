# net.py by Dannil
#
# This is the first piece of code that was written for DannilMUD.
# I started working on it at 19:30 on Feb 23rd, 2007.

import socket, select

TELNET_ECHO =   1

TELNET_WILL = 251
TELNET_WONT = 252
TELNET_DO   = 253
TELNET_DONT = 254
TELNET_IAC  = 255                       # Telnet "Interpret As Command"

DO_ECHO   = "%c%c%c" % (TELNET_IAC, TELNET_DO,   TELNET_ECHO)
DONT_ECHO = "%c%c%c" % (TELNET_IAC, TELNET_DONT, TELNET_ECHO)

###############################################
#
# Class Con
#
###############################################

class Con:
    """The Con class represents the server side socket in a client/server
    connection."""
    
    def __init__(self, con_man, sock):
        #print "  entering Con.__init__()"
        self.con_man   = con_man            # Our Connection Manager
        self.sock      = sock               # The socket itself
        self.fd        = sock.fileno()      # The socket's fd
        self.mask      = 0                  # The read / write mask
        self.read_buf  = ""                 # The buffer for incoming msgs
        self.write_buf = ""                 # The buffer for outgoing msgs
        self.login_state = "awaiting_login" # Set the state of the login,
                                            # so the input handler knows what
                                            # to do with it.
        self.num_failed_logins = 0          # Numer of failed logins

        (ip, port) = sock.getpeername()
        self.remote_ip   = ip               # Remote end IP
        self.remote_port = port             # Remote end port number

        self.user_char   = None             # The user char for this con

    #
    # Public functions
    #
    
    def write(self, data):
        """Call this function to ask the socket to queue data for
        sending."""
        #print "  Con.write() called."
        #data = data.replace("\n", "\r\n")
        #data = data.encode("ascii")
        #self.write_buf += str(data)
        self.write_buf += data.replace("\n", "\r\n")
        self._watch_write()


    def query_fd(self):
        """Returns the socket's corresponding file descriptor."""
        return self.fd

    
#    def set_login_state(self, new_state):
#        """Sets the current state of the connection.
#This information is used by the input handler, to determine what to do
#with input it receives."""
#        self.state = new_state


#    def query_login_state(self):
#        """Returns the login state the connection is in.
#This information is used by the input handler, to determine what to do
#with input that arrives during the login sequence."""
#        return self.state


    def end_after_write(self):
        """Instruct the connection to die once it's output buffer is empty."""
        if len(self.write_buf) == 0:
            self.end()
        else:
            self.end_after_write = True
    

    def end(self):
        """Ends a connection, closing the socket if need be."""
        self._dont_watch_anything()
        self.con_man.end_con(self)

        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()


    def set_user_char(self, user_char):
        self.user_char = user_char


    def query_user_char(self):
        return self.user_char


    #
    # Internal functions
    #

    def _read_now(self):
        """Called when incoming data is available."""
        try:
            bytes = self.sock.recv(4096)#.decode("UTF-8")
            
            if len(bytes) == 0: # If EOF (client disconnected)
                print("[net] Client disconnected.")
                self.end()
                return

            print("Data type: %s (%s)" % (type(bytes).__name__, bytes))

            while len(bytes) and bytes[0] == TELNET_IAC:
               bytes = self._handle_inc_iac(bytes[1:])

            if len(bytes):
                self.read_buf = bytes.decode("UTF-8")
            else:
                return None
        except:
            print("[net] Error on socket")
            self.end()
            raise

        text = self.read_buf
        self.read_buf = ""
        return text


    def _write_now(self):
        # If there is nothing to write, then return.
        if not len(self.write_buf):
            self.dont_watch_write()
            return

        # Send data.
        bytes_written = self.sock.send(self.write_buf.encode("ascii"))
        #bytes_written = self.sock.send(self.write_buf)

        # Remove the data that was actually sent from the buffer.
        self.write_buf = self.write_buf[bytes_written:]

        # If the entire buffer was sent:
        if not len(self.write_buf):
            if self.end_after_write == True: # Check if we should die now
                self.end()
                return
            self._dont_watch_write()


    def _watch_read(self):
        """Notify the connection manager that this socket now wants to
        read data."""
        #print "  now entering Con._watch_read()"
        self.mask |= select.POLLIN
        #print "  Calling con_man.register_for_poll()... "
        self.con_man.register_for_poll(self, self.mask)
        #print "  Done."
        #print "      fd %d now watching for read." % self.fd


    def _watch_write(self):
        """Notify the connection manager that this socket now wants to
        write data."""
        self.mask |= select.POLLOUT
        self.con_man.register_for_poll(self, self.mask)


    def _watch_both(self):
        """Notify the connection manager that this socket now wants to
        both read and write data."""
        self.mask = select.POLLIN | select.POLLOUT
        self.con_man.register_for_poll(self, self.mask)


    def _dont_watch_read(self):
        """Notify the connection manager that this socket does not want
        to read data."""
        self.mask &= ~select.POLLIN
        self.con_man.register_for_poll(self, self.mask)


    def _dont_watch_write(self):
        """Notify the connection manager that this socket does not want
        to write data."""
        self.mask &= ~select.POLLOUT
        self.con_man.register_for_poll(self, self.mask)


    def _dont_watch_anything(self):
        """Notify the connection manager that this socket wants to
        neither read nor write data."""
        self.mask = 0
        self.con_man.unregister_for_poll(self, self.mask)


    def _handle_inc_iac(self, bytes):
        """Called when an Telnet IAC character (255) arrives."""
        print("Telnet:")

        if bytes[0] == TELNET_DO:
            bytes = self._handle_inc_do(bytes[1:])
        elif bytes[0] == TELNET_WILL:
            bytes = self._handle_inc_will(bytes[1:])
        else:
            print("  Unhandled option: %d" % bytes[0])

        return bytes


    def _handle_inc_do(self, bytes):
        print("  DO")

        print("    Unhandled option: %d" % bytes[0])

        return bytes[1:]


    def _handle_inc_will(self, bytes):
        """Called when a Telnet WILL arrives."""
        print("  WILL")

        print("    Unhandled options: %d" % bytes[0])
        
        return bytes[1:]


#####################################################
#
# Class ConMan
#
#####################################################

class ConMan:
    """The ConMan class listens for new connections, and handles
    existing ones."""
    std_mask = select.POLLERR | select.POLLHUP | select.POLLNVAL

    def __init__(self, host = '', listen_port = 4851):
        self.host          = host
        self.listen_port   = listen_port
        
        # Set up the listening socket
        self.listen_sock = socket.socket(socket.AF_INET,
                                         socket.SOCK_STREAM)
        self.listen_sock.setsockopt(socket.SOL_SOCKET,
                                    socket.SO_REUSEADDR, 1)
        self.listen_sock.bind((self.host, self.listen_port))

        # Set up the poller
        self.poller = select.poll()

        self.poller.register(self.listen_sock.fileno(),
                             select.POLLIN | self.std_mask)

        # Set up socket and connection dictionaries
        self.socks  = { self.listen_sock.fileno(): self.listen_sock }
        self.cons   = {}

        self.listen_sock.listen(5)

    
    #
    # Public functions
    #

    def main_loop(self, input_handler):
        """Listens to the listen_socket, and handles connections.
        This function is obsolete. The main loop now resides in the
        driver."""
        #self.listen_sock.listen(5)
        #print("[net] Server accepting connections on port %d." % \
        #          self.listen_port)

        while 1:
            self.handle_one_event(input_handler)


    def handle_one_event(self, input_handler):
        result = self.poller.poll()
        for fd, event in result:
            if fd == self.listen_sock.fileno() and \
                    event == select.POLLIN:
                # We have an incomming connection request on the
                # listen socket. Time to accept it.
                    
                new_sock, addr = self._fd2socket(fd).accept()
                (ip, port) = new_sock.getpeername()
                print("[net] Accepted incoming connection on " \
                          "fd %d from %s:%d." %
                      (new_sock.fileno(), ip, port))
                self._new_con(new_sock, input_handler)
            elif event & select.POLLIN:
                self._read_event(fd)
            elif event & select.POLLOUT:
                self._write_event(fd)
            else:
                print("Event: %d" % event)
                self._error_event(fd)


    def broadcast(self, msg):
        for con in self.cons.values():
            con.write(msg)


    def register_for_poll(self, con, mask):
        #print "  now entering register_for_poll()"
        self.poller.register(con.query_fd(), mask | self.std_mask)


    def unregister_for_poll(self, con, mask):
        self.poller.unregister(con.query_fd())
    
            
    def end_con(self, con):
        print("[net] Closing connection on fd %d from %s:%d." % \
            (con.sock.fileno(), con.remote_ip, con.remote_port))
        if con.user_char:
            print("[net] %s logged out from %s:%d." % \
                      (con.user_char.query_cap_name(),
                       con.remote_ip, con.remote_port))
        del self.socks[con.query_fd()]
        del self.cons[con.query_fd()]

        # Tell the user char that the connection has been closed.
        if con.user_char:
            con.user_char.con_closed()

    
    #
    # Internal functions
    #

    def _fd2socket(self, fd):
        """Return the socket corresponding to a given file descriptor."""
        return self.socks[fd]


    def _new_con(self, sock, input_handler):
        """Handle a new incoming connection."""
        new_con = Con(self, sock)

        new_con.input_handler          = input_handler
        new_con._watch_read()
        self.socks[new_con.query_fd()] = sock
        self.cons[sock.fileno()]       = new_con

        new_con.write("Welcome to DannilMUD!\n\n")
        new_con.write("Login: ")


    def _read_event(self, fd):
        """Called when data is ready to be read on a socket."""
        con = self.cons[fd]
        text = con._read_now()

        # Text could be None, if it was just IAC commands
        if text:
            con.input_handler(*(con, text))


    def _write_event(self, fd):
        """Called when it is possible to write on a socket."""
        con = self.cons[fd]
        con._write_now()
        

    def _error_event(self, fd):
        """Called when an error has occurred on a socket."""
        con = self.cons[fd]
        print("[net] Error on fd %d from %s:%d." % 
              (fd, con.remote_ip, con.remote_port))
        con.end()
        
        

if __name__ == "__main__":
    #con_man = ConMan(listen_port = 5000)
    #con_man.main_loop()
    print("This file should not be started manually. Start main.py instead.")
