from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {'status':200, 'message':'FastAPI server running'}

