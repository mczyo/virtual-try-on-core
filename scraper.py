import requests
import os
import time

def industrial_harvest(target_total=200):
    folder_name = 'raw_wardrobe'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Expanded categories for a full fashion catalog
    categories = [
        "mens-shirts", "mens-shoes", "mens-watches", 
        "womens-dresses", "womens-shoes", "womens-bags", 
        "womens-jewellery", "tops", "sunglasses"
    ]
    
    downloaded = 0
    print(f"🚀 Starting Industrial Harvest. Goal: {target_total} items.")

    for cat in categories:
        if downloaded >= target_total: break
        
        # We use a larger limit per category
        url = f"https://dummyjson.com/products/category/{cat}?limit=20"
        try:
            res = requests.get(url)
            if res.status_code == 200:
                products = res.json().get('products', [])
                for p in products:
                    if downloaded >= target_total: break
                    
                    img_url = p['images'][0]
                    # Create a clean filename
                    clean_title = "".join([c for c in p['title'] if c.isalnum()])
                    filename = f"{downloaded:03d}_{clean_title}.jpg"
                    
                    path = os.path.join(folder_name, filename)
                    with open(path, 'wb') as f:
                        f.write(requests.get(img_url).content)
                    
                    print(f"📦 [{downloaded+1}/{target_total}] Saved: {filename}")
                    downloaded += 1
                    time.sleep(0.5) # Protect the HDD
        except Exception as e:
            print(f"❌ Error in {cat}: {e}")

    print(f"\n✅ Factory Output: {downloaded} items ready for processing.")

if __name__ == "__main__":
    industrial_harvest(100)