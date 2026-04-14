import os
from PIL import Image

def generate_masks():
    input_folder = 'ready_wardrobe'
    output_folder = 'mask_wardrobe'

    # Create output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")

    if not os.path.exists(input_folder) or not os.listdir(input_folder):
        print("No standardized images found! Run standardizer.py first.")
        return

    print("Generating AI Binary Masks from Alpha Channels...")

    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            try:
                # 1. Open the standardized transparent image
                img = Image.open(input_path).convert("RGBA")
                
                # 2. Create a blank black canvas of the exact same size (L mode = grayscale)
                mask = Image.new("L", img.size, 0)
                
                # 3. Extract the Alpha (transparency) channel from the clothing image
                alpha_channel = img.split()[3]
                
                # 4. Paste pure white (255) anywhere the clothing exists
                mask.paste(255, box=None, mask=alpha_channel)
                
                # 5. Save the black-and-white mask
                mask.save(output_path)
                print(f"✅ Mask generated: {filename}")
                
            except Exception as e:
                print(f"❌ Error generating mask for {filename}: {e}")

    print("\n🎉 Mask generation complete! Your dataset is fully prepped for AI.")

if __name__ == "__main__":
    generate_masks()