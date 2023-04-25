from flask import Flask
from exts import db
from blueprints.auth import bp as auth_bp
from blueprints.history import bp as hist_bp
from blueprints.retrosys import bp as retro_bp


app = Flask(__name__)
app.secret_key = "abcdefg"

app.register_blueprint(auth_bp)
app.register_blueprint(hist_bp)
app.register_blueprint(retro_bp)


if __name__ == '__main__':
    app.run(debug=True)