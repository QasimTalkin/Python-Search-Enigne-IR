from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
 
# App config.
app = Flask(__name__)
app.secret_key = "super secret key"

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
 
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
 
    print (form.errors)
    if request.method == 'POST':
        name=request.form['name']
        print (name)
    
    if form.validate():
        # Save the comment here.
        flash('Hello ' + name)
    else:
        flash('All the form fields are required. ')
    
    return render_template('hello.html', form=form)
 
if __name__ == "__main__":
    app.run()