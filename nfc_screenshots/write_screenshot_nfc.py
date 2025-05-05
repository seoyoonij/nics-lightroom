import random
from datetime import datetime, timedelta

import nfc
import nfc.ndef

# 1) Pick a random date in the last 30 days (YYYYMMDD)
def pick_random_date(days_back=30):
    today = datetime.today()
    rand_dt = today - timedelta(days=random.randint(0, days_back-1))
    return rand_dt.strftime("%Y%m%d")

random_code = pick_random_date()

# 2) Build the URL for Google Photos screenshots on that date
uri_random = nfc.ndef.UriRecord(
    f"https://photos.google.com/search/#date_range:{random_code}-{random_code}"
)

# 3) Other records (Android/iCloud/OneDrive/etc.)
aar          = nfc.ndef.AndroidApplicationRecord("com.google.android.apps.photos")
uri_icloud   = nfc.ndef.UriRecord("https://www.icloud.com/photos/#/screenshots/")
uri_onedrive = nfc.ndef.UriRecord(
    "https://onedrive.live.com/?id=root&view=thumbnails&path=%2Fdrive%2Froot%2FPictures%2FScreenshots"
)

# 4) Assemble message (random Google Photos first)
message = nfc.ndef.Message([aar, uri_random, uri_icloud, uri_onedrive])

# 5) Write to NFC tag on first tap
def write_tag():
    with nfc.ContactlessFrontend('usb') as clf:
        clf.connect(rdwr={'on-connect': lambda tag: tag.ndef.write(message) or False})
        print(f"✅ NFC tag written. Random date: {random_code}")

if __name__ == "__main__":
    write_tag()
