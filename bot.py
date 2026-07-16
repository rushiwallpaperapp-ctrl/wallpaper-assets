import os
import json
import requests
from PIL import Image
from io import BytesIO

# 1. Setup Folders
folders = ["preview", "HD", "FHD", "2K", "4K"]
for f in folders:
    os.makedirs(f, exist_ok=True)

# 2. Check Tracker (Kontya divasacha batch chalu aahe?)
try:
    with open("tracker.txt", "r") as f:
        batch = int(f.read().strip())
except:
    batch = 0

# 10 Days Loop (Batch 0 to 9). 10 zale ki parat 0 (2000 images strict limit).
if batch >= 10: 
    batch = 0

print(f"Bhidu, Aajcha Batch: {batch}. Updating 10 images in all 20 categories!")

# 20 Categories Prompts List (Tu yaat nantar badal karu shaktos)
category_prompts = [
    "stunning dark amoled wallpaper, pure black background, 4k", # Cat 0: Dark
    "epic anime style wallpaper, vibrant colors, 4k", # Cat 1: Anime
    "breathtaking nature landscape, mountains, 4k", # Cat 2: Nature
    "cyberpunk futuristic city, neon lights, 4k", # Cat 3: Cyberpunk
    "hyper-realistic supercars, luxury sports bikes, 4k", # Cat 4: Vehicles
    "minimalist clean design, modern 4k", # Cat 5: Minimalist
    "magical fantasy world, epic ai art, 4k", # Cat 6: Fantasy
    "deep space, galaxy, universe, 4k", # Cat 7: Space
    "superhero cinematic lighting, epic action scene, 4k", # Cat 8: Superheroes
    "abstract 3d render, colorful shapes, 4k", # Cat 9: Abstract
    "cute 3d cartoon characters, kid shows style like tom and jerry, 4k", # Cat 10: Cartoons
    "cute pets, wild animals, lions, dogs, wildlife photography 4k", # Cat 11: Animals
    "beautiful floral aesthetic, soft pastel colors, roses, for girls 4k", # Cat 12: Floral
    "epic gaming esports background, cyberpunk gaming 4k", # Cat 13: Gaming
    "peaceful spiritual background, zen, divine 4k", # Cat 14: Spiritual
    "neon glowing art, bright led shapes 4k", # Cat 15: Neon
    "romantic love hearts, moody aesthetic 4k", # Cat 16: Love
    "beautiful cityscapes, night city travel aesthetic 4k", # Cat 17: Cityscapes
    "spooky dark horror background, cinematic 4k", # Cat 18: Horror
    "liquid texture, metallic geometric patterns 4k" # Cat 19: Patterns
]

latest_updates = []

# 3. Generate and Resize Loop (Horizontal Update)
for cat_index in range(20):
    base_id = (cat_index * 100) # Base ID for the category (e.g., 0, 100, 200)
    start_offset = (batch * 10) + 1 # Offset based on the day (e.g., 1 to 10)
    
    for j in range(10):
        current_img_num = base_id + start_offset + j
        img_id = f"wall_{current_img_num:04d}" # Result: wall_0001, wall_0101, etc.
        
        prompt = category_prompts[cat_index]
        formatted_prompt = prompt.replace(" ", "%20")
        
        # Pollinations API with unique seed (Uses image ID to keep images unique)
        ai_url = f"https://image.pollinations.ai/prompt/{formatted_prompt}?nologo=true&seed={current_img_num}"
        
        try:
            print(f"Downloading: {img_id} (Category {cat_index})...")
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
                # Quality 60 for preview thumbnail, 85 for actual downloads
                resized_img.save(target_path, 'WEBP', quality=85 if folder != 'preview' else 60)
                
            latest_updates.append(img_id)
            
        except Exception as e:
            print(f"Error on {img_id}: {e}")

# 4. Update JSON & Tracker
with open("latest_updates.json", "w") as f:
    json.dump(latest_updates, f)

with open("tracker.txt", "w") as f:
    f.write(str(batch + 1)) # Next day sathi tracker update

print("Aajcha target complete Bhidu! 200 images generated and optimized successfully.")
