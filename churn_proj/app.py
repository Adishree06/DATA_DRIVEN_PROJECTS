from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
import matplotlib
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import sqlite3 
from sqlalchemy import create_engine, text
from flask import Flask, redirect, url_for, render_template, request




app = Flask(__name__)

engine = create_engine("sqlite:////Users/adishreepandey/Desktop/ADISHREE/F2022/churn_proj/churn.db", echo = True)



model = pickle.load(open('Customer_Churn_Prediction.pkl', 'rb'))
@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')

standard_to = StandardScaler()
@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        int_features = []
        creditScore = int(request.form['CreditScore'])
        age = int(request.form['Age'])
        tenure = int(request.form['Tenure'])
        balance = float(request.form['Balance'])
        numOfProducts = int(request.form['NumOfProducts'])
        hasCrCard = int(request.form['HasCrCard'])
        isActiveMember = int(request.form['IsActiveMember'])
        estimatedSalary = float(request.form['EstimatedSalary'])
        geography_Germany = request.form['Geography_Germany']
        if(geography_Germany == 'Germany'):
            geography_Germany = 1
            geography_Spain= 0
            geography_France = 0
                
        elif(geography_Germany == 'Spain'):
            geography_Germany = 0
            geography_Spain= 1
            geography_France = 0
        
        else:
            geography_Germany = 0
            geography_Spain= 0
            geography_France = 1
        gender_Male = request.form['Gender_Male']
        if(gender_Male == 'Male'):
            gender_Male = 1
            gender_Female = 0
        else:
            gender_Male = 0
            gender_Female = 1
        prediction = model.predict([[creditScore,age,tenure,balance,numOfProducts,hasCrCard,isActiveMember,estimatedSalary,geography_Germany,geography_Spain,gender_Male]])
        if prediction==1:
             return render_template('index.html',prediction_text="The Customer will leave the bank")
    

        else:
            print(prediction)
            int_features.append([prediction,  creditScore,  age, tenure, balance, numOfProducts, hasCrCard,isActiveMember, estimatedSalary ])
            connection=sqlite3.connect("churn.db")
            cursor=connection.cursor()

            q = "INSERT INTO Churn_Modelling VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"


            r_set = cursor.execute(q,tuple(int_features))
            return render_template('index.html',prediction_text="Customer will not leave the  {} Bank".format(prediction))

    ##else:

        ##return render_template('index.html')

##########################################






if __name__=="__main__":
    app.run(debug=True)
