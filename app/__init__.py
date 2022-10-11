from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '46c56fa19d9512b024d20d477795053a48c1c731'
app.static_folder = 'static'
app.config.from_object('app.config_main')

from app import routes
