from flask import Flask
from routes.home import homeRoute
from routes.video import videoRoute
from routes.encurtador import encurtadorRoute

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.register_blueprint(homeRoute)
app.register_blueprint(videoRoute, url_prefix='/video')
app.register_blueprint(encurtadorRoute, url_prefix='/encurtador')




if __name__ == '__main__':
    app.run(debug=True)