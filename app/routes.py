from flask import render_template, Flask, request, redirect, url_for, jsonify
from app import app
from app.forms import DataForm
from app.prediction_model.predict import treatment_prediction
import requests 
from pprint import pprint as pp
import json
import math

medic_url =  "https://hooks.slack.com/services/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"
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
    for k in required_keys:
        default = "No"
        if k == 'Age':
            default = "21"
        featureDict[k] = [featureDict.get(k, default)]
    return featureDict

@app.route('/api/getEmpData', methods=['POST'])
def getEmpdata():
    print("###REQUEST####")
    pp(request.__dict__)
    print("#####PRINTED#########")
    pp(process(request.get_json()))
    prob_yes = treatment_prediction(process(request.get_json()))[0]
    print(prob_yes)
    print('####POSTING TO SLACK#####')
    post_to_hr(request.get_json(),prob_yes)
    print('####DONE#####')
    return jsonify({'yes': prob_yes}), 201

def post_to_hr(dataEmp, prob_yes):
    pronoun = "She"
    if dataEmp["Gender"] == "Male":
        pronoun = "He"
    emoji = ":white_check_mark:"
    if prob_yes <0.5:
        emoji = ":exclamation:"
    data =  {
    "text": "Hey, the following employee might be in need of some psychological help.",
    "attachments": [
        {
            "title": "ID : {}".format(dataEmp['id']),
            "fields": [
                {
                    "title": "Age",
                    "value": dataEmp['Age'],
                    "short": True
                },
                {
                    "title": "Gender",
                    "value": dataEmp["Gender"],
            "short": True
                }
            ],
            "author_name": dataEmp["name"]
        },
        {
            "title": "{} says".format(pronoun),
            "text": dataEmp['comment']
        },
        {
            "title" : "I am {}% sure that this is a genuine request.".format(math.ceil(prob_yes*100)) + emoji
        },
        {
            "fallback": "Would you recommend {} take a medical leave?".format(pronoun.lower),
            "title": "Would you recommend {} take a medical leave?".format(pronoun.lower()),
            "callback_id": "comic_1234_xyz",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "recommend",
                    "text": "Recommend",
                    "type": "button",
                    "value": "recommend"
                },
                {
                    "name": "no",
                    "text": "No",
                    "type": "button",
                    "value": "bad"
                }
            ]
        }
    ]
}
    response = requests.post(medic_url, data=json.dumps(
        data), headers={'Content-Type': 'application/json'})

    pp(response)
"""
{
	            "type": "block_actions",
	            "team": {
		            "id": "T0CAG",
		            "domain": "acme-creamery"
	            },
	            "user": {
		            "id": "U0CA5",
		            "username": "Amy McGee",
		            "name": "Amy McGee",
		            "team_id": "T3MDE"
	            },
	            "api_app_id": "A0CA5",
	            "token": "Shh_its_a_seekrit",
	            "container": {
		            "type": "message",
		            "text": "The contents of the original message where the action originated"
	            },
                "trigger_id": "12466734323.1395872398",
                "response_url": "https://www.postresponsestome.com/T123567/1509734234",
                "actions": [
                            {
                                "type": "button",
                                "block_id": "rNFxy",
                                "action_id": "JKe",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Approve",
                                    "emoji": True
                                },
                                "value": "click_me_123",
                                "style": "primary",
                                "action_ts": "1567295645.162176"
                            }
                        ]
            }
"""