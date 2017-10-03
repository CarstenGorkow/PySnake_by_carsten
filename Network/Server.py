
import socket
import threading
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
import time
import queue

import os

from Network.ClientOnServerWraper import ClientOnServerWraper

class Server( QtCore.QObject ): # (object):
    """base server that manages the client connection, sending and receiving of messages"""

    def __init__(self):        
        QtCore.QObject.__init__(self)
        # valiables for general server
        self.client_list = []
        
        self.listen_for_client_connect = True
        self.listen_for_client_msg = True
        self.execute_queue = True
        
        self.timer_client_interval = 0.1 # s
        self.timer_client_connect_timeout = 2.0 # s
        self.timer_queue_execution = 0.1 # s
        
        self.task_queue = queue.Queue()
        self.port = 12349                # Reserve a port for your service.
        
        self.start_server()
        
    # ============= start server ===================

    def start_server(self):
        """ starts all background processes for listening"""
        self.listen_for_client_connect=True
        self.listen_for_client_msg=True
        self.execute_queue=True
        
        self.create_server()
        self.start_listen_for_client_connect()
        self.start_listener_to_client()
        self.start_queue_execution()


    def create_server(self):
        """ create socket and bind to network parameter"""
        try:
            self.server = socket.socket()         # Create a socket object
            self.host = socket.gethostname() # Get local machine name
            self.server.bind((self.host, self.port))        # Bind to the port
            print("=== create server at %s with port id %i ==="%(self.host,self.port))
        except:
            print(" -> server start failed")
            self.server.close()
            self.server = None


    def start_listen_for_client_connect(self):
        """ starts the server listen in background loop 
        - can be stoped with self.listen_for_client_connect=False"""
        if self.server != None:
            thread = threading.Thread(target=self._listen_for_client_connect_bkg, args=())
            thread.daemon = True                            # Daemonize thread
            thread.start()     


    def start_listener_to_client(self):
        """ starts listerner to client 
        - background process, to get the message emideatly"""
        if self.server != None:
            thread = threading.Thread(target=self._listen_to_client_bkg, args=())
            thread.daemon = True                            # Daemonize thread
            thread.start()     


    def start_queue_execution(self):
        """ starts the server listen in background loop 
        - can be stoped with self.listen_for_client_connect=False"""
        if self.server != None:
            thread = threading.Thread(target=self._execute_queue_commands_bkg, args=())
            thread.daemon = True                            # Daemonize thread
            thread.start()     

    # ============= listener ================

    def _listen_for_client_connect_bkg(self):
        """ server listening for client connections 
        -> inifinite loop until listering is stoped with self.listenfor_client_connect=False"""
        #print("server - start listen")
        self.server.listen(5)                 # Now wait for client connection.
        self.server.settimeout(self.timer_client_connect_timeout)
        self.listen_for_client_connect = True
        while self.listen_for_client_connect:
            try:
                c, addr = self.server.accept()     # Establish connection with client.
            except:
                continue
            self._attach_client(c,addr)
    
            
    def _listen_to_client_bkg(self) :
        """ receving messages from all clients in list 
        -> inifinite loop until listen is stoped with self.listen_for_client_msg=False"""
        while self.listen_for_client_msg:
            self._check_client_connection()
            self._listen_client()
            time.sleep(self.timer_client_interval)


    def _execute_queue_commands_bkg(self):
        """ execution of the commands stores in the queue 
        -> inifinite loop until listen is stoped with self.timer_queue_execution=False"""
        while self.execute_queue:
            while not self.task_queue.empty():
                [client,queue_command] = self.task_queue.get()
                self.command_eval(client,queue_command)
                self.task_queue.task_done()
            time.sleep(self.timer_queue_execution)


    # ============= listen helper  ====================

    def _attach_client(self,c,addr):
        """ attaches the new client to the client list """
        client = ClientOnServerWraper( c, addr,"s")
        self.client_list.append(client)
        #print('Got connection from', addr)
        return client


    def _check_client_connection(self):
        remove_list = []
        for c in self.client_list:
            if not c.is_connection_open():
                remove_list.append(c)

        for c in remove_list:
            self.client_list.remove(c)
        

    def _listen_client(self):
        """ listen to all clients on server 
        -> add the found commands to the server queue """
        for c in self.client_list:
            try:
                c.listen()
                while not c.task_queue.empty():
                    self.task_queue.put(c.task_queue.get())
                    c.task_queue.task_done()
            except ConnectionAbortedError as e:
                pass

    # =============

    def stop_server_listen(self):
        """ set all flags to stop the background processes for listening"""
        self.listen_for_client_connect=False
        self.listen_for_client_msg=False


    def close_clients(self):
        """ closing all clients that are registered at the server"""
        for c in self.client_list:
            c.close()
            self.client_list.remove(c)


    def command_eval(self,client,data_element_tree):
        """ functins for data evaluation for received data
       -> must be overwritten by child class """
        pass


    def send_clients(self,msg):
        """ listen to all clients on server 
        -> add the found commands to the server queue """
        for c in self.client_list:
            c.send_msg(msg)


    def send_client(self,client,msg):
        """ sends message only to one client """
        client.send_msg(msg)
    



