import base64
import socket
import os

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
        send_command(client_socket, "EHLO example.com")

            ## Gửi thông tin xác thực
            #send_command(client_socket, f"AUTH LOGIN")
            #send_command(client_socket, base64.b64encode(sender_email.encode()).decode())
            #send_command(client_socket, base64.b64encode(password.encode()).decode())

        # Nhập thông tin người nhận
        to_emails = input("Nhập địa chỉ email người nhận (các địa chỉ cách nhau bởi dấu phẩy): ").split(',')
        cc_emails = input("Nhập địa chỉ email CC (các địa chỉ cách nhau bởi dấu phẩy): ").split(',')
        bcc_emails = input("Nhập địa chỉ email BCC (các địa chỉ cách nhau bởi dấu phẩy): ").split(',')

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

        # Nhập nội dung email từ bàn phím
        print("Nhập nội dung email. Nhấn Enter hai lần để kết thúc.")
        body_lines = []
        while True:
            line = input()
            if not line:
                break
            body_lines.append(line)

        # Gửi nội dung email    
        body = "\r\n".join(body_lines)
        send_command(client_socket, body)

        # Gửi file đính kèm
        attach_file_path = input("Nhập đường dẫn đến file đính kèm: ")
        if os.path.exists(attach_file_path):
            with open(attach_file_path, 'rb') as attachment:
                attachment_data = attachment.read()
                send_command(client_socket, "Content-Type: application/octet-stream")
                send_command(client_socket, "Content-Transfer-Encoding: binary")
                send_command(client_socket, f"Content-Disposition: attachment; filename={os.path.basename(attach_file_path)}")
                send_command(client_socket, "")
                client_socket.sendall(attachment_data)

        # Kết thúc nội dung email
        send_command(client_socket, ".")

def send_command(socket, command):
    socket.sendall(f"{command}\r\n".encode())
    response = socket.recv(4096).decode()
    print(response)

send_email()
print("Email sent successfully.")