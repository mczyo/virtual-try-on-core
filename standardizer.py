import os
from PIL import Image

def standardize_images():
    input_folder = 'clean_wardrobe'
    output_folder = 'ready_wardrobe'
    
    # Standard AI input size
    TARGET_SIZE = 512 

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")

    if not os.path.exists(input_folder) or not os.listdir(input_folder):
        print("No clean images found! Run bg_remover.py first.")
        return

    print(f"Standardizing images to {TARGET_SIZE}x{TARGET_SIZE}...")

    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            try:
                # 1. Open the transparent image
                img = Image.open(input_path).convert("RGBA")
                
                # 2. Get the bounding box of the actual clothing (ignoring empty transparent space)
                bbox = img.getbbox()
                if bbox:
                    # Crop the image tight around the clothing
                    img = img.crop(bbox)
                
                # 3. Calculate how to scale it so it fits inside 512x512 with a little padding
                img_ratio = img.width / img.height
                if img_ratio > 1:
                    # Wider than tall
                    new_width = int(TARGET_SIZE * 0.8) # 80% of canvas
                    new_height = int(new_width / img_ratio)
                else:
                    # Taller than wide
                    new_height = int(TARGET_SIZE * 0.8)
                    new_width = int(new_height * img_ratio)
                
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # 4. Create a brand new perfectly square transparent canvas
                new_canvas = Image.new("RGBA", (TARGET_SIZE, TARGET_SIZE), (0, 0, 0, 0))
                
                # 5. Paste the clothing dead center on the new canvas
                paste_x = (TARGET_SIZE - new_width) // 2
                paste_y = (TARGET_SIZE - new_height) // 2
                new_canvas.paste(img, (paste_x, paste_y), img) # Use img as mask

                # 6. Save it
                new_canvas.save(output_path)
                print(f"✅ Centered and resized: {filename}")
                
            except Exception as e:
                print(f"❌ Error formatting {filename}: {e}")

    print("\n🎉 Dataset standardized! The 'ready_wardrobe' folder is ready for AI Training.")

if __name__ == "__main__":
    standardize_images()