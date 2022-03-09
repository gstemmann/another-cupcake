from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
def connect_db(app):
    db.app = app
    db.init_app(app)
defaut_img = 'https://tinyurl.com/demo-cupcake'
class Cupcake(db.Model):
   
    __tablename__ = "cupcakes"
    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default=defaut_img)

    def serialize(self):
    # """Serialize a dessert SQLAlchemy obj to dictionary."""
        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image
        }

    def __repr__(self):
        return f"<Cupcake {self.id} flavor={self.flavor} size={self.size} rating={self.rating} image={self.image} >"