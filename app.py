# app.py

from app import create_app

app = create_app()  # 👈 make sure this line is present at the top level

if __name__ == '__main__':
    app.run(debug=True)
