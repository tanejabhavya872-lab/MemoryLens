import mss
import time
from datetime import datetime

with mss.MSS() as sct:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"data/screenshots/{timestamp}.png"
        sct.shot(output=filename)
        print(f"Saved: {filename}")
        time.sleep(5)