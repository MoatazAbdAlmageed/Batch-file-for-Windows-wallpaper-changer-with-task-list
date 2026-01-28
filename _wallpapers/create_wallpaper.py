from PIL import Image, ImageDraw, ImageFont
import os
import random
import glob

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Read the todo file from parent directory
todo_file = os.path.join(os.path.dirname(script_dir), '_todo.txt')
with open(todo_file, 'r', encoding='utf-8') as f:
    tasks_text = f.read()

# Get all image files from current directory (_wallpapers)
image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif']
wallpapers = []
for ext in image_extensions:
    wallpapers.extend(glob.glob(os.path.join(script_dir, ext)))
    wallpapers.extend(glob.glob(os.path.join(script_dir, ext.upper())))

# Exclude the output file from selection
output_file = os.path.join(script_dir, 'wallpaper_with_tasks.jpg')
wallpapers = [w for w in wallpapers if os.path.abspath(w) != os.path.abspath(output_file)]

if not wallpapers:
    print("Error: No wallpaper images found in _wallpapers directory!")
    print("Please add .jpg, .png, or other image files to the _wallpapers folder.")
    exit(1)

# Randomly pick a wallpaper
selected_wallpaper = random.choice(wallpapers)
print(f"Selected wallpaper: {os.path.basename(selected_wallpaper)}")

# Open the base image
img = Image.open(selected_wallpaper)
width, height = img.size
print(f"Wallpaper size: {width}x{height}")

# Calculate dimensions
# Tasks box is 30% of width from the right
tasks_width_percent = 0.30
tasks_area_width = int(width * tasks_width_percent)

# Tasks box margin from left (right edge)
left_margin_percent = 0.05  # 5% margin from right edge
left_margin = int(width * left_margin_percent)

# Position from right side with left margin
tasks_area_start_x = width - tasks_area_width - left_margin
tasks_area_end_x = width - left_margin

# Tasks area starts from 5% down from top
top_5_percent = int(height * 0.05)

# Padding inside the tasks box (text padding from box edges)
padding_left = 40
padding_right = 40
padding_top = 40
padding_bottom = 40

# Ubuntu font paths
font_bold = None
ubuntu_bold_paths = [
    r"C:/fonts/ubuntu-font-family-0.83/Ubuntu-B.ttf",
    "Ubuntu-B.ttf",
    os.path.join(os.path.dirname(script_dir), "Ubuntu-B.ttf")
]

for font_path in ubuntu_bold_paths:
    try:
        font_bold = ImageFont.truetype(font_path, 32)
        print(f"Using Ubuntu Bold from: {font_path}")
        break
    except Exception as e:
        continue

# Ubuntu Regular font paths
font_regular = None
ubuntu_regular_paths = [
    r"C:/fonts/ubuntu-font-family-0.83/Ubuntu-R.ttf",
    "Ubuntu-R.ttf",
    os.path.join(os.path.dirname(script_dir), "Ubuntu-R.ttf")
]

for font_path in ubuntu_regular_paths:
    try:
        font_regular = ImageFont.truetype(font_path, 20)
        print(f"Using Ubuntu Regular from: {font_path}")
        break
    except Exception as e:
        continue

# Fallback to Arial if Ubuntu not found
if font_bold is None:
    print("Ubuntu Bold not found, using Arial Bold for titles...")
    try:
        font_bold = ImageFont.truetype("arialbd.ttf", 32)
    except:
        try:
            font_bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 32)
        except:
            font_bold = ImageFont.load_default()

if font_regular is None:
    print("Ubuntu Regular not found, using Arial for tasks...")
    try:
        font_regular = ImageFont.truetype("arial.ttf", 20)
    except:
        try:
            font_regular = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
        except:
            font_regular = ImageFont.load_default()

# Create semi-transparent overlay for tasks area
overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
overlay_draw = ImageDraw.Draw(overlay)
overlay_draw.rectangle(
    [(tasks_area_start_x, top_5_percent), (tasks_area_end_x, height)],
    fill=(0, 0, 0, 200)
)

# Composite the overlay
img_rgba = img.convert('RGBA')
img_with_overlay = Image.alpha_composite(img_rgba, overlay)
img = img_with_overlay.convert('RGB')
draw = ImageDraw.Draw(img)

# Starting position (with padding inside the tasks box)
x = tasks_area_start_x + padding_left
y = top_5_percent + padding_top
max_x = tasks_area_end_x - padding_right
max_y = height - padding_bottom
text_width_limit = tasks_area_width - padding_left - padding_right

line_spacing_normal = 30
line_spacing_large = 45
section_gap = 30

# Track if we're in completed tasks section
in_completed_section = False

# Draw the tasks on the image
for line in tasks_text.split('\n'):
    line = line.strip()
    if line:
        # Check if we're running out of vertical space
        if y > max_y:
            break

        # Check if we're entering the COMPLETED TASKS section
        if 'COMPLETED' in line and line.endswith('TASKS'):
            in_completed_section = True
            y += section_gap
            if y > max_y:
                break

        # Set color based on section
        if in_completed_section and not line.endswith('TASKS'):
            text_color = (255, 255, 255, 204)  # 80% opacity
        else:
            text_color = (255, 255, 255, 255)  # 100% opacity

        # Use Ubuntu Bold for section headers
        if line.endswith('TASKS'):
            draw.text((x, y), line, font=font_bold, fill=text_color)
            y += line_spacing_large
        else:
            # Word wrap for long lines
            words = line.split(' ')
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                try:
                    bbox = draw.textbbox((0, 0), test_line, font=font_regular)
                    text_width = bbox[2] - bbox[0]
                except:
                    text_width = len(test_line) * 10

                if text_width < text_width_limit:
                    current_line = test_line
                else:
                    if current_line:
                        draw.text((x, y), current_line.strip(), font=font_regular, fill=text_color)
                        y += line_spacing_normal
                        if y > max_y:
                            break
                    current_line = word + " "

            # Draw remaining text
            if current_line and y <= max_y:
                draw.text((x, y), current_line.strip(), font=font_regular, fill=text_color)
                y += line_spacing_normal

# Save the output image in the same directory
output_path = os.path.join(script_dir, 'wallpaper_with_tasks.jpg')
img.save(output_path, quality=95)
print(f"Wallpaper saved to: {output_path}")
print("Wallpaper created successfully!")