#!/usr/bin/env python3                      # Unix/Linux command

'''
v0.91 Beta

Welcome to BlueSonar! Your Samsung OS7000 series status checker.

In order to use this script install 'DB Browser for SQLite'. Open the Database in folder SmasungDB\SamsungDB.db
and update the tables.

In order to get Email report working fill in the following fields at the bottom, also if using google mail
make sure in google settings 'Allow less secure apps' is turned on to be able to sign in!

from_addr='example@gmail.com'               - input your email address
to_addr_list=['example@gmail.com']          - input recipients email address
cc_addr_list=['']                           - input CC email address (optional)
subject='Test Fault'                        - Email Subject
message=str(box_fault),                     - Do not modify
login='example@gmail.com'                   - input login name, with google this will be your emain address
pwEncoded='VGVzdCBwYXNzd29yZA=='            - Password needs to be encoded to base64, google search 'base64 encode'
smtpserver='smtp.gmail.com'                 - SMTP Server address
smtpport=587                                - SMTP PORT

Windows powershell encode:
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('Test password'))
'VGVzdCBwYXNzd29yZA=='
Windows powershell decode:
[Text.Encoding]::Utf8.GetString([Convert]::FromBase64String('VGVzdCBwYXNzd29yZA=='))
'Test password'

Linux encode:
echo 'Test password' | base64 -
'VGVzdCBwYXNzd29yZA=='
Linux decode:
echo 'VGVzdCBwYXNzd29yZA==' | base64 -d
'Test password'
'''

import socket
import time
from SamsungDB import os7100Class
from mods import EmailFaults
import sys
import argparse

# Start setting up argparse for user interaction
# Allow them to set time between scan
# Allow them to change database
# READ things_to_do.txt

ip_count = 0
try_count = 1
fail_count = 0
sleep = 300
password = []
fault_record = 'error_report.txt'
statement = "SELECT Name, IPaddress FROM SamsungPBX WHERE NOT MAC=''"


# Reads from SQLite, data parse & loops
def encapsulate():    
    sql = os7100Class.DB()
    sql.connection()
    data_pack = sql.read_from_db()
    total_count = sql.list_size(data_pack)
    global ip_count
    global try_count
    global fail_count
    global password
    sitename = []
    ip_address = []

    i = 0
    while i < total_count:
        for d in data_pack:
            sitename.append(d[0])
            ip_address.append(d[1])
            password.append(d[3])
            i += 1

    print(f"Starting Round: {try_count}\n")
    while True:
        for address in ip_address:
            if ip_count >= total_count:
                print(f"Fail count for this round: {fail_count}")
                print(f"Active Port count: {total_count - fail_count}")
                print(f"Total scanned: {total_count}")
                fail_count = 0
                print(f"End of Round: {try_count}\n")
                try_count += 1
                print(f"Restarting scan in {int(sleep / 60)} minutes")
                time.sleep(sleep)
                print(f"Round: {try_count}\n")
                ip_count = 0
            try:
                name = sitename[ip_count]
                pw = password[ip_count]
                ip_count += 1
                print(f"{ip_count}: Scanning {name} at IP Address {address}")
                connection(address, 5090, name, pw)
            except ValueError:
                break


# Makes connection, Tuples Error report & Emails Error report
def connection(addr, tp, name, pw):
    global fail_count
    socket.setdefaulttimeout(3.0)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:            
            s.connect((addr, tp))
        except socket.error as msg:
            print(f"    -- Not able to scan '{name}' at IP Address {addr}  --")
            #print(f"    -- [WinError {msg.args[0]}] {msg.args[1][:27]} --\n")
            msgAddon = f"    -- {name} --    Username: admin, Password: {pw}"
            fail_count += 1
            box_fault = addr, tp, msg, msgAddon
            with open(fault_record, 'a', encoding='utf-8') as faults:
                # sqlreader.update_db(box_fault)
                faults.write(str(box_fault) + '\n')
                faults.close()
                EmailFaults.sendemail(from_addr='someemail@domain.com', to_addr_list=['someemail@domain.com'],
                                      cc_addr_list=[''], subject='Test Fault', message=str(box_fault),
                                      login='someemail@domain.com', pwEncoded='VGVzdCBwYXNzd29yZA==',
                                      smtpServer='smtp.gmail.com', smtpPort=587)
        s.close()

if __name__ == "__main__":
    try:
        encapsulate()
    except KeyboardInterrupt:
        print("\nExiting...")


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument()
#     parser.add_argument()
#     parser.add_argument()
#     parser.add_argument()
#     parser.add_argument()
#     parser.add_argument()
#     parser.add_argument()

#     # Fill in args before sys.args need to know what to print
#     if len(sys.argv[2:]) ==0:
#         parser.print_help()
#         parser.exit()
#     args = parser.parse_args()
#     if args
