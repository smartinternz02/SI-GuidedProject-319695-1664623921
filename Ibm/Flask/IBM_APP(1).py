from flask import Flask, request, render_template
import pickle
import json
import requests
import numpy as np
import pandas as pd

API_KEY = "_uQJaQRra2V-2lHNbQY1-q314HMfQ3Rkw1ZhkFeVDtWN"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict")
def predict():
    return render_template("predict.html")

@app.route('/output', methods = ['post','get'])
def output():
    #  reading the inputs given by the user
    input_feature= [float(x) for x in request.form.values()] 
    input_feature=[np.array(input_feature)]
    print(input_feature)
    names = ['CO2_room', 'Relative_humidity_room', 'Lighting_room', 'Meteo_Rain', 'Meteo_Wind', 'Meteo_Sun_light_in_west_facade',
       'Outdoor_relative_humidity_Sensor']
 payload_scoring = {"input_data": [{"field": [["pH","Temprature", "Taste","Odor", "Fat","Turbidity","Colour"]], "values": [[8.5,70,1,1,1,1,246]]}]}

 response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/f7293f6f-67be-4c43-9eb5-917a520bac11/predictions?version=2022-06-07', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
 print("Scoring response")
 print(response_scoring.json())
 predictions=response_scoring.json()
 
 print(predictions)
 pred=predictions['predictions'][0]['values'][0][0]

    return render_template('predict.html', prediction=prediction[0])


if __name__ == '__main__':
    app.run(debug = True)