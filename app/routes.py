from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, ronnoc. We have come for you, as we promised we would."

