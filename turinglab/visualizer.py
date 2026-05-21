"""
Bonus D: Görselleştirici (Pillow ve imageio tabanlı)
"""
import os
from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio

class Visualizer:
    def __init__(self, cell_size: int = 50, padding: int = 20):
        self.cell_size = cell_size
        self.padding = padding
        
    def _draw_frame(self, step_data: dict, frame_index: int, output_dir: str):
        tape_dict = step_data["tape_dict"]
        head_pos = step_data["head"]
        state = step_data["state"]
        step = step_data["step"]
        
        if not tape_dict:
            min_pos, max_pos = 0, 0
        else:
            min_pos = min(min(tape_dict.keys()), head_pos) - 2
            max_pos = max(max(tape_dict.keys()), head_pos) + 2
            
        num_cells = max_pos - min_pos + 1
        img_width = num_cells * self.cell_size + 2 * self.padding
        img_height = self.cell_size * 3 + 2 * self.padding
        
        img = Image.new("RGB", (img_width, img_height), color="white")
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
            
        draw.text((self.padding, self.padding), f"Step: {step} | State: {state}", fill="black", font=font)
        
        y_offset = self.padding + 50
        for i, pos in enumerate(range(min_pos, max_pos + 1)):
            char = tape_dict.get(pos, "B")
            x1 = self.padding + i * self.cell_size
            y1 = y_offset
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            fill_color = "yellow" if pos == head_pos else "white"
            draw.rectangle([x1, y1, x2, y2], fill=fill_color, outline="black", width=2)
            
            text_x = x1 + self.cell_size // 3
            text_y = y1 + self.cell_size // 4
            draw.text((text_x, text_y), str(char), fill="black", font=font)
            
        head_index = head_pos - min_pos
        arrow_x = self.padding + head_index * self.cell_size + self.cell_size // 2
        arrow_y = y_offset + self.cell_size + 10
        draw.polygon([(arrow_x, arrow_y), (arrow_x - 10, arrow_y + 20), (arrow_x + 10, arrow_y + 20)], fill="red")
        
        os.makedirs(output_dir, exist_ok=True)
        frame_path = os.path.join(output_dir, f"frame_{frame_index:04d}.png")
        img.save(frame_path)
        return frame_path
        
    def generate_gif(self, history: list[dict], output_file: str, duration: int = 500):
        temp_dir = "temp_frames"
        frame_paths = []
        for i, step_data in enumerate(history):
            path = self._draw_frame(step_data, i, temp_dir)
            frame_paths.append(path)
            
        frames = [imageio.imread(p) for p in frame_paths]
        imageio.mimsave(output_file, frames, format='GIF', duration=duration/1000.0)
        
        for p in frame_paths:
            try:
                os.remove(p)
            except OSError:
                pass
        try:
            os.rmdir(temp_dir)
        except OSError:
            pass
