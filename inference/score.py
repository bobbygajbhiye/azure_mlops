import os
import joblib

import json
import traceback


def init():
    '''
    Initialize required models:
        Get the IRIS Model from Model Registry and load
    '''
    global cv
    global model
    cv_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'models', 'cv_model.pkl')
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'models', 'spam_model.pkl')
    model = joblib.load(model_path)
    print('SPAM model loaded...')

def create_response(predicted_lbl):
    '''
    Create the Response object
    Arguments :
        predicted_label : Predicted IRIS Species
    Returns :
        Response JSON object
    '''
    resp_dict = {}
    print("Predicted Species : ",predicted_lbl)
    resp_dict["predicted_species"] = str(predicted_lbl)
    return json.loads(json.dumps({"output" : resp_dict}))

def run(raw_data):
    '''
    Get the inputs and predict the IRIS Species
    Arguments : 
        raw_data : SepalLengthCm,SepalWidthCm,PetalLengthCm,PetalWidthCm
    Returns :
        Predicted IRIS Species
    '''
    try:
        data = json.loads(raw_data)
        sepal_l_cm = data['SepalLengthCm']
        sepal_w_cm = data['SepalWidthCm']
        petal_l_cm = data['PetalLengthCm']
        petal_w_cm = data['PetalWidthCm']
        predicted_species = model.predict([[sepal_l_cm,sepal_w_cm,petal_l_cm,petal_w_cm]])[0]
        return create_response(predicted_species)
    except Exception as err:
        traceback.print_exc()