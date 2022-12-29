import subprocess
import time
import os
import sys
from emailfinder.extractor import *

def get_email(com_name) -> list:
    glob_mails = []
    try:
        glob_mails += get_emails_from_baidu(com_name)
    except Exception:
        pass
    try:
        glob_mails += get_emails_from_bing(com_name)
    except Exception:
        pass
    try:
        glob_mails += get_emails_from_google(com_name)
    except Exception:
        pass

    return list(set(glob_mails))

def main(com_name):
    emails_list = []
    emails_len_list = []
    for _ in range(3):
        emails_list.append(get_email(com_name))
    for a_email_list in emails_list:
        emails_len_list.append(len(a_email_list))

    big = 0
    # Taking out the biggest list using length
    for one in range(len(emails_len_list)):
        if emails_len_list[big] <= emails_len_list[one]:
            big = one

    print(emails_len_list)
    print(f"No Of Dmains Founded are -> {len(emails_list[big])}")
    for a_mail in emails_list[big]:
        print(a_mail)

main('iitk.ac.in')