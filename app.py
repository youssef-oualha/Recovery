from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/recover', methods=['POST'])
def recover():
    file = request.files['file']
    file.save('temp_image')
    result = subprocess.run(['recover.exe', 'temp_image'], capture_output=True, text=True)
    
    # Count recovered JPEG files
    recovered_files = [f for f in os.listdir('.') if f.endswith('.jpg') and f.split('.')[0].isdigit()]
    
    return render_template('success.html', filename=file.filename, count=len(recovered_files))

if __name__ == '__main__':
    app.run(debug=True)