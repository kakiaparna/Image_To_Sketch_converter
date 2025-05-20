import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from utils.sketch_converter import convert_to_sketch

app = Flask(__name__)
app.secret_key = "image_to_sketch_secret_key"

# Configure upload and output folders
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If user does not select file, browser also submits an empty part
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Get sketch conversion parameters
            sketch_type = request.form.get('sketch_type', 'pencil')
            
            # Process the image to create a sketch
            output_filename = f"sketch_{filename}"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            convert_to_sketch(file_path, output_path, sketch_type)
            
            # Return result page
            return render_template('result.html', 
                                  original_image=f"{UPLOAD_FOLDER}/{filename}",
                                  sketch_image=f"{OUTPUT_FOLDER}/{output_filename}")
    
    return render_template('index.html')


@app.route('/shutdown', methods=['GET'])
def shutdown():
    if request.remote_addr == '127.0.0.1':
        func = request.environ.get('werkzeug.server.shutdown')
        if func is not None:
            func()
        return 'Server shutting down...'
    return 'Unauthorized', 403

if __name__ == '__main__':
    app.run(debug=True)
