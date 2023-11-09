from flask import Flask

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/data/img/user'
app.config['DATASET_FOLDER'] = 'app/data/img/dataset'

from app import views
