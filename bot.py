import os
import json
import requests
from PIL import Image
from io import BytesIO

# 1. Setup Folders
folders = ["preview", "HD", "FHD", "2K", "4K"]
for f in folders:
    os.makedirs(f, exist_ok=True)

# 2. Check Tracker (Kontya divasacha kam chalu aahe?)
try:
    with open("tracker.txt", "r") as f:
        batch = int(f.read().strip())
except:
    batch = 0

if batch >= 10: 
    batch = 0 # 10 divas zale ki parat 0 pasun (Overwrite loop)

start_id = (batch * 200) + 1
end_id = start_id + 199
print(f"Bhidu, Aajcha Batch: {batch}. Generating Wallpapers from {start_id} to {end_id}")

latest_updates = []

# 3. Generate and Resize Loop
for i in range(start_id, end_id + 1):
    img_id = f"wall_{i:04d}" # Example: wall_001
    
    # Pollinations AI Free Endpoint (Negative prompt is built-in for safety)
    # Using a random seed (i) to get unique images every time
    ai_url = f"https://image.pollinations.ai/prompt/stunning%204k%20mobile%20wallpaper%20masterpiece%20nature%20cyberpunk%20cars?nologo=true&seed={i}"
    
    try:
        response = requests.get(ai_url)
        img = Image.open(BytesIO(response.content))
        
        # Resize parameters
        sizes = {
            'preview': (480, 854),
            'HD': (720, 1280),
            'FHD': (1080, 1920),
            '2K': (1440, 2560),
            '4K': (2160, 3840)
        }
        
        # Save in all 5 folders
        for folder, res in sizes.items():
            target_path = os.path.join(folder, f"{img_id}.webp")
            resized_img = img.resize(res, Image.Resampling.LANCZOS)
            resized_img.save(target_path, 'WEBP', quality=85 if folder != 'preview' else 60)
            
        latest_updates.append(img_id)
        print(f"Successfully generated: {img_id}")
        
    except Exception as e:
        print(f"Error on {img_id}: {e}")

# 4. Update JSON & Tracker
with open("latest_updates.json", "w") as f:
    json.dump(latest_updates, f)

with open("tracker.txt", "w") as f:
    f.write(str(batch + 1)) # Puthchya divasachi tayari

print("Aajcha target complete Bhidu!")
