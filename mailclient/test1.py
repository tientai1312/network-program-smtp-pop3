import socket
import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email(sender_email, receiver_email, subject, body, attachment_paths, cc_list, bcc_list, smtp_server, smtp_port, username, password, max_attachment_size_MB):
    # Tạo đối tượng MIMEMultipart
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Thêm nội dung email
    message.attach(MIMEText(body, 'plain'))

    # Thêm danh sách CC vào email nếu có
    if cc_list:
        cc = ', '.join(cc_list)
        message['CC'] = cc

    # Thêm danh sách BCC vào email nếu có
    if bcc_list:
        bcc = ', '.join(bcc_list)
        message['BCC'] = bcc

    # Thêm các file đính kèm
    if attachment_paths:
        for attachment_path in attachment_paths:
            attachment_size_MB = os.path.getsize(attachment_path) / (1024 * 1024)  # Kích thước file đính kèm tính bằng MB
            if attachment_size_MB > max_attachment_size_MB:
                print(f"Skipping attachment {attachment_path} as it exceeds the maximum allowed size.")
                continue

            with open(attachment_path, 'rb') as attachment_file:
                attachment = MIMEApplication(attachment_file.read(), _subtype="auto")
                attachment.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
                message.attach(attachment)

    # Xây dựng nội dung MIME
    mime_content = message.as_string()

    # Kết nối đến server SMTP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((smtp_server, smtp_port))

        # Nhận và in lời chào từ server
        response = client_socket.recv(1024)
        print(response.decode())

        # Gửi lệnh EHLO để bắt đầu phiên làm việc
        client_socket.sendall('EHLO [127.0.0.1]\r\n'.encode())
        response = client_socket.recv(1024)
        print(response.decode())

        # Bắt đầu quá trình xác thực
        client_socket.sendall('AUTH LOGIN\r\n'.encode())
        response = client_socket.recv(1024)
        print(response.decode())

        # Gửi tên người dùng đã mã hóa base64
        client_socket.sendall(base64.b64encode(username.encode()) + b'\r\n')
        response = client_socket.recv(1024)
        print(response.decode())

        # Gửi mật khẩu đã mã hóa base64
        client_socket.sendall(base64.b64encode(password.encode()) + b'\r\n')
        response = client_socket.recv(1024)
        print(response.decode())

        # Gửi lệnh MAIL FROM
        client_socket.sendall(f'MAIL FROM: <{sender_email}>\r\n'.encode())
        response = client_socket.recv(1024)
        print(response.decode())

        # Gửi lệnh RCPT TO:
        if receiver_email:
            client_socket.sendall(f'RCPT TO: <{receiver_email}>\r\n'.encode())
            response = client_socket.recv(1024)
            print(response.decode())
        
        if cc_list:
            for ccs in cc_list:
                client_socket.sendall(f'RCPT TO: <{ccs}>\r\n'.encode())
                response = client_socket.recv(1024)
                print(response.decode())
        
        if bcc_list:
            for bccs in cc_list:
                 client_socket.sendall(f'RCPT TO: <{bccs}>\r\n'.encode())
                 response = client_socket.recv(1024)
                 print(response.decode())

        # Gửi lệnh DATA để bắt đầu truyền nội dung email
        client_socket.sendall('DATA\r\n'.encode())
        response = client_socket.recv(1024)
        print(response.decode())

        # Gửi nội dung email
        client_socket.sendall(mime_content.encode())
        client_socket.sendall('\r\n.\r\n'.encode())
        response = client_socket.recv(1024)
        print(response.decode())

        # Đóng kết nối
        client_socket.sendall('QUIT\r\n'.encode())
        response = client_socket.recv(1024)
        print(response.decode())

    print(f'Email sent successfully!')

# Sử dụng hàm
sender_email = 'dlmmt1512@gmail.com'
receiver_email = 'tle255837@gmail.com'
subject = 'Mot ngay dep troi'
body = '1234556789'

attachment_paths = ['C:/Users/DEEZENI/source/repos/testMail/testMail/3.jpg', 'C:/Users/DEEZENI/source/repos/testMail/testMail/2.jpg']

cc_list = ['tle255837@gmail.com', '1@gmail.com','dlmmt1512@gmail.com']
bcc_list = ['tle255837@gmail.com', '1@gmail.com','dlmmt1512@gmail.com']

send_email(
    sender_email, receiver_email, subject, body,
    attachment_paths, cc_list, bcc_list,
    smtp_server='127.0.0.1', smtp_port=2225,
    username='dlmmt1512@gmail.com', password='123asdcz', max_attachment_size_MB=3
)
