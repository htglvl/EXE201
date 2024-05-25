from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename, safe_join
import os
from io import BytesIO
from glob import glob
from zipfile import ZipFile
from transflow.pipeline import main
import shutil
from transflow.modules.utils import *

app = Flask(__name__)

# This is the path to the upload directory
if not os.path.exists("uploads"):
    os.makedirs("uploads")

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['PROCESSED_FOLDER'] = 'processed/'
app.config['ARCHIVED'] = 'archived/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def rename_files(folder_path): # IMPLEMENT YOUR OWN PROCESSING FUNCTION 
    # List all files in the specified folder
    files = os.listdir(folder_path)

    # # Rename files to cardinal numbers
    for i, filename in enumerate(files):
        _, extension = os.path.splitext(filename)
        new_filename = f"{i + 1}{extension}"
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))

    parser = get_parser()
    args = parser.parse_args(['--image', app.config['UPLOAD_FOLDER'], '--output', app.config['PROCESSED_FOLDER']])
    main(args)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/mainframe')
def mainframe():
    return render_template('MainFrame.html')

@app.route('/mainframe', methods = ['POST'])
def upload_files():
    files = request.files.getlist("file[]")
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Rename files to cardinal numbers
    rename_files(app.config['UPLOAD_FOLDER'])
    
    return redirect(url_for('process_uploads'))

@app.route('/process_uploads')
def process_uploads():
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    # file_count = len(uploaded_files)
    return render_template('process_uploads.html', files=uploaded_files)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    archive_path = os.path.join(app.config['ARCHIVED'], filename)
    if os.path.exists(file_path):
        os.replace(file_path, archive_path)
    return redirect(url_for('process_uploads'))

# Then, within your view function:
@app.route('/view_file/<filename>')
def view_file(filename):
    safe_filename = secure_filename(filename)
    file_path = safe_join(app.config['PROCESSED_FOLDER'],'final', safe_filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return 'File not found', 404
    
@app.route('/download', methods=['POST'])
def download():
    with ZipFile('translated.zip', 'w') as zipf:
        for root, dirs, files in os.walk(os.path.join(app.config['PROCESSED_FOLDER'], 'final')):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), 'translated.zip'))
    return send_file('translated.zip', as_attachment=True)

@app.route('/delete_upload', methods=['GET', 'POST'])
def delete_upload():
    print("move")
    try:
     files = os.listdir(app.config['UPLOAD_FOLDER'])
     for file in files:
       file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
       archive_path = os.path.join(app.config['ARCHIVED'], file)
       if os.path.isfile(file_path):
         os.replace(file_path, archive_path)
        #  os.remove(file_path)
     print("All files moved successfully.")
    except OSError:
     print("Error occurred while moving files.")
    clear_folder(app.config['PROCESSED_FOLDER'])
    # Code for the function you want to trigger goes here
    # For example, you can render a template
    return redirect(url_for('index'))

def clear_folder(folder_path):
    """
    Clear all items inside the specified folder.

    Parameters:
    folder_path (str): Path to the folder to be cleared.
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder {folder_path} does not exist.")
    
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"The path {folder_path} is not a directory.")

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Remove the file or link
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove the directory and its contents
        except Exception as e:
            print(f"Failed to delete {item_path}. Reason: {e}")

if __name__ == '__main__':
    clear_folder(app.config['UPLOAD_FOLDER'])
    clear_folder(app.config['PROCESSED_FOLDER'])
    app.run() 
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5000)