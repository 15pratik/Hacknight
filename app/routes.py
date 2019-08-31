from flask import render_template, Flask, request, redirect, url_for, jsonify
from app import app
from app.forms import DataForm
from app.prediction_model.predict import treatment_prediction 

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
        featureDict = process(request.form)
        print(request.form)
        result = treatment_prediction(featureDict)
        return render_template("result.html", prob_yes = result)

def process(formDict):
    required_keys = ['Age', 'Gender', 'Country', 'state', 'self_employed', 
                     'family_history', 'work_interfere', 'no_employees', 
                     'remote_work', 'tech_company', 'benefits', 'care_options',
                     'wellness_program', 'seek_help', 'anonymity', 'leave', 
                     'mental_health_consequence', 'phys_health_consequence', 'coworkers', 
                     'supervisor', 'mental_health_interview', 'phys_health_interview', 
                     'mental_vs_physical', 'obs_consequence', 'comments']
    featureDict = {}
    for key,val in formDict.items():
        if key in required_keys:
            featureDict[key] = [val]
    return featureDict