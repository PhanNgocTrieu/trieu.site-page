"""
Standalone script to create default admin user.
This is called from entrypoint.sh after migrations are complete.
"""
from app import create_app
from app.models.user import User
from app.extensions import db

def create_default_admin():
    app = create_app()
    
    with app.app_context():
        try:
            # Check if admin already exists
            admin = User.query.filter_by(username='admin').first()
            
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@spiritualfeed.com',
                    role='admin'
                )
                admin.set_password('admin12345')
                db.session.add(admin)
                db.session.commit()
                print("✓ Created default admin user: admin/admin12345")
            else:
                print("✓ Admin user already exists")
                
        except Exception as e:
            print(f"✗ Failed to create admin user: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    create_default_admin()
