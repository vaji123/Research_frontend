import os
import pandas as pd 
import numpy as np 
import flask
import pickle
from flask import Flask, render_template, request
import requests
app=Flask(__name__)
@app.route('/')
def index():
 return flask.render_template('CarUserHome.html')
# def ValuePredictor(to_predict_list):
#  to_predict = np.array(to_predict_list).reshape(1,4)
#  loaded_model = pickle.load(open("model.pkl","rb"))
#  result = loaded_model.predict(to_predict)
#  return result[0]


 
def PassValuePredictor1(id):
        url = 'https://0d8p49x2jb.execute-api.ap-south-1.amazonaws.com/ch/carforward'
        url2 = 'https://0d8p49x2jb.execute-api.ap-south-1.amazonaws.com/ch/carbackwardall'

        r = requests.get(url)
        r2 = requests.get(url2)
        json = r.json()
        json2 = r2.json()
        dataframe = pd.DataFrame.from_dict(json, orient="columns")
        dataframe=dataframe.loc[dataframe.Activity=='Forward',:]
        dataframe=dataframe.loc[dataframe.cid==id,:]

        dataframe2 = pd.DataFrame.from_dict(json2, orient="columns")
        dataframe2=dataframe2.loc[dataframe2.Activity=='Forward',:]
        dataframe2=dataframe2.loc[dataframe2.cid==id,:]
        # max  
        df1=dataframe.groupby('cid')[['nRotations1', 'nRotations2']].max()
        # max  
        df2=dataframe2.groupby('cid')[['nRotations3', 'nRotations4']].max()
        x = pd.concat([df1, df2], axis=1, join='outer')

        list=x.values.tolist()
        ro1=list[0][0]
        ro2=list[0][1]
        ro3=list[0][2]
        ro4=list[0][3]
        list2=[ro1,ro2,ro3,ro4]
 

        to_predict = np.array(list2).reshape(1,4)
        loaded_model = pickle.load(open("model.pkl","rb"))
        result = loaded_model.predict(to_predict)
        return result[0]

        



        

# def ValuePredictor1(list2):
#  to_predict = np.array(list2).reshape(1,4)
#  loaded_model = pickle.load(open("model.pkl","rb"))
#  result = loaded_model.predict(to_predict)
#  return result[0]







@app.route('/CarUser',methods = ['POST'])
def resultCar():
 if request.method == 'POST':
    id = request.form.get("id")
     
    result = PassValuePredictor1(id)
     
    if float(result) == 1:
            prediction='Typical Child'
    elif float(result) == 0:
            prediction='Model Suggested Child as an atypicl child.'
       
            
    return render_template("result.html",prediction=prediction)
if __name__ == "__main__":
 app.run(debug=True)