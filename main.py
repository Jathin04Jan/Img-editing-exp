from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import MultiDict 
import os
from imageProcessing import imagOperation
from deleting import delete_files_in_directory
import zipfile
from flask import send_file,Flask,send_from_directory

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webg', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    delete_files_in_directory('uploads')
    delete_files_in_directory('static')
    delete_files_in_directory('zipFile')
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("aboutPage.html")

@app.route("/edit", methods = ["GET", "POST"])
def edit():
    if request.method == 'POST':
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        
        firstFile = request.files['file']
        fileList = request.files.getlist('file')

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if firstFile.filename == '':
            flash('No selected file')
            return "No file selected"
        
        if firstFile and allowed_file(firstFile.filename):

            for item in fileList:
                file = item.filename
                filename = secure_filename(file)
                item.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new = imagOperation(filename, operation)
                flash(f"Your image is processed and is avaible <a href= '/{new}' target= '_blank'> here </a>")

            flash(f"Folder Path <a href= '/static' target= '_blank'> click Me </a>")
            return render_template("ThankyouPage.html")
    
    return render_template("ThankyouPage.html")

@app.route('/download_files')
def download_all():
    # Zip file Initialization and you can change the compression type
    zipfolder = zipfile.ZipFile('zipFile/ProcessedImages.zip','w', compression = zipfile.ZIP_STORED)

    # zip all the files which are inside in the folder
    for root,dirs, files in os.walk('static'):
        for file in files:
            zipfolder.write('static/'+file)
    zipfolder.close()

    return send_file('zipFile/ProcessedImages.zip',
            mimetype = 'zip',
            download_name= 'zipFile/ProcessedImages.zip',
            as_attachment = True)


#app.run()
