from app import create_app
from app.extensions import db
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    print("Existing tables:", inspector.get_table_names())
    
    # Check alembic version
    with db.engine.connect() as conn:
        try:
            result = conn.execute(db.text("SELECT * FROM alembic_version")).fetchall()
            print("Alembic Version:", result)
        except Exception as e:
            print("Alembic table check failed:", e)
