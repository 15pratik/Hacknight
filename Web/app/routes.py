from flask import render_template, Flask, request, redirect, url_for, jsonify
from app import app
from app.prediction_model.predict import predict

@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Anonymous'}
    return render_template('index.html', title='Home', user=user)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method=='GET':
        return render_template('userform.html', title='Home')
    if request.method=='POST':
        for k in request.form.keys():
            print(request.form)
            result = predict(request.form)
        return render_template("result.html", prob_yes = result)