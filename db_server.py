import socket
import subprocess
import pymongo
import json
import os
import random

connection= pymongo.MongoClient("localhost",27017)
database= connection["ncc_dip2"]
collection= database["user_info"]

class TCPserver():
    def __init__(self):
        self.server_ip = 'localhost'
        self.server_port = 9994
        self.toSave = {}

    def main(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.server_ip, self.server_port))
        server.listen()
        print("Server listen on port:{} and ip {}".format(self.server_port, self.server_ip))
        try:
            while True:
                client, address = server.accept()
                print("Accepted Connection from - {} : {} ".format(address[0], address[1]))
                self.handle_client(client)
        except Exception as err:
            print(err)

    def handle_client(self, client_socket):
        data_list= []
        with client_socket as sock:
            from_client = sock.recv(1024)
            data_list = from_client.decode("utf-8").split(' ')
            # print("Received Data From Client:", data_list[0])
                   
               
            if data_list[0] == "gad":
                self.get_all_data(sock)

            elif data_list[0] == "login":
                self.login_check(sock,data_list)
            elif data_list[0] == "reg":
                self.regi_check(sock, data_list)   
            else:
                sms= bytes("Invalid",'utf-8')
                sock.send(sms)

    def get_all_data(self, sock):
        data: dict= {}
        id= 0
        for i in collection.find({},{"_id":0,"email":1,"password":1}):
            
            id= len(data)
            data_form:dict= {"email":i["email"],"password":i["password"]}
            data.update({id:data_form})
        print(data)
        str_data=json.dumps(data)
           
        send_data= bytes(str_data,'utf-8')
        sock.send(send_data)
        
           
    def login_check(self,sock,data_list):
        l_email= data_list[1]
        l_password= data_list[2]
        flag= -1
        index= 0
        sms= {}
        for i in collection.find({},{"_id":0,"email": 1, "password": 1,"info":1,"point":1}):
           if i["email"] == l_email and i["password"] == l_password:
              index= i
              flag= 1
              sms= {"email":index["email"],"info":index["info"],"point":index["point"]}
              sms= json.dumps(sms)

              break
           
        if flag == 1:
            str_data= bytes(sms, "utf-8")
            sock.send(str_data)

        else:
            str_data= bytes("User name and password not found!!",'utf-8')    
            sock.send(str_data)

    def regi_check(self, sock, data_list):
        user_id= random.randint(10,1000)
        r_email= data_list[1]
        r_password= data_list[2]
        r_phone= data_list[3]
        
        regi_data_form= {"_id":user_id,"email": r_email, "password": r_password, "phone": r_phone}

        ids= collection.insert_one(regi_data_form)
        
        send= "From server: Your registration is successful!!"
        bloo= bytes(send,'utf-8')
        sock.send(bloo)
        
if __name__ == '__main__':
    tcpserver = TCPserver()
    tcpserver.main()