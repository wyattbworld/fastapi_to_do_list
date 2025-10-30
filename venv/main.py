from fastapi import FastAPI

app = FastAPI(title="Wyatt's FastAPI Demo", description="Your number one to-do app!")

#Create routes
@app.get("/") #Define what path we are using
def home():
    return {"Hello": "FastAPI"} #Json response