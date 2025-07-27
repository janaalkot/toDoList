from flask import Flask , render_template, request ,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

    
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)
class Todo(db.Model):
    priority = db.Column(db.Integer , primary_key = True)
    todo = db.Column(db.String(200) , nullable = False)
    detalis = db.Column(db.String(600) , nullable = False)
    time = db.Column(db.DateTime , default = datetime.utcnow)
    def __repr__(self) -> str:
        return f"{self.priority} - {self.todo}"
    
@app.route("/", methods =['GET','POST'])

def enter():
    
    if request.method=='POST':
        todo_title =request.form['todo']
        detalis_title =request.form['details']
        data = Todo(todo= todo_title , detalis = detalis_title)
        db.session.add(data)
        db.session.commit()

    alltodo = Todo.query.all()
    
    return render_template("index.html" , alltodo = alltodo)

@app.route("/delete/<int:priority>")
def delete(priority):
    todo = Todo.query.filter_by(priority=priority).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route("/update/<int:priority>" , methods =['GET','POST'])
def update(priority):
    if request.method=='POST' :
        todo_title =request.form['todo']
        detalis_title =request.form['details']
        data = Todo.query.filter_by(priority=priority).first()
        data.todo = todo_title
        data.detalis = detalis_title
        db.session.add(data)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(priority=priority).first()
    return render_template('update.html' , todo=todo)

if __name__ == "__main__":
    app.run(debug = True)