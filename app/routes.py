from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': "Pleachy"}
    posts = [
        {
            'author': {'username': 'Twudge'},
            'body': 'Another beautiful day in Pudge Town!'
        },
        {
            'author': {'username': 'Zeddius'},
            'body': 'Just finished casting my first snowball spell!'
        },
        {
            'author': {'username': 'Ronnoc'},
            'body': 'Twice blast and confound those damnable ragamuffins! If one more of those weasels makes it into my pantry I swear on the nine i will teleport it straight to Murkmill!'
            
        }
    ]
    #return render_template('index.html', title='Home', user=user)
    return render_template('index.html', user=user, posts=posts)
    

