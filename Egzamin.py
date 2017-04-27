from flask import Flask, jsonify, abort, make_response, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import sqlite3
import hashlib
import os


UPLOAD_FOLDER = '/home/piotrek/py/Egzamin/pliki'
ALLOWED_EXTENSIONS  =set(['txt','pdf','png','jpg','jpeg','gif', 'zip', 'xls','xlsx'])


app = Flask(__name__)


@app.route('/get/<string:nazwa>', methods=['GET'])
def getPlik(nazwa):
  return send_file(UPLOAD_FOLDER+'/'+nazwa);

@app.route('/')
def indeks():
  return '''
<!doctype html>
<title>Egzamin testowy</title>
<h1>Pliki:<h1>
<p>
<a href="get/wyniki.txt">wyniki.txt</a><br>
<a href="get/zadanie.doc">zadanie.doc</a><br>
</p>

<br>
<p>
<a href="/fileput">Wyslij wynik</a>
<p>
'''


def allowed_file(filename):
  return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/fileput', methods=['GET','POST'])
def upload_file():
  if request.method == 'POST':
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save( os.path.join(app.config['UPLOAD_FOLDER'], filename))
#      return redirect(url_for('uploaded_file', filename = filename))
      print('ok')
  return '''
  <!doctype html>
  <title>Dodaj plik</title>
  <h1>Dodaj plik</h1>
  <form method=post enctype=multipart/form-data>
  <p><input type=file name=file>
  <input type=submit value=Upload>
  </form>
  '''



@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)







#app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
