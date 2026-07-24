import mss
import time
import os
from datetime import datetime
from PIL import Image, ImageChops
import numpy as np

def images_are_different(img1_path, img2_path, threshold=10):
    img1 = Image.open(img1_path).convert("L").resize((200, 150))
    img2 = Image.open(img2_path).convert("L").resize((200, 150))

    diff = ImageChops.difference(img1, img2)
    diff_array = np.array(diff)
    average_diff = diff_array.mean()

    return average_diff > threshold

last_saved_path = None

with mss.MSS() as sct:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        temp_path = f"data/screenshots/temp_{timestamp}.png"
        sct.shot(output=temp_path)

        if last_saved_path is None or images_are_different(last_saved_path, temp_path):
            final_path = f"data/screenshots/{timestamp}.png"
            os.rename(temp_path, final_path)
            last_saved_path = final_path
            print(f"Saved (changed): {final_path}")
        else:
            os.remove(temp_path)
            print(f"Skipped (no change): {timestamp}")

        time.sleep(5) 