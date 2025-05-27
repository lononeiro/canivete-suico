from flask import Blueprint, render_template

homeRoute = Blueprint('home', __name__)

@homeRoute.route('/')

def home():
    return render_template('index.html')