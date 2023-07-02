from flask import Flask,render_template,request,flash
from werkzeug.utils import secure_filename
import os
import cv2
app = Flask(__name__)
app.secret_key = "super secret key"
ALLOWED_EXTENSIONS = ['jpg','png','webp']
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def processimage(filename):
    img = cv2.imread(f'C:/Users/dasar/OneDrive/Desktop/Flask Tutorials/static/uploads/{filename}')
    grey_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(grey_img)
    blur = cv2.GaussianBlur(invert,(21,21),0)
    invertedblur = cv2.bitwise_not(blur)
    sketch = cv2.divide(grey_img,invertedblur,scale=256.0)
    cv2.imwrite(f"C:/Users/dasar/OneDrive/Desktop/Flask Tutorials/static/images/{filename}",sketch)




@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/edit",methods = ['GET','POST'])
def edit():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return 'error'
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return 'no file selected'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('C:/Users/dasar/OneDrive/Desktop/Flask Tutorials/static/uploads',filename))
            processimage(filename)
            flash(f"Your image is Processed and Download <a href = '/static/images/{filename}' target='_blank'>here</a>")
            return render_template('index.html')
    return render_template('index.html')
app.run(debug=True)


