from flask import Flask
from routes.home import homeRoute
from routes.video import videoRoute

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.register_blueprint(homeRoute)
app.register_blueprint(videoRoute, url_prefix='/video')

if __name__ == '__main__':
    app.run(debug=True)