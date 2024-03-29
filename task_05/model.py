from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.Text())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
 
    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()