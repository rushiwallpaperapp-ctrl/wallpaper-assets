import os
import json
import requests
import time
from PIL import Image
from io import BytesIO

# 1. Setup Folders
folders = ["preview", "HD", "FHD", "2K", "4K"]
for f in folders:
    os.makedirs(f, exist_ok=True)

# 2. Check Tracker
try:
    with open("tracker.txt", "r") as f:
        batch = int(f.read().strip())
except:
    batch = 0

if batch >= 10: 
    batch = 0

print(f"Bhidu, Aajcha Batch: {batch}. Updating 10 images in all 20 categories!")

# 100% Google Play Store Safe Categories (Copyright-Free)
category_prompts = [
    "stunning dark amoled wallpaper, pure black background, 4k masterpiece",
    "epic anime style wallpaper, vibrant colors, 4k masterpiece",
    "breathtaking nature landscape, mountains, 4k masterpiece",
    "cyberpunk futuristic city, neon lights, 4k masterpiece",
    "hyper-realistic supercars, luxury sports bikes, 4k masterpiece",
    "minimalist clean design, modern 4k masterpiece",
    "magical fantasy world, epic ai art, 4k masterpiece",
    "deep space, galaxy, universe, 4k masterpiece",
    "epic futuristic warriors, cyber armor, cinematic lighting, action scene, 4k masterpiece", # Changed from Superheroes
    "abstract 3d render, colorful shapes, 4k masterpiece",
    "cute 3d cartoon animal characters, funny cat and mouse playing, kid shows style, 4k masterpiece", # Changed from Tom & Jerry
    "cute pets, wild animals, lions, dogs, wildlife photography 4k masterpiece",
    "beautiful floral aesthetic, soft pastel colors, roses, for girls 4k masterpiece",
    "epic gaming esports background, cyberpunk gaming 4k masterpiece",
    "peaceful spiritual background, zen, divine 4k masterpiece",
    "neon glowing art, bright led shapes 4k masterpiece",
    "romantic love hearts, moody aesthetic 4k masterpiece",
    "beautiful cityscapes, night city travel aesthetic 4k masterpiece",
    "spooky dark horror background, cinematic 4k masterpiece",
    "liquid texture, metallic geometric patterns 4k masterpiece"
]

latest_updates = []

# 3. Generate and Resize Loop (With 4K Force & Retry Logic)
for cat_index in range(20):
    base_id = (cat_index * 100) 
    start_offset = (batch * 10) + 1 
    
    for j in range(10):
        current_img_num = base_id + start_offset + j
        img_id = f"wall_{current_img_num:04d}" 
        
        prompt = category_prompts[cat_index]
        formatted_prompt = prompt.replace(" ", "%20")
        
        # PRO FIX 1: Direct 4K Resolution demand from AI server
        ai_url = f"https://image.pollinations.ai/prompt/{formatted_prompt}?nologo=true&seed={current_img_num}&width=2160&height=3840"
        
        # PRO FIX 2: Retry Logic
        max_retries = 3
        success = False
        
        for attempt in range(max_retries):
            try:
                print(f"Downloading: {img_id} (Attempt {attempt + 1}/3)...")
                response = requests.get(ai_url, timeout=30)
                
                if response.status_code == 200 and 'image' in response.headers.get('content-type', ''):
                    img = Image.open(BytesIO(response.content))
                    
                    sizes = {
                        'preview': (480, 854),
                        'HD': (720, 1280),
                        'FHD': (1080, 1920),
                        '2K': (1440, 2560),
                        '4K': (2160, 3840)
                    }
                    
                    for folder, res in sizes.items():
                        target_path = os.path.join(folder, f"{img_id}.webp")
                        resized_img = img.resize(res, Image.Resampling.LANCZOS)
                        resized_img.save(target_path, 'WEBP', quality=95 if folder != 'preview' else 60)
                        
                    latest_updates.append(img_id)
                    success = True
                    break 
                else:
                    print(f"Server busy. Retrying...")
                    time.sleep(2) 
                    
            except Exception as e:
                print(f"Error on {img_id}: {e}")
                time.sleep(2)
                
        if not success:
            print(f"Failed to generate {img_id} after 3 attempts. Skipping.")

# 4. Update JSON & Tracker
with open("latest_updates.json", "w") as f:
    json.dump(latest_updates, f)

with open("tracker.txt", "w") as f:
    f.write(str(batch + 1)) 

print("Aajcha target complete Bhidu! High Quality 4K, 100% Copyright-Free images generated.")
