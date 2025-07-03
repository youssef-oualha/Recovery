# Recover - Multi-Format File Recovery Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This tool helps recover multiple file types from forensic disk images. It detects and extracts files based on their signature bytes. It provides two interfaces:
1. A simple GUI application using Tkinter
2. A web interface using Flask

## Prerequisites

- Python 3.x installed
- `recover.exe` in the same directory (compiled from recover.c)
- A forensic disk image (see "Creating a Forensic Image" section below)

## Supported File Types

This tool can recover the following file types:

1. **JPEG Images** - Signature: `0xFF 0xD8 0xFF 0xE0-0xEF`
2. **PNG Images** - Signature: `0x89 0x50 0x4E 0x47 0x0D 0x0A 0x1A 0x0A`
3. **PDF Documents** - Signature: `0x25 0x50 0x44 0x46`
4. **DOCX Documents** - Signature: `0x50 0x4B 0x03 0x04` (ZIP format)

### Potential Future Extensions

The tool could be extended to support additional file types such as:

1. **GIF Images** - Signature: `0x47 0x49 0x46 0x38 0x37/0x39 0x61` (GIF87a/GIF89a)
2. **MP3 Audio** - Signature: `0x49 0x44 0x33` (ID3) or `0xFF 0xFB` (MPEG frame sync)
3. **MP4 Video** - Signature: Various, typically starts with `0x66 0x74 0x79 0x70` (ftyp)
4. **ZIP Archives** - Signature: `0x50 0x4B 0x03 0x04`
5. **RAR Archives** - Signature: `0x52 0x61 0x72 0x21 0x1A 0x07`
6. **EXE Files** - Signature: `0x4D 0x5A` (MZ)
7. **DOCX/XLSX/PPTX** - All use ZIP format signature
8. **BMP Images** - Signature: `0x42 0x4D` (BM)

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
7. Recovered files will be saved in the current directory with appropriate extensions (.jpg, .png, .pdf, .docx)

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
5. The application will process the image and recover all supported file types
6. Recovered files will be saved in the current directory with appropriate extensions

## Creating a Forensic Image

Before using this recovery tool, you need to create a forensic image of your storage device. We recommend using FTK Imager, a free forensic tool:

1. **Download and Install FTK Imager**:
   - Download the free version of FTK Imager from AccessData's website
   - Install the application following the provided instructions

2. **Create a Forensic Image**:
   - Launch FTK Imager
   - Click on "File" > "Create Disk Image"
   - Select the source evidence type (Physical Drive for USB drives)
   - Select the specific device you want to image
   - Choose "Raw Image (.dd)" as the image type
   - Specify a destination location and filename
   - Complete the evidence information form (optional)
   - Click "Finish" to create the image

3. **Use the Image with This Tool**:
   - Once the imaging process is complete, you can use the resulting .dd file with this recovery tool
   - The forensic image preserves the exact state of the storage device, allowing for safe recovery without modifying the original media

## Sample Test Files

You can test the recovery functionality with:
- Forensic disk images (.img, .raw, .dd) created with FTK Imager or similar tools
- Memory card dumps
- Any file that contains supported file types that need to be recovered

A test script `test_recover.py` is included to verify the recovery functionality with all supported file types.

## Notes

- Both interfaces call the same underlying `recover.exe` executable
- Recovered files will be named ###.ext (where ### is a sequential number and ext is the appropriate extension)
- Files are detected by checking for their unique signature bytes
- Files are processed in binary mode to ensure proper handling of data
- Always work with a forensic image rather than the original storage device to preserve evidence integrity
- This tool performs file carving based on signatures and does not recover file names or directory structures

## Troubleshooting

If you encounter issues with the recovery process:

1. Make sure `recover.exe` is compiled correctly from `recover.c`
2. Verify that the input file is a valid disk image containing supported file types
3. Check that you have write permissions in the current directory
4. Run the included `test_recover.py` script to verify that all file types can be recovered correctly

## Testing Recovery

To test the recovery functionality with all supported file types:

```
python test_recover.py
```

This will create a test file with signatures for all supported formats and attempt to recover them.