
from PyQt5 import QtCore
import socket
import queue
import threading
import time

from Network.ClientOnServerWraper import ClientOnServerWraper


class Client( QtCore.QObject):
    """Base client class that manages the receving and sending of data"""

    signalCommand = QtCore.pyqtSignal(list)    
    signal_status_message = QtCore.pyqtSignal(str)

    def __init__(self,parent):
        QtCore.QObject.__init__(self)
        self.parent = parent

        self.listen_for_server_msg = True
        self.execute_queue = True

        self.timer_client_interval = 0.03 # 

        self.task_queue = queue.Queue()
        
        self.client_wrap = None
        self.port = 12349                # Reserve a port for your service.
        self.create_client()

    # ================ properties ===================

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self,val):
        #print(self._host,val)
        if self._host != val:
            self._host = val
            self._set_host()

    # ================ methodes ===================

    def create_client(self):
        """create socket for client
        - set host and port for connection"""
        self.client = socket.socket()         # Create a socket object
        self._host = socket.gethostbyname(socket.gethostname()) # Get local machine name


    def connect_client(self):
        """connect the client to the given server """
        try:
            print("connect to server %s at port %s"%(str(self.host),str(self.port)))
            self.client.connect((self.host, self.port))
            self.client_wrap = ClientOnServerWraper(self.client,[],"c")
            self.start_listener_to_server()
            #print(" -> connected to server")
            self.signal_status_message.emit(" -> connected to server")
            #self.start_queue_execution()
        except OSError as e:
            #print( e.errno)
            #print( e.filename)
            print( e.strerror)
            #print(" -> connection failed - return ")
            self.signal_status_message.emit(e.strerror)

    def close_client(self):
        self.client.close()
        self.client = socket.socket()         # Create a socket object


    def _set_host(self):
        self.close_client()
        self.connect_client()
        #print(self.host)


    def is_connected(self):
        """ returns True is the client is connected to an endpoint, otherweise False"""
        is_connected = False
        if self.client != None:
            try:
                peername = self.client.getpeername()
                is_connected = True
            except:
                pass

        return is_connected

    

    def start_listener_to_server(self):
        """ starts listern to get data from server 
        - background process, to get the message emideatly"""
        thread = threading.Thread(target=self.listen_to_server_bkg, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()     


    def listen_to_server_bkg(self) :
        """ receving messages from the server
        -> inifinite loop until listen is stoped with self.listen_for_server_msg=False"""
        while self.listen_for_server_msg:
            self.client_wrap.listen()
            while not self.client_wrap.task_queue.empty():
                self.put_task_to_queue(self.client_wrap.task_queue.get())
                self.client_wrap.task_queue.task_done()
            time.sleep(self.timer_client_interval)


    def put_task_to_queue(self,task):
        """ orgenises the execution and redirection of tasks in the background process 
        -> can be overwritten by derived class for redirection"""        
        #self.task_queue.put(task)
        self.signalCommand.emit(task)

