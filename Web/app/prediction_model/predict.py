from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib 
import pandas as pd
import numpy as np

def treatment_prediction(input_dict):
    print("######################")
    print(input_dict.keys())
    print("######################")
    x = pd.DataFrame(input_dict)
    print(x)
    #labeling
    for col in x.columns:
        label_encoder=joblib.load('./app/prediction_model/columns/' + col)
        x[col]=label_encoder.fit_transform(x[col])

    # Load the model from the file 
    trained_model = joblib.load('./app/prediction_model/prediction.model')

    # Use the loaded model to make predictions 
    y_pred = trained_model.predict(x)
    return y_pred, trained_model.predict_proba(x)

if __name__ == '__main__':
    input_dict = {'Age':[25],'Gender':['Male'],'Country':['United States'],'state':['PA'],'self_employed':['No'],'family_history':['Yes'],'work_interfere':['Often'],'no_employees':['6-25'],'remote_work':['Yes'],'tech_company':['Yes'],'benefits':['Yes'],'care_options':['Yes'],'wellness_program':['No'],'seek_help':["Don't know"],'anonymity':['Yes'],'leave':['Somewhat easy'],'mental_health_consequence':['No'],'phys_health_consequence':['No'],'coworkers':['Yes'],'supervisor':['Yes'],'mental_health_interview':['Maybe'],'phys_health_interview':['Maybe'],'mental_vs_physical':["Don't know"],'obs_consequence':["No"],'comments':[""]}
    print(treatment_prediction(input_dict))