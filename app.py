# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 23:02:50 2022

@author: kvssn
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 20:06:54 2022

@author: kvssn
"""

import numpy as np
import pandas as pd

import pickle

from flask import Flask, request, render_template

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

    input_features = [int(x) for x in request.form.values()] 
    features_value = [np.array(input_features)]

    features_name = ['Country','Life expectancy','Mean years of schooling','Gross national income (GNI) per         capita','Internet Users']
    df = pd.DataFrame(features_value, columns=features_name)
    
    # predictions using the loaded model file
    output = model.predict(df)
    print(round(output[0][0],2))
    print(type(output))
    y_pred =round(output[0][0],2)
    if(y_pred >= 0.3 and y_pred <= 0.4) :
        return render_template("resultnew.html",prediction_text = 'Low HDI'+ str(y_pred))
    elif(y_pred >= 0.4 and y_pred <= 0.7) :
        return render_template("resultnew.html",prediction_text = 'Medium HDI '+str(y_pred))
    elif(y_pred >= 0.7 and y_pred <= 0.8) :
        return render_template("resultnew.html",prediction_text = 'High HDI'+str(y_pred))
    elif(y_pred >= 0.8 and y_pred <= 0.94) :
        return render_template("resultnew.html",prediction_text = 'Very High HDI'+str(y_pred))
    else :
        return render_template("resultnew.html",prediction_text = 'The given values do not match the range of values of the model.Try giving the values in the mnetioned range'+str(y_pred))
    
    
    # showing the prediction results in a UI# showing the prediction results in a UI
    return render_template('resultnew.html', prediction_text=output)

if __name__=='__main__':

    app.run(debug=False)
