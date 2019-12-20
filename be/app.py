import os
import sys
from flask import Flask
# from be.view import auth # pytest
from view import auth 
# import db
app = Flask(__name__)
@app.route('/')
def homepage():
    return "please give url like login or register to buy some books."

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

if __name__ == '__main__':
    app.register_blueprint(auth.bp)
    app.run()
