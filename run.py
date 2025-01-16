from app import create_app

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    # Run the app in debug mode with specified host and port
    app.run(debug=True, host='127.0.0.1', port=5000)
