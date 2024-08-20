
from flask_app import app
from flask import Flask, redirect, session, render_template, flash, request
from markupsafe import Markup

from flask_app.models.videos import Video

@app.route('/showvid')
def showVid():
    return render_template('showvid.html', videos=Video.get_all())

