# Recover - JPEG Recovery Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This tool helps recover JPEG files from disk images. It specifically detects and extracts JPEG files based on their signature bytes (0xFF, 0xD8, 0xFF, 0xE0-0xEF). It provides two interfaces:
1. A simple GUI application using Tkinter
2. A web interface using Flask

## Prerequisites

- Python 3.x installed
- `recover.exe` in the same directory (compiled from recover.c)

## Testing the Tkinter GUI

1. Open a command prompt or terminal
2. Navigate to the project directory
3. Run the GUI application:
   ```
   python recover_gui.py
   ```
4. A simple window will appear with a "Select Drive Image" button
5. Click the button and select your disk image file
6. The application will run recover.exe on the selected file
7. Recovered JPEG files will be saved in the current directory

## Testing the Flask Web Interface

1. Make sure you have Flask installed:
   ```
   pip install flask
   ```
2. Run the Flask application:
   ```
   python app.py
   ```
3. Open a web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```
4. Use the file upload form to select and upload your disk image
5. The application will process the image and recover JPEG files
6. Recovered files will be saved in the current directory

## Sample Test Files

You can test the recovery functionality with:
- Any raw disk image (.img, .raw, .dd)
- Memory card dumps
- Any file that contains JPEG data that needs to be recovered

## Notes

- Both interfaces call the same underlying `recover.exe` executable
- The current implementation doesn't show progress during recovery
- Recovered files will be named ###.jpg (where ### is a sequential number)
- This tool specifically detects JPEG files by checking for the JPEG signature bytes (0xFF, 0xD8, 0xFF, 0xE0-0xEF)
- Only JPEG files will be recovered from the disk image
- Files are processed in binary mode to ensure proper handling of image data

## Troubleshooting

If you encounter issues with the recovery process:

1. Make sure `recover.exe` is compiled correctly from `recover.c`
2. Verify that the input file is a valid disk image containing JPEG files
3. Check that you have write permissions in the current directory