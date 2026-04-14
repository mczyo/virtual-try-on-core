import os
from rembg import remove
from PIL import Image
import time

def process_wardrobe():
    input_folder = 'raw_wardrobe'
    output_folder = 'clean_wardrobe'

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")

    # Check if we have images to process
    if not os.path.exists(input_folder) or not os.listdir(input_folder):
        print("No images found in raw_wardrobe! Run the scraper first.")
        return

    print("Starting AI Background Removal. This may take a moment per image on a CPU...")

    for filename in os.listdir(input_folder):
        # We only want to process image files
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            
            # Change the extension from .jpg to .png for transparency
            new_filename = os.path.splitext(filename)[0] + ".png"
            output_path = os.path.join(output_folder, new_filename)

            try:
                # Open the image using PIL (Pillow)
                input_image = Image.open(input_path)
                
                # The AI magic happens here
                print(f"Processing: {filename}...")
                output_image = remove(input_image)
                
                # Save the new transparent image
                output_image.save(output_path)
                print(f"✅ Saved clean image to: {new_filename}")
                
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")

    print("\n🎉 Background removal complete! Check the clean_wardrobe folder.")

if __name__ == "__main__":
    process_wardrobe()