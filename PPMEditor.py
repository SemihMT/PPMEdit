import tkinter as tk
from tkinter import colorchooser, simpledialog, filedialog, Label, Toplevel, Canvas, Tk
from tkinter import messagebox
from PIL import Image
import os

class PPMEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("PPM Editor")

        self.width, self.height = 32, 26  # grid dimensions
        self.pixel_size = 20  # size of each pixel in the grid
        self.current_color = "#000000"  # default color
        self.grid = []
        self.metadata = {}  # to store metadata comments
        self.metadata_mode = False  # flag for metadata mode

        self.create_widgets()
        self.create_grid()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=self.width * self.pixel_size,
                                height=self.height * self.pixel_size)
        self.canvas.grid(row=0, columnspan=6)
        self.canvas.bind("<ButtonPress-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)
        self.canvas.bind("<ButtonPress-3>", self.paint_or_metadata)  # Right click for paint/metadata
        self.canvas.bind("<B3-Motion>", self.paint)  # Right click drag for painting
        self.canvas.bind("<Motion>", self.show_tooltip)


        self.color_button = tk.Button(self.root, text="Choose Color", command=self.choose_color)
        self.color_button.grid(row=1, column=0)

        self.eraser_button = tk.Button(self.root, text="Eraser", command=self.use_eraser)
        self.eraser_button.grid(row=1, column=1)

        self.metadata_button = tk.Button(self.root, text="Metadata Tool", command=self.toggle_metadata_mode)
        self.metadata_button.grid(row=1, column=2)

        self.save_button = tk.Button(self.root, text="Save PPM", command=self.save_ppm)
        self.save_button.grid(row=1, column=3)

        self.open_button = tk.Button(self.root, text="Open PPM", command=self.open_ppm)
        self.open_button.grid(row=1, column=4)

        self.select_button = tk.Button(self.root, text="Select Area", command=self.select_area)
        self.select_button.grid(row=1, column=5)

    def start_selection(self, event):
        self.start_x = event.x // self.pixel_size
        self.start_y = event.y // self.pixel_size

    def update_selection(self, event):
        self.canvas.delete("selection")
        end_x = event.x // self.pixel_size
        end_y = event.y // self.pixel_size
        self.canvas.create_rectangle(
            self.start_x * self.pixel_size, self.start_y * self.pixel_size,
            (end_x + 1) * self.pixel_size, (end_y + 1) * self.pixel_size,
            outline="blue", tags="selection"
        )

    def end_selection(self, event):
        self.canvas.delete("selection")
        end_x = event.x // self.pixel_size
        end_y = event.y // self.pixel_size
        selected_pixels = []
        for y in range(min(self.start_y, end_y), max(self.start_y, end_y) + 1):
            for x in range(min(self.start_x, end_x), max(self.start_x, end_x) + 1):
                selected_pixels.append((x, y))
        print("Selected pixels:", selected_pixels)



    def create_grid(self):
        for y in range(self.height):
            row = []
            for x in range(self.width):
                rect = self.canvas.create_rectangle(
                    x * self.pixel_size, y * self.pixel_size,
                    (x + 1) * self.pixel_size, (y + 1) * self.pixel_size,
                    fill="#FFFFFF", outline="gray"
                )
                row.append(rect)
            self.grid.append(row)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose color")[1]
        if color_code:
            self.current_color = color_code
            self.metadata_mode = False  # Turn off metadata mode if color is chosen

    def use_eraser(self):
        self.current_color = "#FFFFFF"
        self.metadata_mode = False  # Turn off metadata mode if eraser is chosen

    def toggle_metadata_mode(self):
        self.metadata_mode = not self.metadata_mode
        if self.metadata_mode:
            self.root.config(cursor="question_arrow")
        else:
            self.root.config(cursor="")

    def paint_or_metadata(self, event):
        if self.metadata_mode:
            self.add_metadata(event)
        else:
            self.paint(event)

    def paint(self, event):
        x, y = event.x // self.pixel_size, event.y // self.pixel_size
        if 0 <= x < self.width and 0 <= y < self.height:
            self.canvas.itemconfig(self.grid[y][x], fill=self.current_color)
            if self.current_color == "#FFFFFF":
                self.metadata.pop((x, y), None)
            else:
                self.metadata[(x, y)] = None

    def add_metadata(self, event):
        x, y = event.x // self.pixel_size, event.y // self.pixel_size
        if 0 <= x < self.width and 0 <= y < self.height:
            comment = simpledialog.askstring("Metadata", f"Enter metadata for pixel ({x}, {y}):")
            if comment:
                self.metadata[(x, y)] = comment

    def show_tooltip(self, event):
        x, y = event.x // self.pixel_size, event.y // self.pixel_size
        tooltip_text = self.metadata.get((x, y))
        if tooltip_text:
            if hasattr(self, "tooltip"):
                self.tooltip.destroy()
            self.tooltip = Toplevel(self.root)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            label = Label(self.tooltip, text=tooltip_text, background="lightyellow", relief="solid", borderwidth=1)
            label.pack(ipadx=5, ipady=5)
        else:
            if hasattr(self, "tooltip"):
                self.tooltip.destroy()

    def select_area(self):
        x1 = simpledialog.askinteger("Select Area", "Enter start x:")
        y1 = simpledialog.askinteger("Select Area", "Enter start y:")
        x2 = simpledialog.askinteger("Select Area", "Enter end x:")
        y2 = simpledialog.askinteger("Select Area", "Enter end y:")
        if None in (x1, y1, x2, y2):
            return

        comment = simpledialog.askstring("Metadata", "Enter metadata for the selected area:")

        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.canvas.itemconfig(self.grid[y][x], fill=self.current_color)
                    self.metadata[(x, y)] = comment

    def save_ppm(self):
        ppm_type = simpledialog.askstring("PPM Type", "Enter PPM type (P3 or P6):")
        if ppm_type not in ["P3", "P6"]:
            messagebox.showerror("Error", "Invalid PPM type.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".ppm", filetypes=[("PPM files", "*.ppm")])
        if not file_path:
            return

        with open(file_path, 'wb') as f:
            f.write(f"{ppm_type}\n".encode())
            f.write(f"# Metadata: Generated by PPM Editor\n".encode())

            for (x, y), comment in self.metadata.items():
                if comment:
                    f.write(f"# Metadata: ({x}, {y}) {comment}\n".encode())

            f.write(f"{self.width} {self.height}\n255\n".encode())

            for y in range(self.height):
                for x in range(self.width):
                    color = self.canvas.itemcget(self.grid[y][x], 'fill')
                    r, g, b = self.hex_to_rgb(color)
                    if ppm_type == "P3":
                        f.write(f"{r} {g} {b} ".encode())
                    else:
                        f.write(bytes([r, g, b]))

    def open_ppm(self):
        file_path = filedialog.askopenfilename(filetypes=[("PPM files", "*.ppm")])
        if not file_path:
            return

        with open(file_path, 'rb') as f:
            ppm_type = f.readline().strip()
            if ppm_type not in [b"P3", b"P6"]:
                messagebox.showerror("Error", "Invalid PPM file.")
                return

            metadata = {}
            dimensions = f.readline().strip()
            while dimensions.startswith(b"#"):
                if dimensions.startswith(b"# Metadata:"):
                    parts = dimensions.split(b":", 1)[1].strip().split(b" ", 2)
                    if len(parts) == 3:
                        x_str = parts[0].split(b",")[0].lstrip(b"(")
                        y_str = parts[1].rstrip(b")")
                        try:
                            x, y = int(x_str), int(y_str)
                            comment = parts[2].decode('utf-8')
                            metadata[(x, y)] = comment
                        except ValueError:
                            pass
                dimensions = f.readline().strip()

            width, height = map(int, dimensions.split())
            max_color = int(f.readline().strip())

            if self.width != width or self.height != height:
                messagebox.showerror("Error", "Dimensions of the loaded PPM file do not match the current canvas size.")
                return
        
            if ppm_type == b"P3":
                pixel_data = f.read().decode('utf-8').split()
                index = 0
                for y in range(self.height):
                    for x in range(self.width):
                        r, g, b = map(int, pixel_data[index:index+3])
                        index += 3
                        color = f"#{r:02x}{g:02x}{b:02x}"
                        self.canvas.itemconfig(self.grid[y][x], fill=color)
            else:  # P6
                pixels = f.read(self.width * self.height * 3)
                index = 0
                for y in range(self.height):
                    for x in range(self.width):
                        r, g, b = pixels[index:index+3]
                        index += 3
                        color = f"#{r:02x}{g:02x}{b:02x}"
                        self.canvas.itemconfig(self.grid[y][x], fill=color)
                        

            self.metadata = metadata
            print(metadata)



    @staticmethod
    def hex_to_rgb(hex_color):
        if hex_color == "":
            return (255, 255, 255)  # Return white for empty color
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

if __name__ == "__main__":
    root = tk.Tk()
    editor = PPMEditor(root)
    root.mainloop()
