import os
from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

pw= "ChangeMe#2026"
uri= f"mysql+pymysql://jona:{pw}"
uri+="@127.0.0.1/schooldb"
pw= "jona123"
uri= f"mysql+pymysql://appuser:{pw}"
uri+="@127.0.0.1/practiceTable"
app.config["SQLALCHEMY_DATABASE_URI"] = uri
db=SQLAlchemy(app)

class Student(db.Model):
    __tablename__="students"
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50))
    email = db.Column(db.String(80))

    def to_dict(self):
        return dict(id=self.id, name=self.name, email=self.email)

@app.route("/students", methods=["POST"])
def create():
    d = request.get_json()
    s = Student(name=d["name"], email=d["email"])
    db.session.add(s)
    db.session.commit()
    return jsonify(s.to_dict()), 201

@app.route("/students")
def read_all():
    rows = Student.query.all()
    return jsonify([s.to_dict() for s in rows])

@app.route("/students/<int:i>")
def read_one(i):
    s = db.get_or_404(Student, i)
    return jsonify(s.to_dict())


@app.route("/")
def home():
    return "Hello from Flask"

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)
