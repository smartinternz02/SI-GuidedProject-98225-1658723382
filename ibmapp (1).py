# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 21:44:40 2022

@author: Divya
"""
import requests
import numpy as np
import pandas as pd

import pickle

from flask import Flask, request, render_template

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "bhpZeKLeybwIIT6Nme6huKn_h6xW2w2FhM7JdMAydnBO"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
app=Flask(__name__)
model = pickle.load(open(r"C:\Users\Divya\Desktop\Project\HDI.pkl",'rb'))

@app.route('/', methods=['GET'])

def index():

    return render_template("home.html")

@app.route('/home.html', methods=['GET'])
def about():
    return render_template("home.html")
@app.route('/index', methods=['GET'])
def page():
    return render_template("index.html")

@app.route('/resultnew', methods=['POST'])
def predict():

   
     Country=request.form["Country"]
     le=request.form['Life expectancy']
     mn=request.form['Mean years of schooling']
     gni=request.form['Gross national income (GNI) per capita']
     internet=request.form['Internet users']
     if(Country=="Afganistan"):
         Country=0
     if(Country=="Australia"):
         Country=8
     if(Country=="Bangladesh"):
         Country=13
     if(Country=="Canada"):
         Country=31
     if(Country=="India"):
         Country=76
     if(Country=="Poland"):
         Country=138
     if(Country=="Turkey"):
          Country=179
    # predictions using the loaded model file
     t=[[int(Country),int(le),int(mn),int(gni),int(internet)]]
     payload_scoring = {"input_data": [{"field":['Country','Life expectancy','Mean years of schooling','Gross national income (GNI) per capita','Internet Users'], "values":t}]}

     response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/853cb825-d423-40e8-920e-dcc3e40c532f/predictions?version=2022-08-17', json=payload_scoring,
     headers={'Authorization': 'Bearer ' + mltoken})
     print("Scoring response")
     print(response_scoring.json())

     prediction=response_scoring.json()

     output=prediction["predictions"][0]["values"][0][0]
    # print(type(output))
     y_pred =output
     #if(y_pred >= 0.3 and y_pred <= 0.4) :
      #  return render_template(r"resultnew.html",prediction_text = 'Low HDI'+ str(y_pred))
     #elif(y_pred >= 0.4 and y_pred <= 0.7) :
       # return render_template(r"resultnew.html",prediction_text = 'Medium HDI '+str(y_pred))
    # elif(y_pred >= 0.7 and y_pred <= 0.8) :
       # return render_template(r"resultnew.html",prediction_text = 'High HDI'+str(y_pred))
     #elif(y_pred >= 0.8 and y_pred <= 0.94) :
      #  return render_template(r"resultnew.html",prediction_text = 'Very High HDI'+str(y_pred))
    # else :
       # return render_template(r"resultnew.html",prediction_text = 'The given values do not match the range of values of the model.Try giving the values in the mnetioned range'+str(y_pred))
    
    
    # showing the prediction results in a UI# showing the prediction results in a UI
     return render_template(r'resultnew.html', prediction_text=output)

if __name__=='__main__':

    app.run(debug=False)
