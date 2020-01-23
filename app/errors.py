from flask import render_template
from app import app, db

"""
The error function works similarly to view functions. For these
two errors we are returning the contents of their respective templates.
Both functions return a second value after the template which is
the error code number. For our other view functions we didn't need to
do this because the default of 200(successful response code) is what
we wanted. Since these are error pages we wan the status code of the
response to reflect the error.
"""
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


"""
this error can be invoked after a database error,
which is the case with our username duplication error. To make
sure that failed database sessions do not interefere with any
database accesses trigered by the template, we issue a
session rollback, resetting the session to a clean state.
"""
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
