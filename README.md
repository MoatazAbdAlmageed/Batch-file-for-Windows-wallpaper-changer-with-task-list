# Dynamic Task Wallpaper Generator

Automatically overlay your daily tasks onto your Windows desktop wallpaper. A simple productivity tool that keeps your to-do list always visible!

## 🎯 What It Does

- Randomly picks a wallpaper from your collection
- Overlays your tasks in a clean, readable format
- Updates your Windows wallpaper automatically
- Completed tasks appear at 80% opacity (dimmed)

## 📋 Quick Setup

### Prerequisites
```bash
pip install Pillow
```

### File Structure
```
your_folder/
├── update_wallpaper.bat          # Run this!
├── _todo.txt                     # Your tasks
└── _wallpapers/
    ├── create_wallpaper.py       # Generator script
    ├── image1.jpg                # Add wallpapers here
    └── wallpaper_with_tasks.jpg  # Output
```

### Your Tasks File (`_todo.txt`)
```markdown
## TODAY TASKS
- [ ] Ahmed Ramadan – WhatsApp Update  
- [ ] Bilal System  
- [ ] QL-ME – Certification System

## COMPLETED TASKS
- [x] QuranOasis – Emails Issue  
- [x] Chrome extension
```

### Run It
Double-click `update_wallpaper.bat` - done! ✨

## 🎨 Features

- **30% width** task box on the right side
- **5% margins** from top and right edge
- **Ubuntu Bold** for headers, **Ubuntu Regular** for tasks
- **Semi-transparent** dark overlay for readability
- **Word wrapping** for long task names
- **Random wallpaper** selection for variety

## 🔧 Customization

Edit `create_wallpaper.py` to adjust:
- Box size: `tasks_width_percent = 0.30`
- Margins: `left_margin_percent = 0.05`
- Font sizes: `32` (headers), `20` (tasks)
- Overlay color: `fill=(0, 0, 0, 200)`
- Spacing: `section_gap = 30`

## 💡 Pro Tips

1. Add multiple wallpapers to `_wallpapers` for variety
2. Use fun/meme wallpapers to stay motivated
3. Set up Windows Task Scheduler to run daily
4. Update `_todo.txt` throughout the day

## 🐛 Troubleshooting

**Font not found?** Script falls back to Arial automatically.

**Wallpaper not changing?** Check `_wallpapers/wallpaper_with_tasks.jpg` was created - you can set it manually.

**No images found?** Add `.jpg`, `.png`, or `.gif` files to `_wallpapers` folder.

---

Made with ❤️ for productivity enthusiasts
