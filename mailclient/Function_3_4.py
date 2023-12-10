import os
import shutil
import configparser
import string
import re
import glob
import email
from email import policy
from email.parser import BytesParser
from EmailMethod import *



# loc email
def FilterEmail(Email_File):
    file_path = find_file(Email_File)
    msg = read_eml_file(file_path)
    info_email = get_email_info(msg)
    content_email = get_content_from_eml(file_path)
    List_text = list()
    List_text.extend(info_email)
    List_text.extend(content_email)
    for Text in List_text:
        folder_name = FilterText(Text)
        moveFile(Email_File, folder_name)


# Thong tin cua email can doc: from, subject, content. 
def Read_Email(Email):
    Email_path = find_file(Email)
    msg = read_eml_file(Email_path)

    info = get_email_info(msg)
    print(f"{info[0]}, {info[1]}, {info[2]}")
    print(f"Content: {get_content_from_eml(Email_path)} \r\n")
    
    # lay danh sach file dinh kem
    file_attach = get_attachments(msg)
    if len(file_attach) == 0:
        print("Không có file đính kèm. \r\n")
    else:
        print("Có file đính kèm.\r\n")
        isDown = int(input("Nhập 1 để tải về (không tải về vui lòng nhập 0): "))
        if isDown == 1:
            DownLoad_folder = find_folder("File_attachment")
            try:
                if os.path.exists(Email_path) and os.path.exists(DownLoad_folder):
                    download_attachments(Email_path, DownLoad_folder)    
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        else:
            print("kết thúc đọc email.\r\n")



def ViewEmail():
    print("Danh sách folder: ")
    List_foder = PrintList("mailbox")
    choice_folder = int(input("Nhập folder (nhập theo số): "))
    if List_foder[choice_folder] == "Thoát.":
        return
    print(f"Danh sách email trong {List_foder[choice_folder]}: ")
    while True:
        List_email = PrintList(List_foder[choice_folder])
        choice_email = int(input("Nhập email bạn muốn xem (nhập theo số): "))
        if(List_email[choice_email] == "Thoát."):
            return
        Read_Email(List_email[choice_email])


def MoveEmail():
    print("Danh sách folder: ")
    List_foder = PrintList("mailbox")
    choice_folder = int(input("Nhập folder chứa email muốn chuyển (nhập theo số): "))
    if List_foder[choice_folder] == "Thoát.":
        return
    print(f"Danh sách email trong {List_foder[choice_folder]}: ")
    List_email = PrintList(List_foder[choice_folder])
    choice_email = int(input("Nhập email/file bạn muốn chuyển (nhập theo số): "))
    if(List_email[choice_email] == "Thoát."):
        return
    for key, value in List_foder.items():
        print(f"{key}. {value}.\r\n")
    choice_ToFoder = int(input("Nhập folder muốn chuyển tới (nhập theo số): "))
    if List_foder[choice_folder] == "Thoát.":
        return  
    moveFile(List_email[choice_email], List_foder[choice_ToFoder])