# Smart-composter-hci-cloud-API

Steps to deploy the app

1. Clone the repository
2. In root directory run the commands
    `python3 -m venv venv`
    `source venv/bin/activate`
    `pip install -r requirements.txt`
3. Create in root folder '.env' file with key variable and value
    `API_KEY="your_secret_key"`
4. To run for local testing use this command in root directory
    `uvicorn main:app --host 127.0.0.1 --port 8000`
5. To run on the server use this command in the root directory
    `uvicorn main:app --host 0.0.0.0 --port 8000`


# Swagger route
http://SERVER_HOST:PORT/docs

# Swagger route for local testing
http://localhost:8000/docs
