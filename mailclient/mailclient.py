import socket
import os
import base64
from datetime import date, datetime

def menu():
    print("Vui lòng chọn menu: ")
    print("1. Để gửi email")
    print("2. Thoát")
    
def send_email():
    # Thông tin tài khoản email
    sender_email = input("Nhập địa chỉ email của bạn: ")
    password = input("Nhập mật khẩu email của bạn: ")

    # Thông tin SMTP server (ví dụ: Gmail)
    smtp_server = "127.0.0.1"
    smtp_port = 2225

    # Kết nối tới SMTP server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((smtp_server, smtp_port))

        # Gửi lệnh EHLO để bắt đầu phiên kết nối
        send_command(client_socket, "EHLO [127.0.0.1]")

        # Nhập thông tin người nhận
        to_emails = input("TO: ").split(',')
        cc_emails = input("CC: ").split(',')
        bcc_emails = input("BCC: ").split(',')

        # Gửi lệnh MAIL FROM
        send_command(client_socket, f"MAIL FROM: <{sender_email}>")

        # Gửi lệnh RCPT TO cho người nhận
        for to_email in to_emails:
            send_command(client_socket, f"RCPT TO: <{to_email}>")

        # Gửi lệnh RCPT TO cho CC
        for cc_email in cc_emails:
            send_command(client_socket, f"RCPT TO: <{cc_email}>")

        # Gửi lệnh RCPT TO cho BCC
        for bcc_email in bcc_emails:
            send_command(client_socket, f"RCPT TO: <{bcc_email}>")

        # Gửi lệnh DATA để bắt đầu nhập nội dung email
        send_command(client_socket, "DATA") 

        #Nhập nội dung email từ bàn phím
        print("Content: ")
        
        content_lines = []
        while True:
            line = input()
            if not line: 
                break
            content_lines.append(line)
        body = "\r\n".join(content_lines)
        send_command(client_socket, body)
        
        name_attachments = input("Input link attachment: ").split(',')
        
        attachments = get_attachment(name_attachments)
           
        msg += f"\n\n{attachments}"
        client_socket.send(attachments)
        
        # Kết thúc nội dung email
        send_command(client_socket, ".")
SUPPORTED_FORMATS = {
    "txt": "text/plain",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "pdf": "application/pdf",
    "jpg": "image/jpeg",
    "png": "image/png",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "zip": "application/zip"
}

def get_attachment(filename):
    name = os.path.basename(filename)
    ext = os.path.splitext(name)[1].lower().strip(".")
    
    if ext not in SUPPORTED_FORMATS:
        return
        
    mime_type = SUPPORTED_FORMATS[ext]
    
    with open(filename, "rb") as f:
        data = f.read()
        
    b64 = base64.b64encode(data).decode("utf-8")
    
    part = f"Content-Type: {mime_type}; name=\"{name}\"\n"
    part += f"Content-Transfer-Encoding: base64\n" 
    part += f"Content-Disposition: attachment; filename=\"{name}\"\n\n{b64}"
    
    return part

def send_command(socket, command):
    socket.sendall(f"{command}\r\n".encode())
    response = socket.recv(4096).decode()
    print(response)
    
def main():
    while True:
        menu()
        choice = int(input("Nhập lựa chọn: "))
        if choice == 1:
            send_email()
            print("Gửi email thành công!")
        elif choice == 2:   
              print("Hẹn gặp lại!")
              exit()
            

if __name__ == '__main__':
    main()