# app.py
from app import create_app

app = create_app()  # 👈 this must be top-level, not inside __main__

if __name__ == '__main__':
    app.run()
