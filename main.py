from website import create_app

app = create_app()

if __name__ == '__main__':
#if you're running main directly
    app.run(debug=True) #debug = auto-update dev server
    #run the flask app

