from modules.check import check_last_policy
from modules.scraper import grab_meta_data
from modules.emailer import make_email, send_mail

def main():
    if check_last_policy():  # True = new post
        meta = grab_meta_data()
        subject, body = make_email(meta)
        send_mail(subject, body)
    else:
        print("✅ No new executive order.")

if __name__ == "__main__":
    main()
