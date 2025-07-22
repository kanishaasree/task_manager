from extension import db
class Task(db.Model):
    task_id=db.Column(db.Integer, primary_key=True)
    task_name=db.Column(db.String(50), nullable=False)
    task_status=db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'task_name': self.task_name,
            'task_status': self.task_status
        }