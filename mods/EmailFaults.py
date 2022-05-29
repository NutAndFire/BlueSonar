""" v1.0 Working """

import smtplib
import base64


def sendemail(from_addr, to_addr_list, cc_addr_list, subject, message, login, pwEncoded,
            smtpServer='smtp.gmail.com', smtpPort=587):

    # Email structure
    header = f'From: {from_addr}\n'
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += f'Subject: {subject}\n\n'
    message = header + message

    # Server connection
    server = smtplib.SMTP(smtpServer, smtpPort)  # use both smtp server and port
    server.starttls()
    password = base64.b64decode(pwEncoded)
    password = str(password).strip("b'")
    server.login(login, password)
    server.sendmail(from_addr, to_addr_list, message)
    server.quit()
