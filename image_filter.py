from PIL import Image, ImageFilter, ImageOps
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# --- Core Filter Functions ---
def apply_grayscale(img):
    return img.convert("L")

def apply_blur(img, strength=3):
    """Brute-force blur by resizing down and up"""
    small_size = (img.width//strength, img.height//strength)
    return img.resize(small_size, Image.BILINEAR).resize(img.size, Image.NEAREST)

def apply_edge_enhance(img):
    return img.filter(ImageFilter.EDGE_ENHANCE)

def apply_invert(img):
    if img.mode == 'RGBA':
        # Split into RGB and Alpha, invert RGB only
        r, g, b, a = img.split()
        rgb = Image.merge('RGB', (r, g, b))
        inverted = ImageOps.invert(rgb)
        r, g, b = inverted.split()
        return Image.merge('RGBA', (r, g, b, a))
    else:
        return ImageOps.invert(img)

def apply_sepia(img):
    # Convert to RGB if image has transparency (RGBA)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    width, height = img.size
    pixels = img.load()
    for py in range(height):
        for px in range(width):
            r, g, b = img.getpixel((px, py))  # Now guaranteed 3 values
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            pixels[px, py] = (min(255, tr), min(255, tg), min(255, tb))
    return img

# --- Main Application ---
class ImageFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image Filter App")
        self.root.geometry("500x400")
        
        self.image_path = None
        self.original_image = None
        self.filtered_image = None
        
        # GUI Elements
        self.setup_ui()
    
    def setup_ui(self):
        # Open Image Button
        tk.Button(self.root, text="Open Image", command=self.open_image).pack(pady=10)
        
        # Filter Buttons
        filters = [
            ("Grayscale", "grayscale"),
            ("Blur", "blur"),
            ("Edge Enhance", "edge_enhance"),
            ("Invert", "invert"),
            ("Sepia", "sepia")
        ]
        
        for (text, filter_name) in filters:
            tk.Button(
                self.root, 
                text=text, 
                command=lambda f=filter_name: self.apply_filter(f)
            ).pack(pady=2)
        
        # Status Label
        self.status = tk.Label(self.root, text="No image loaded")
        self.status.pack(pady=10)
    
    def open_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if self.image_path:
            try:
                self.original_image = Image.open(self.image_path)
                self.status.config(text=f"Loaded: {os.path.basename(self.image_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
    
    def apply_filter(self, filter_name):
        if not self.image_path:
            messagebox.showwarning("Warning", "Please open an image first!")
            return
        
        try:
            filter_map = {
                "grayscale": apply_grayscale,
                "blur": apply_blur,
                "edge_enhance": apply_edge_enhance,
                "invert": apply_invert,
                "sepia": apply_sepia
            }
            
            self.filtered_image = filter_map[filter_name](self.original_image)
            output_path = f"filtered_{filter_name}_{os.path.basename(self.image_path)}"
            self.filtered_image.save(output_path)
            
            # Show the filtered image
            self.filtered_image.show()
            self.status.config(text=f"Saved as: {output_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Filter failed:\n{str(e)}")

# --- Console Mode (Fallback) ---
def console_mode():
    print("\n🌟 Python Image Filter App 🌟")
    print("Filters: grayscale | blur | edge_enhance | invert | sepia")
    
    image_path = input("Drag your image here or type its path: ").strip('"')
    if not os.path.isfile(image_path):
        print("❌ Error: Invalid image path!")
        return
    
    filter_name = input("Choose a filter: ").strip().lower()
    
    try:
        img = Image.open(image_path)
        filter_map = {
            "grayscale": apply_grayscale,
            "blur": apply_blur,
            "edge_enhance": apply_edge_enhance,
            "invert": apply_invert,
            "sepia": apply_sepia
        }
        
        if filter_name not in filter_map:
            print("❌ Invalid filter! Choose from:", list(filter_map.keys()))
            return
        
        filtered_img = filter_map[filter_name](img)
        output_path = f"filtered_{filter_name}_{os.path.basename(image_path)}"
        filtered_img.save(output_path)
        print(f"✅ Saved as '{output_path}'")
        filtered_img.show()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

# --- Run the App ---
if __name__ == "__main__":
    try:
        # Try to start GUI mode
        root = tk.Tk()
        app = ImageFilterApp(root)
        root.mainloop()
    except:
        # Fallback to console mode if GUI fails
        console_mode()