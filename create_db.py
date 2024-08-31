from YNOV_BASKET import create_app, db
from YNOV_BASKET.models import User

app = create_app()

with app.app_context():
    db.create_all()
    user = User(username='test_user', email='test@example.com', password='hashed_password')
    db.session.add(user)
    db.session.commit()

    print("Tables créées et utilisateur ajouté avec succès.")
