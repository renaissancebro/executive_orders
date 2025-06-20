from modules.check import check_last_policy
from modules.scraper import grab_meta_data
from modules.emailer import make_email, send_mail
from fake_entry import insert_dummy
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'alert_tripper')))

def main():
    
    if check_last_policy():  # True = new post
        meta = grab_meta_data()
        subject, body = make_email(meta)
        send_mail(subject, body)
    else:
        print("✅ No new executive order.")

if __name__ == "__main__":
    main()
