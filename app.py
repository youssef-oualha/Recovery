from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os
import glob

app = Flask(__name__)

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/recover', methods=['POST'])
def recover():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    # Save the uploaded file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.raw')
    file.save(filepath)
    
    # Run the recovery program
    try:
        subprocess.run(['recover.exe', filepath], check=True)
        
        # Count recovered files by type
        file_counts = {
            'jpeg': len(glob.glob("[0-9][0-9][0-9].jpg")),
            'png': len(glob.glob("[0-9][0-9][0-9].png")),
            'pdf': len(glob.glob("[0-9][0-9][0-9].pdf")),
            'docx': len(glob.glob("[0-9][0-9][0-9].docx")),
            'gif': len(glob.glob("[0-9][0-9][0-9].gif")),
            'mp3': len(glob.glob("[0-9][0-9][0-9].mp3")),
            'bmp': len(glob.glob("[0-9][0-9][0-9].bmp")),
            'rar': len(glob.glob("[0-9][0-9][0-9].rar"))
        }
        
        total_files = sum(file_counts.values())
        
        return render_template('success.html', 
                               file_counts=file_counts,
                               total_count=total_files)
    except Exception as e:
        return render_template('upload.html', error=f"An error occurred during recovery: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)