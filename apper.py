from flask import Flask
from search_app import search_bp  # Import the blueprint

app = Flask(__name__)
app.register_blueprint(search_bp)  # Register the blueprint

if __name__ == '__main__':
    app.run(debug=True)
