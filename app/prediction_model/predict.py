from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib 
import pandas as pd
import numpy as np

def transform(label_encoder, data_list):
    """
    This will transform the data_list to id list where the new values get assigned to Unknown class
    :param data_list:
    :return:
    """
    new_data_list = list(data_list)
    for unique_item in np.unique(data_list):
        if unique_item not in label_encoder.classes_:
            new_data_list = ['Unknown' if x==unique_item else x for x in new_data_list]
            # print("Unknown {}".format(unique_item))
            # print(label_encoder.classes_)

    return label_encoder.transform(new_data_list)

def treatment_prediction(input_dict):
    print("######################")
    print(input_dict.keys())
    print("######################")
    x = pd.DataFrame(input_dict)
    print(x)
    #labeling
    for col in x.columns:
        label_encoder=joblib.load('./app/prediction_model/columns/' + col)
        x[col]=transform(label_encoder, x[col])

    # Load the model from the file 
    trained_model = joblib.load('./app/prediction_model/prediction.model')

    # # Use the loaded model to make predictions 
    # y_pred = trained_model.predict(x)
    return trained_model.predict_proba(x)[:,1]

if __name__ == '__main__':
    input_dict = {'Age':['25'],'Gender':['M'],'Country':['United States'],'state':['PA'],'self_employed':['No'],'family_history':['No'],'work_interfere':['Often'],'no_employees':['More than 1000'],'remote_work':['Yes'],'tech_company':['Yes'],'benefits':['No'],'care_options':['Yes'],'wellness_program':['No'],'seek_help':["Don't know"],'anonymity':['No'],'leave':['Somewhat easy'],'mental_health_consequence':['No'],'phys_health_consequence':['No'],'coworkers':['Yes'],'supervisor':['No'],'mental_health_interview':['Yes'],'phys_health_interview':['Maybe'],'mental_vs_physical':["Don't know"],'obs_consequence':["No"],'comments':[""]}
    print(treatment_prediction(input_dict))
