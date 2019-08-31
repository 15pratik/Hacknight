from flask import render_template, Flask, request, redirect, url_for, jsonify
from app import app
from app.forms import DataForm
#from app.prediction_model.predict import predict

@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Anonymous'}
    return render_template('index.html', title='Home', user=user)

@app.route('/forms', methods=['GET', 'POST'])
def forms():
    form = DataForm()
    if request.method=='GET':
        return render_template('dataform.html', title='Form', form=form)
    if request.method=='POST':
        for k in request.form.keys():
            print(request.form)
            result = 0.75#predict(request.form)
        return render_template("result.html", prob_yes = result)