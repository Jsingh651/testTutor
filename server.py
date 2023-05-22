from flask_app import app
from flask_app.controllers import userController, videoController
from flask import Flask

if __name__ == '__main__':
    app.run(debug = True, port = 5031)

# sudo systemctl daemon-reload


