from modules.scraper import grab_meta_data
from modules.emailer import make_email, send_mail
from modules.check import check_last_policy
from modules.alert_tripper import trigger_alert, clear_alert  # ✅ Import here

def main():
    tag = "testrun"

    # 🔹 Trigger dummy policy before running the checker
    trigger_alert(tag)

    try:
        if check_last_policy():  # True = new post
            meta = grab_meta_data()
            subject, body = make_email(meta)
            send_mail(subject, body)
        else:
            print("✅ No new executive order.")
    finally:
        # 🔹 Always clean up — even if error occurs
        clear_alert(tag)

if __name__ == "__main__":
    main()

