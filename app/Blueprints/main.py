from flask import render_template, request, Blueprint, jsonify, redirect, url_for
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, BooleanField, DateField) 
from wtforms.validators import DataRequired, Length
from app.models.todo import ToDo
from app.extensions import db


bp = Blueprint('main',__name__)

class NewTask(FlaskForm):
    task = StringField("What do you need to do?", validators=[DataRequired()])
    deadline = DateField("Deadline")
    submit = SubmitField("Submit")

# Main route
@bp.route('/main', methods=['GET', 'POST'])
def to_do():
    task = None
    form = NewTask()
    
    # Form create new task
    if form.validate_on_submit():
        task = form.task.data
        deadline = form.deadline.data
        
        todo = ToDo(username='Phong', task=task, deadline=deadline, completed=False)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('main.to_do'))
    # Display to do list
    to_do_list = ToDo.query.order_by(ToDo.id).all()
    deadline_passed = {}
    for todo in to_do_list:
        deadline_passed[todo.id] = True if datetime.now().date() > todo.deadline else False


    # Change completed status
    if request.method == 'POST':
        todo_id = request.form['completed']
        todo = ToDo.query.filter_by(id=todo_id).first()
        todo.completed = not todo.completed
        db.session.commit()
        return redirect(url_for('main.to_do'))

    # Delete request
    if request.method == 'POST':
        todo_id = request.form["delete"]
        return redirect(url_for('main.del_task', todo_id=todo_id))
    
    return render_template('main.html', task=task, form=form, to_do_list=to_do_list, deadline_passed=deadline_passed)

# Delete a task
@bp.route('/del/<todo_id>', methods=['GET', 'POST'])
def del_task(todo_id):
    todo = ToDo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('main.to_do'))