from flask import Flask,render_template,url_for,request,redirect,session
import pickle
from sklearn.ensemble import RandomForestClassifier
import sqlite3 as sql
import numpy as np
import sqlite3
import warnings
warnings.filterwarnings('ignore')

def closest(lst, K):
	
	lst = np.asarray(lst)
	idx = (np.abs(lst - K)).argmin()
	return lst[idx]


model=pickle.load(open('dataset_and_model/heart_model_new.pkl','rb'))
app = Flask(__name__) #constructor

@app.route("/") #root path
def show():
    return render_template('index.html')

@app.route("/backtohome") 
def backtohome():
    return render_template('index.html')

@app.route("/bmi") 
def bmi():
    return render_template('bmi.html')

#for BMI
@app.route('/bmi',methods=['POST','GET'])
def bmicheck():
        if request.method=="POST":
                c1=float(request.form['height'])
                c2=int(request.form['weight'])
                c3=round(c2 / (c1 * c1), 2)
                c3=str(c3)
                return render_template('bmiresult.html',c=c3)
        return render_template('BMI.html')



@app.route("/index.html",methods=["POST","GET"])
def home():
        if request.method=="POST":
            
            gender=int(request.form['gender'])
            age=int(request.form['age'])
            smoke=int(request.form["smoker"])
            cig=int(request.form["cigarette"])
            stroke=int(request.form["stroke"])
            hyp=int(request.form["prevalenthyp"])            
            dia=int(request.form["diabetes"])            
            Chol=int(request.form["totchol"])
            diaBP=int(request.form["diabp"])
            BMI=int(request.form["bmicalc"])
            sysBP=int(request.form["sysbp"])
            HR=int(request.form["hr"])
            glu=int(request.form["gr"])
            
            
            print(gender,age,smoke,cig,stroke,hyp,Chol,diaBP,BMI,sysBP,HR,glu)
            if gender ==1:
                 male=1
                 female=0
            elif gender ==0:
                 male=0
                 female=1
            else:
                 male=0
                 female=0

            print(age,smoke,cig,stroke,hyp,dia,Chol,sysBP,diaBP,BMI,HR,glu,female,male)
            yy = model.predict([[age,smoke,cig,stroke,hyp,dia,Chol,sysBP,diaBP,BMI,HR,glu,female,male]])
            print(yy)

            
            if yy[0]==1:
                return render_template('result.html')
            elif yy[0]==0:
                return render_template('result1.html')        
            
        return render_template('index.html')

@app.route("/result.html",methods=["POST","GET"])
def post():
    if request.method=="POST":
        pin_code=int(request.form['pin'])
        dbase=sqlite3.connect("static/database/Hospital_detail.db")
        con=dbase.cursor()
        con.execute("SELECT PIN_CODE FROM TAB1 ")
        data=con.fetchall()

        if data:
            data_list=[]
            for d in data:
                data_list.append(d[0])
                  
             #print(data_list)

        
        pin=closest(data_list, pin_code)
        print(pin)

        con.execute("SELECT * FROM TAB1 WHERE PIN_CODE =?",(int(pin),))
        total_data=con.fetchone()
        

        if total_data:
            print(total_data)
            print("Hospital Address:",total_data[2])
            print("Phone number:",total_data[3])
            print("Pin number:",total_data[1])
            output11=str(total_data[2])
            output12=str(total_data[3])
        data_list.remove(pin)

        pin=closest(data_list, pin_code)
        print(pin)

        con.execute("SELECT * FROM TAB1 WHERE PIN_CODE =?",(int(pin),))
        total_data=con.fetchone()


        if total_data:
            print(total_data)
            print("Hospital Address:",total_data[2])
            print("Phone number:",total_data[3])
            print("Pin number:",total_data[1])
            output21=str(total_data[2])
            output22=str(total_data[3])
        data_list.remove(pin)


        pin=closest(data_list, pin_code)
        print(pin)

        con.execute("SELECT * FROM TAB1 WHERE PIN_CODE =?",(int(pin),))
        total_data=con.fetchone()


        if total_data:
            print(total_data)
            print("Hospital Address:",total_data[2])
            print("Phone number:",total_data[3])
            print("Pin number:",total_data[1])
            output31=str(total_data[2])
            output32=str(total_data[3])
        data_list.remove(pin)
        dbase.close()



        return render_template('hospsuggest.html',r11=output11,r12=output12,r21=output21,r22=output22,r31=output31,r32=output32)


            
'''@app.route("/post")
def post():
    return "successfull"'''

if __name__=='__main__': #main function 
    app.run(debug = False)