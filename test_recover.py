import subprocess
import os
import glob

def main():
    # Create a test file with multiple file signatures
    with open('test_recovery.raw', 'wb') as f:
        # Create some random data
        f.write(b'\x00' * 512)
        
        # Add a JPEG signature
        f.write(b'\xFF\xD8\xFF\xE0' + b'\x00' * 508)
        
        # Add some image data
        f.write(b'\x00' * 512)
        
        # Add a PNG signature
        f.write(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A' + b'\x00' * 504)
        
        # Add some PNG data
        f.write(b'\x00' * 512)
        
        # Add a PDF signature
        f.write(b'\x25\x50\x44\x46' + b'\x00' * 508)
        
        # Add some PDF data
        f.write(b'\x00' * 512)
        
        # Add a DOCX signature (ZIP format)
        f.write(b'\x50\x4B\x03\x04' + b'\x00' * 508)
        
        # Add some DOCX data
        f.write(b'\x00' * 512)
        
        # Add a GIF signature (GIF89a)
        f.write(b'\x47\x49\x46\x38\x39\x61' + b'\x00' * 506)
        
        # Add some GIF data
        f.write(b'\x00' * 512)
        
        # Add an MP3 signature (ID3)
        f.write(b'\x49\x44\x33' + b'\x00' * 509)
        
        # Add some MP3 data
        f.write(b'\x00' * 512)
        
        # Add a BMP signature
        f.write(b'\x42\x4D' + b'\x00' * 510)
        
        # Add some BMP data
        f.write(b'\x00' * 512)
        
        # Add a RAR signature
        f.write(b'\x52\x61\x72\x21\x1A\x07' + b'\x00' * 506)
        
        # Add some RAR data
        f.write(b'\x00' * 512)
        
        # Add another JPEG signature with different marker
        f.write(b'\xFF\xD8\xFF\xE1' + b'\x00' * 508)
        
        # Add some more image data
        f.write(b'\x00' * 512)
    
    print("Created test recovery file with multiple formats")
    
    # Clean up any previous test files
    for ext in ['.jpg', '.png', '.pdf', '.docx', '.gif', '.mp3', '.bmp', '.rar']:
        for f in glob.glob(f"[0-9][0-9][0-9]{ext}"):
            try:
                os.remove(f)
                print(f"Removed old test file: {f}")
            except:
                pass
    
    # Run recover.exe on the test file
    print("\nRunning recover.exe...")
    result = subprocess.run(['recover.exe', 'test_recovery.raw'], capture_output=True, text=True)
    print(f"Return code: {result.returncode}")
    print(f"Output: {result.stdout}")
    print(f"Error: {result.stderr if result.stderr else 'None'}")
    
    # Check if files were created
    print("\nRecovered files:")
    
    # Check for JPEG files
    jpeg_files = [f for f in os.listdir('.') if f.endswith('.jpg') and f.split('.')[0].isdigit()]
    print(f"JPEG: {len(jpeg_files)} files: {jpeg_files}")
    
    # Check for PNG files
    png_files = [f for f in os.listdir('.') if f.endswith('.png') and f.split('.')[0].isdigit()]
    print(f"PNG: {len(png_files)} files: {png_files}")
    
    # Check for PDF files
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf') and f.split('.')[0].isdigit()]
    print(f"PDF: {len(pdf_files)} files: {pdf_files}")
    
    # Check for DOCX files
    docx_files = [f for f in os.listdir('.') if f.endswith('.docx') and f.split('.')[0].isdigit()]
    print(f"DOCX: {len(docx_files)} files: {docx_files}")
    
    # Check for GIF files
    gif_files = [f for f in os.listdir('.') if f.endswith('.gif') and f.split('.')[0].isdigit()]
    print(f"GIF: {len(gif_files)} files: {gif_files}")
    
    # Check for MP3 files
    mp3_files = [f for f in os.listdir('.') if f.endswith('.mp3') and f.split('.')[0].isdigit()]
    print(f"MP3: {len(mp3_files)} files: {mp3_files}")
    
    # Check for BMP files
    bmp_files = [f for f in os.listdir('.') if f.endswith('.bmp') and f.split('.')[0].isdigit()]
    print(f"BMP: {len(bmp_files)} files: {bmp_files}")
    
    # Check for RAR files
    rar_files = [f for f in os.listdir('.') if f.endswith('.rar') and f.split('.')[0].isdigit()]
    print(f"RAR: {len(rar_files)} files: {rar_files}")
    
    # Total recovered files
    total = len(jpeg_files) + len(png_files) + len(pdf_files) + len(docx_files) + \
            len(gif_files) + len(mp3_files) + len(bmp_files) + len(rar_files)
    print(f"\nTotal recovered files: {total}")
    
    # Verify all expected formats were recovered
    success = True
    expected = {
        'JPEG': 2, 'PNG': 1, 'PDF': 1, 'DOCX': 1,
        'GIF': 1, 'MP3': 1, 'BMP': 1, 'RAR': 1
    }
    
    missing = []
    if len(jpeg_files) < expected['JPEG']: missing.append(f"JPEG (found {len(jpeg_files)}, expected {expected['JPEG']})")
    if len(png_files) < expected['PNG']: missing.append(f"PNG (found {len(png_files)}, expected {expected['PNG']})")
    if len(pdf_files) < expected['PDF']: missing.append(f"PDF (found {len(pdf_files)}, expected {expected['PDF']})")
    if len(docx_files) < expected['DOCX']: missing.append(f"DOCX (found {len(docx_files)}, expected {expected['DOCX']})")
    if len(gif_files) < expected['GIF']: missing.append(f"GIF (found {len(gif_files)}, expected {expected['GIF']})")
    if len(mp3_files) < expected['MP3']: missing.append(f"MP3 (found {len(mp3_files)}, expected {expected['MP3']})")
    if len(bmp_files) < expected['BMP']: missing.append(f"BMP (found {len(bmp_files)}, expected {expected['BMP']})")
    if len(rar_files) < expected['RAR']: missing.append(f"RAR (found {len(rar_files)}, expected {expected['RAR']})")
    
    if not missing:
        print("\nSUCCESS: All file formats were recovered correctly!")
    else:
        print("\nWARNING: Some file formats were not recovered correctly.")
        print(f"Missing or incomplete formats: {', '.join(missing)}")
        print("\nThis could be due to signature detection issues or compilation problems.")
        print("Make sure to recompile recover.c after making changes.")


if __name__ == "__main__":
    main()