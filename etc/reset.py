from ..app import db

def reset():
    db.students.drop()

reset()
