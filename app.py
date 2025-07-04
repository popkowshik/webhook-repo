from app import create_app  # Import create_app from your app folder

app = create_app()  # Initialize Flask app

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)
