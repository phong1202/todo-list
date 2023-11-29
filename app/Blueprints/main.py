from flask import render_template, request, Blueprint, jsonify, redirect, url_for, flash
from datetime import datetime
from flask_wtf import FlaskForm
from flask_login import login_required, current_user
from wtforms import (StringField, SubmitField, BooleanField, DateField) 
from wtforms.validators import DataRequired, Length
from app.models.todo import ToDo, User
from app.extensions import db


bp = Blueprint('main',__name__)

class NewTask(FlaskForm):
    task = StringField("What do you need to do?", validators=[DataRequired()])
    deadline = DateField("Deadline")
    submit = SubmitField("Submit")

# Main route
@bp.route('/main', methods=['GET', 'POST'])
@login_required
def to_do():
    task = None
    form = NewTask()
    
    # Form create new task
    if form.validate_on_submit():
        task = form.task.data
        deadline = form.deadline.data
        
        todo = ToDo(user_id=current_user.id, task=task, deadline=deadline, completed=False)
        db.session.add(todo)
        db.session.commit()
        flash('Create task successfully', 'success')
        return redirect(url_for('main.to_do'))
    # Display to do list
    to_do_list = ToDo.query.filter_by(user_id=current_user.id).order_by(ToDo.id).all()
    deadline_passed = {}
    for todo in to_do_list:
        deadline_passed[todo.id] = True if datetime.now().date() > todo.deadline else False


    if request.method == 'POST' and request.form['button']:
        todo_id = request.form['id']
        todo = ToDo.query.filter_by(id=todo_id).first()
        # Change completed status
        if request.form['button'] == 'completed':
            todo.completed = not todo.completed
            db.session.commit()
            flash('Complete status change!', 'info')
        elif request.form['button'] == 'delete':
        # Delete request
            db.session.delete(todo)
            db.session.commit()
            flash('Deleted task', 'danger')
            
        return redirect(url_for('main.to_do'))
    
    
    return render_template('main.html', task=task, form=form, to_do_list=to_do_list, deadline_passed=deadline_passed)

# # Delete a task
# @bp.route('/del/<todo_id>', methods=['GET', 'POST'])
# @login_required
# def del_task(todo_id):
#     if request.method == 'POST':
#         todo = ToDo.query.filter_by(id=todo_id).first()
#         db.session.delete(todo)
#         db.session.commit()
#         return redirect(url_for('main.to_do'))
#     else:
#         return render_template('denied.html')