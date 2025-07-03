import subprocess
import os

def main():
    # Create a simple test file with JPEG signatures
    with open('test_image.raw', 'wb') as f:
        # Create some random data
        f.write(b'\x00' * 512)
        
        # Add a JPEG signature
        f.write(b'\xFF\xD8\xFF\xE0' + b'\x00' * 508)
        
        # Add some image data
        f.write(b'\x00' * 512)
        
        # Add another JPEG signature
        f.write(b'\xFF\xD8\xFF\xE1' + b'\x00' * 508)
        
        # Add some more image data
        f.write(b'\x00' * 512)
    
    print("Created test image file")
    
    # Run recover.exe on the test file
    print("Running recover.exe...")
    result = subprocess.run(['recover.exe', 'test_image.raw'], capture_output=True, text=True)
    print(f"Return code: {result.returncode}")
    print(f"Output: {result.stdout}")
    print(f"Error: {result.stderr}")
    
    # Check if files were created
    recovered_files = [f for f in os.listdir('.') if f.endswith('.jpg') and f.split('.')[0].isdigit()]
    print(f"Recovered {len(recovered_files)} files: {recovered_files}")

if __name__ == "__main__":
    main()