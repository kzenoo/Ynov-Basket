from YNOV_BASKET import create_app, db
from YNOV_BASKET.models import User

app = create_app()

with app.app_context():
    users = User.query.all()
    print(f"Nombre total d'utilisateurs : {len(users)}")
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")