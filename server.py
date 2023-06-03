from flask_app import app
from flask_app.controllers import userController, videoController, paymentController
from flask import Flask

if __name__ == '__main__':
    app.run(debug = True, port = 4242)

# sudo systemctl daemon-reload


