#type:ignore
from flask import Flask,request,json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__) #instatiate the app

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///hello.db"

db=SQLAlchemy(app)
ma=Marshmallow(app)

class Schema(ma.Schema):
    class Meta:
        fields=('id',"name","age")

user=Schema()
users=Schema(many=True)

class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    age=db.Column(db.Integer)

    def __init__(self, name,age):
        self.name=name
        self.age=age



@app.route("/")
def index():

    return "hello world"

@app.post("/add")
def adduser():
    usr=request.json()
    user=Users(usr['name'],usr['age'])
    db.session.add(user)
    db.session.commit()
    
    return {"message":"added user sucessfully"}

@app.get("/users")
def allusers():
    data=Users.query.all()
    data=users.dump(data)

    return users.jsonify(data)

@app.route('/user/<uid>')
def getuser(uid):
    data=Users.query.filter_by(id=uid).first()
    data=user.dump(data)

    return user.jsonify(data)

@app.route("/delete/<uid>")
def delete(uid):
    usr=Users.query.filter_by(id=uid).first()
    db.session.delete(usr)
    db.session.commit()

    return {"msg":"deleted successfully"}

if __name__=="__main__":
    db.create_all()
    app.run(debug=True) 