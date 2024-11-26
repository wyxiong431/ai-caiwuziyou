from datetime import datetime, timedelta


def get_end_date():
    now = datetime.now()

    if now.hour > 15 or (now.hour == 15 and now.minute >= 30):
        target_date = now.date()
    else:
        target_date = (now - timedelta(days=1)).date()
    return target_date


def is_today():
    now = datetime.now()
    if (now.hour > 15 or (now.hour == 15 and now.minute >= 30)) or (now.hour < 9 or (now.hour == 9 and now.minute < 25)):
        return False
    else:
        return True

