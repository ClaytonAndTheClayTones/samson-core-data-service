# Summary

The DICS Core Data Service is a Python FastApi implementation that provides a RESTful CRUD API for the DICS application space. Primary responsibilities include but are not limited to:

1. Creating, Retrieving, Searching, Updating, and Deleteing each entity in the DICS DB.
2. Authenticating requests and attaching them to a user.
3. Controlling which actors can access what data.
4. Providing a layer of abstraction and common model for the various services and APIs DICS will be calling.
5. Providing a control layer for the asynchronous processes and transforms in the DICS system.

# Architecture

The DICS Core Data Service follows a very strict architecture for all of its endpoints.

## Run the service

1. Open the service folder in Visual Studio Code
2. Copy the .env-example file to another file called ".env"
3. Open the terminal and run `pip install -r requirements.txt`
4. Go to the Debug Tab on the left and, near the top, select "Python Debugger: Run API"
5. Hit F5 on your keyboard. You should see console output telling you that Uvicorn is running on 127.0.0.1:8001
6. Your API is running!

## Run the API Tests

1. Open the tests folder in Visual Studio Code
2. Copy the .env-example file to a new file called ".env"
3. Open the terminal and run `pip install -r requirements.txt`
4. The Flask Tab on the left should detect tests and you can run them from there. Otherwise, go into the validation/CRUD folder and select a test file, and you can right click in the code and run a case from there.
