"""

this program counts the number of pixels in a given image
in order to classify the quality of the printhead.
the program will dislay the total number of pixels and the number of dark pixels.
It will then calculate the percentage of the total pixels of the image,
and then rank the image based on the percentage of the dark pixels.


"""
 
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

class ImageBoxCounter:
    def __init__(self, root):
        self.root = root
        self.root.title("Dark Pixel and Total Pixel Counter with Ranking")

        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.image = None
        self.image_tk = None
        self.rectangles = []
        self.start_x = None
        self.start_y = None

        self.control_frame = tk.Frame(root)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.threshold_scale = tk.Scale(
            self.control_frame, from_=0, to=255, orient=tk.HORIZONTAL, label="Darkness Threshold", length=200
        )
        self.threshold_scale.set(150)
        self.threshold_scale.pack()

        self.count_text = tk.Label(self.control_frame, text="Dark Pixels: 0 | Total Pixels: 0 | Rank: N/A", fg="black")
        self.instr_text2 = tk.Label(self.control_frame, text=f"Drag mouse from top left to bottom right of the image.", fg="red")
        self.count_text.pack()
        self.instr_text2.pack()
        

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        menubar = tk.Menu(root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Image", command=self.open_image)
        menubar.add_cascade(label="File", menu=file_menu)
        root.config(menu=menubar)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.load_image(file_path)

    def load_image(self, path):
        self.original_image = Image.open(path).convert("RGB")
        self.image = self.original_image.copy()
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

    def on_button_press(self, event):

        self.rectangles = []
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.image = self.original_image.copy()
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.redraw()
        self.start_x, self.start_y = event.x, event.y
        self.rectangles.append((self.start_x, self.start_y, self.start_x, self.start_y))
        self.draw_rectangle()

    def on_mouse_drag(self, event):
        self.rectangles[-1] = (self.start_x, self.start_y, event.x, event.y)
        self.redraw()

    def on_button_release(self, event):
        self.rectangles[-1] = (self.start_x, self.start_y, event.x, event.y)
        dark_pixel_count, total_pixel_count = self.count_dark_pixels(self.threshold_scale.get())
        rank = self.rank_image(dark_pixel_count, total_pixel_count)
        self.update_count_text(dark_pixel_count, total_pixel_count, rank)
        self.reset()

    def draw_rectangle(self):
        x1, y1, x2, y2 = self.rectangles[-1]
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="red")

    def redraw(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        for rect in self.rectangles:
            self.canvas.create_rectangle(rect, outline="red")

    def count_dark_pixels(self, threshold):
        if self.original_image is None:
            return 0, 0

        img_array = np.array(self.original_image)
        x1, y1, x2, y2 = self.rectangles[-1]
        x1, y1, x2, y2 = max(0, x1), max(0, y1), min(x2, img_array.shape[1]), min(y2, img_array.shape[0])
        box = img_array[y1:y2, x1:x2]

        mask = np.all(box < threshold, axis=-1)
        dark_pixel_count = np.sum(mask)
        total_pixel_count = box.shape[0] * box.shape[1]

        # Highlight dark pixels in blue
        if np.any(mask):
            img_array[y1:y2, x1:x2][mask] = [0, 0, 255]  # Set dark pixels to blue

        # Update displayed image with highlighted dark pixels
        self.image = Image.fromarray(img_array)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.redraw()

        return dark_pixel_count, total_pixel_count
    
    def rank_image(self, dark_count, total_count):
        if total_count == 0:
            return "N/A"
        
        percentage = (dark_count / total_count) * 100
        rank = int(percentage // 5) + 1
        return min(rank, 20)


    def update_count_text(self, dark_count, total_count, rank):
        self.count_text.config(
            text=f"Dark Pixels: {dark_count} | Total Pixels: {total_count} | Rank: {rank} "
        )

    def reset(self):
        self.rectangles = []  # Clear all rectangles
        self.redraw()  # Redraw the canvas

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageBoxCounter(root)
    root.mainloop()
