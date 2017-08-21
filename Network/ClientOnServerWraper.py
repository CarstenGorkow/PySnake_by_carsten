import queue
import xmltodict
import dicttoxml

import Network

class ClientOnServerWraper(object):
    """base client class that is used by player client and server client
    to send messages"""

    def __init__(self,client,addr):  
        self.client = client   
        self.addr = addr

        self.encd = 'utf-8'
        
        self.current_message_length = 0
        self.remaining_message_length = 0

        self.byte_array_remaining = b""

        # a Queue is used here to enable the separation of listen und reading the 
        # commands from the ClientServerWraper()
        self.task_queue = queue.Queue()
        

    def listen(self):
        recv_byte_array = self._recv_message()
        self._eval_message(recv_byte_array)


    def _recv_message(self):
        """ functions to recv a message from a socket in non blocking mode """
        #print("server listen to client msg",c)
        self.client.setblocking(0)
        try:
            byte_array = self.client.recv(1024)
            return byte_array
        except BlockingIOError:
            # exception is called if no data is in the socket buffer
            return b""            

       
    def _eval_message(self,byte_array):
        """ evaluate a byte string received from a socket """
        # this functions musst be simplet
        # -> mesage len cen be integraeted in xml dict
        # -> wait for more data on error or if not end sign
        if len(byte_array) == 0: 
            return 
        
        #print(byte_array)
        byte_array_split = byte_array.split(b"\0")
        recv_str_split = [b_str.decode("utf-8") for b_str in byte_array_split]
        #print(recv_str_split)
        for l in recv_str_split:
            if len(l) == 0:         # zero length message
                continue

            data_tree = Network.DataElementTree(l)
            if data_tree.root_tree == None :
                print("Wait for more data")
                print(l)
                self.byte_array_remaining = l
                return

            self.current_message_length = len(l)

            message_len = len(l)
            if message_len == self.current_message_length: # check if message is compleate
                # always executed
                # message ok
                # add message to server queue
                self._add_command_to_queue(data_tree)
            else:
                # message not compleate
                # get more data
                print("message not compleat")
                print(l)
                print("message len     : %i"%message_len)
                print("curretn msg len : %i"%self.current_message_length)
                

    def _new_msg_start(self,new_msg_length):

        #if self.remaining_message_length > 0:
        #    print("ERROR - last msg was not compleate - %i signs missing"%self.remaining_message_length)

        new_msg_length = int(new_msg_length)
        self.current_message_length = new_msg_length
        self.remaining_message_length = new_msg_length


    def _add_command_to_queue(self,command):
        """ add command """
        #print("command:",command.tree_dict)
        self.task_queue.put([self,command.tree_dict])


    def send_msg(self,msg):
        """ sending a msg to the server 
        - the len of the message pre send as xmg command"""

        #xml = dicttoxml.dicttoxml({"test":"entry"})
        #print(xml)

        if type(msg) is str:
            pass
        elif type(msg) is dict:
            msg = dicttoxml.dicttoxml(msg,custom_root='command')
        else:
            print("ERROR - ClientWraper - send_msg - send type unknown (%s)"%str(type(msg)))
            return

        # data string with len of message not send separatly
        #len_msg = len(msg)
        #len_msg_str = "<msg>%i</msg>\0"%len_msg
        #self._send_msg(len_msg_str)

        self._send_msg(msg+b"\0")


    def _send_msg(self,msg):
        if type(msg) is bytes:
            pass
        elif type(msg) is str:
            msg = msg.encode(self.encd)
        self.client.send(msg)



    def close(self):
        """ warper function for client closing """
        self.client.close()