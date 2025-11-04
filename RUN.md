1. Setup and activate your python environment
> cd to the folder you cloned this repo to.
> python venv ./
> pip install -r requirements.txt
> ./Scripts/Activate

2. Run the app
To run on localhost run:
> uvicorn main:app --reload
#uvicorn: A web server implementation for python.
#main: The python file to run
#app: The app to run
#--reload makes it so you don't have to rerun the server every time you make a change.

3. Make sure to deactivate your environment when you are done.
> deactivate