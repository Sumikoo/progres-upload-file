#6C /19090075 /Nur Khafidah
#6D /19090133 /Helina Putri


# import library
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import datetime, os


# Inisialisasi
database_file = 'sqlite:///database/files.db'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = 'dump'
app.config['UPLOAD_EXTENSIONS'] = ['zip','pdf','doc','docx','xls','xlsx','ppt','pptx','mp4','mkv','jpg', 'jpeg', 'png', 'gif']
db = SQLAlchemy(app)


# DATABASE
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    timeStamp = db.Column(db.DateTime)

db.create_all()

def validate_img(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_EXTENSIONS']

# http://127.0.0.1:4000/api/v1/upload/file
@app.route('/api/v1/upload/file', methods=["POST"])
def upImage():
    upfile = request.files['file']
    time = datetime.datetime.utcnow()
    if upfile and validate_img(upfile.filename):
        filename = secure_filename(upfile.filename)
        upfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        gambar = Image(name=upfile.filename, timeStamp=time)
        db.session.add(gambar)
        db.session.commit()
        return jsonify({"msg": "Upload File Successful !", "name":filename, "time":time})
    return jsonify({"msg": "Upload File Failed !"})

if __name__ == '__main__':
   app.run(debug = True, port=4000)