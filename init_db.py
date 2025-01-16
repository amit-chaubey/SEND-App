from app import create_app, db
from app.models import Word  # Ensure to upload all the  models

app = create_app()

# Use app context to create tables
with app.app_context():
    db.create_all()
    print("Database and tables created successfully.")

