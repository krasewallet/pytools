import poplib
import argparse
import re

def main(options):
    mailSer = re.match(r"[a-zA-Z\.]+@([\w\.]+)",options.email).group(1)
    mailbox=poplib.POP3(f"mail.{mailSer}",110)
    mailbox.user(options.email)
    mailbox.pass_(options.pwd)
    mails=mailbox.stat()[0]
    for i in range(mails):
        mailbox.dele(i+1)
    mailbox.quit()
if __name__=="__main__":
    parser = argparse.ArgumentParser(description="python image tools")
    parser.add_argument("email")
    parser.add_argument("pwd")
    args = parser.parse_args()
    main(args)