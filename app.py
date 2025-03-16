from website import create_app
from website import db


app=create_app()
with app.app_context():
    if __name__ == '__main__':
        app.run(debug=True)
        #print(f"Database URI----->>>>: {db.engine.url}") 



