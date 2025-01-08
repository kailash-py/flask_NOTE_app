from website import create_app, db   #__init__.py file in website folder

app = create_app()

if __name__=='__main__':
    app.run(debug=True)
