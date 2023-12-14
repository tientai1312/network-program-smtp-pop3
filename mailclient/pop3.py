import email
import socket
import configparser
from email import message_from_string
import base64
from email.header import decode_header
import glob
import os
import quopri
from email.parser import BytesParser
from email.policy import default
from email import policy
from EmailMethod import download_attachments
import json
from EmailMethod import *
from Function_3_4 import *



def save_email_eml(email_data, save_path, uidl):
    # Phân giải email từ dạng bytes
    email_message = BytesParser(policy=policy.default).parsebytes(email_data)

    # Tạo tên file dựa trên UIDL của email
    email_filename = f"{uidl.split('.')[0]}.eml"
    email_path = os.path.join(save_path, email_filename)

    # Lưu email vào file .msg
    with open(email_path, "wb") as email_file:
        email_file.write(email_data)
    
    FilterEmail(email_filename)
 
def save_status_to_json(status, save_path):
    # Lưu trạng thái vào file JSON
    json_path = os.path.join(save_path, "status.json")
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(status, json_file, indent=2, ensure_ascii=False)

 
def save_status_to_json(status, save_path):
    # Lưu trạng thái vào file JSON
    json_path = os.path.join(save_path, "status.json")
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(status, json_file, indent=2, ensure_ascii=False)
        
def download_msg(user_name, user_pass, pop3_server, pop3_port, save_msg_path):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client_socket:
        client_socket.connect((pop3_server,pop3_port))
        response = client_socket.recv(1024).decode("utf-8")
        print(response)
        
        # GỬI LỆNH USER
        client_socket.send(f"USER {user_name}\r\n".encode("utf-8"))
        response = client_socket.recv(1024).decode("utf-8")
        print(response)

        # Gửi lệnh PASS
        client_socket.send(f"PASS {user_pass}\r\n".encode("utf-8"))
        response = client_socket.recv(1024).decode("utf-8")
        print(response)
        
        # Gửi lệnh STAT để lấy thông tin về số lượng email
        client_socket.send("STAT\r\n".encode("utf-8"))
        response = client_socket.recv(1024).decode("utf-8")
        print(response)
           # Lấy thông tin về số lượng email và kích thước của chúng
        num_messages = int(response.split()[1])
        print(response)
        print(f"Total emails: {num_messages}")
        print("LIST")
        # Gửi lệnh LIST để lấy danh sách email
        client_socket.send("LIST\r\n".encode("utf-8"))
        response = client_socket.recv(4096).decode("utf-8")
        print(response)
        
     
    
        print("UIDL")
        # Lấy danh sách UIDL (Unique IDs) của tất cả email
        uidl_command = "UIDL\r\n"
        client_socket.sendall(uidl_command.encode())
        response = client_socket.recv(1024).decode()
        print(response)
        uidl_list = response.split("\r\n")[1:-2]
        uidl_list = [uidl.split()[1] for uidl in uidl_list ]


       
        # Lấy thông tin của từng email và tải nội dung có attachment
        for i in range(num_messages):
            # Gửi lệnh RETR để lấy nội dung email
            client_socket.send(f"RETR {i + 1}\r\n".encode("utf-8"))
            email_data = b''
            while True:
                data = client_socket.recv(4096)
                email_data += data
                if data.decode().endswith("\r\n.\r\n"):
                    break
           
            email_data = '\n'.join(email_data.decode().splitlines()[1:-1]).encode('utf-8')
            # Hiển thị thông tin về email
            email_data = email_data.decode("utf-8")
            # Xử lý nội dung email
            email_message = BytesParser(policy=policy.default).parsebytes(email_data.encode("utf-8"))
            
           
            save_email_eml(email_data.encode("utf-8"), save_msg_path,  uidl_list[i])

        
       # Gửi lệnh QUIT để đóng kết nối
        client_socket.send("QUIT\r\n".encode("utf-8"))
        response = client_socket.recv(1024).decode("utf-8")
        print(response)
            
# if __name__ == "__main__":
#     config_obj = configparser.ConfigParser()
#     config_file = "C:/Users/DEEZENI/source/repos/network-program/mailclient/mailclient/Config.ini"
#     config_obj.read(config_file, encoding = "utf-8")

#     user_config = config_obj['USER']
#     user_name = user_config['Email'].strip('"\'')
#     user_pass = user_config['Password'].strip('"\'')
#     pop3_server = user_config['Mailserver'].strip('"\'')
#     pop3_port = int(user_config['POP3'].strip('"\''))
#     save_msg_path = f"C:/Users/DEEZENI/source/repos/network-program/mailclient/mailclient/msgdownload/"
#     os.makedirs(save_msg_path, exist_ok=True)
#     download_msg(user_name, user_pass, pop3_server, pop3_port, save_msg_path)