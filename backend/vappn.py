from dotenv import load_dotenv
load_dotenv()

from app import app, db
from app.models import User


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(host='0.0.0.0')