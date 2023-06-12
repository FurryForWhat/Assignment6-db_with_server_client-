import socket
import json
import pymongo

connection =pymongo.MongoClient('localhost',27017)
database= connection["ncc_dip2"]
collection= database["user_info"]
######### global variable #################
UNfound_PassAndMail= -1   #regi flag



class TCPclient():
    def __init__(self, sms):
        self.target_ip = 'localhost'
        self.target_port = 9994
       
        self.input_checking(sms)

    def run_client(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_ip, self.target_port))

        # client.send(self.client_sms)

        # received_from_server = client.recv(4096)

        # recv_sms = received_from_server.decode("utf-8")

       
        # print("$",recv_sms)

        # client.close()
        return client #to send and receive data

    def input_checking(self, sms):
        if sms == "gad":
            self.get_all_data(sms)
        elif sms == "login":
            self.login(sms)
        elif sms == "reg":
            self.register(sms)

        else:
            print("invalid option:")
    
    def get_all_data(self, sms):
       client = self.run_client()
       by_client= bytes(sms+'','utf-8')
       client.send(by_client)
       from_server= client.recv(4096)
    #    result= from_server.decode("utf-8")
    #    print(result)
       dict_data: dict= json.loads(from_server.decode("utf-8")) # string to dict
       print(type(dict_data))
       print(dict_data)
       client.close()

    def login(self,info):
        try:
            print("This is login!!")
            email= input("Enter your email to login:")
            password = input("Enter your password to login:")
            
            client= self.run_client()
            sms= info+' '+ email + ' '+ password
            sms= bytes(sms, "utf-8")
            client.send(sms)
            received_from_server= client.recv(4096)
            user_info= json.loads(received_from_server.decode("utf-8"))
            print("Email:",user_info["email"])
            print("Info:",user_info["info"])
            print("Point:",user_info["point"])

            
            client.close()
       
        except Exception as err:
            print(err)    


    def register(self, info):
        bank= []
        to_sent: dict= {}
        try:
            print("This is registeration!!!")
            for i in collection.find({},{"_id": 0,"email": 1}):
                bank.append(i["email"])
            print(bank)    

            r_email:str=input("Enter your email: ")   
            
            # for i in collection.find({},{"_id": 0,"email": 1,"password": 1}):
            #     index= len(bank)
            #     bank_second= {"email": i["email"],"password": i["password"]}
            #     bank.update({index:bank_second})
            # print(bank) 
            if r_email in bank:
              print("*********    Your email is used  ********")
              print("*********    Try with a new one!!!  ********")              
              return self.register(info)
            

            r_password= input("Enter your password: ")
            phone: int= int(input("Enter phone number: "))

            client= self.run_client()
            sms= info+' '+ r_email + ' '+ r_password+' '+ str(phone)
            sms= bytes(sms, "utf-8")
            client.send(sms)
            print("*********    sending success     ************")
            
            received_from_server= client.recv(4096)
            recv_data=received_from_server.decode("utf-8")
            print(recv_data)
            client.close()    

            # print(type(bank))    
            
        except Exception as err:
            print("There is some error")
            print(err)


if __name__ == "__main__":
    while True:
        sms = input("Enter some data to send:") 
        tcp_client = TCPclient(sms)
        