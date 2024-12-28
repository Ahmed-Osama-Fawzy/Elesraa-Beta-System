from flask import Flask, jsonify, render_template, request
from Database import SQLiteDB as DB

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html' , title="Home")

@app.route('/MaterialControling', methods= ["POST" ,"GET"])
def MaterialControling():
    TheMessage = ["" , True]
    if request.method == "POST":
        Title = request.form.get("Title").strip()
        Field = request.form.get("Field")
        High = float(request.form.get("High"))
        Mid = float(request.form.get("Mid"))
        Low = float(request.form.get("Low"))
        Duplicate = True if request.form.get("Duplicate") else False
        db = DB("System.db")
        db.connect()
        Finded = db.fetchone(f"SELECT * FROM Materials WHERE Title = '{Title}'")
        TheMessage = []
        if Finded:
            if Duplicate:
                Updates = []
                Updates.append(db.update(f"UPDATE Materials SET Field = '{Field}' WHERE Title = '{Title}'"))
                Updates.append(db.update(f"UPDATE Materials SET High = {High} WHERE Title = '{Title}'"))
                Updates.append(db.update(f"UPDATE Materials SET Mid = {Mid} WHERE Title = '{Title}'"))
                Updates.append(db.update(f"UPDATE Materials SET Low = {Low} WHERE Title = '{Title}'"))
                if False in Updates:
                    TheMessage = ["This Item Have Been Inserted Before, Wont Update It, Data Have Error", False]
                else:
                    TheMessage = ["This Item Have Been Inserted Before, Updated It", True]
            else:
                TheMessage = ["This Item Have Been Inserted Before, Wont Update It", False]
        else:
            Added = db.insert(f"INSERT INTO Materials VALUES('{Title}', '{Field}' , {High}, {Mid}, {Low})")
            TheMessage = ["Item Have Been Added Succes" if Added else "Item Havenot Been Added Succes", True if Added else False]
        db.close()
    return render_template('Material Controling.html' , title="Material Controling", TheMessage= TheMessage[0], Status=TheMessage[1] )

@app.route('/MaterialsExplore')
def MaterialsExplore():
    db = DB("System.db")
    db.connect()
    data = db.fetchall("SELECT * FROM Materials")
    db.close()
    matrix = []
    for row in data:
        newlist = []
        for val in row.values():
            newlist.append(val)
        matrix.append(list(enumerate(newlist)))
    return render_template('Materials Explore.html' , title="Materials Explore", data=list(enumerate(matrix)))

def AllData():
    db = DB("System.db")
    db.connect()
    data = db.fetchall("SELECT * FROM Materials")
    db.close()
    matrix = []
    for row in data:
        newlist = []
        for val in row.values():
            newlist.append(val)
        matrix.append(list(enumerate(newlist)))
        newdata = list(enumerate(matrix))
    return newdata

@app.route('/WindowsDiscounts', methods= ["POST" ,"GET"])
def WindowsDiscounts():
    if request.method == "POST":
        Title = request.form.get("Title")
        Data = request.get_json()
        print(Data)
    return render_template('Windows Discounts.html' , title="Windows Discounts", data=AllData())

if __name__  == "__main__":
    app.run(debug=True)