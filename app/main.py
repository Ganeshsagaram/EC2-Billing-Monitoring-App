from fastapi import FastAPI
from pydantic import BaseModel
# from .routes.ec2 import router as router_to_ec2
from app.routes import ec2  # Import the EC2 router to include it in the main app
from app.routes import billing  # Import the billing router to include it in the main app
from app.routes import metrics

# class Name(BaseModel):
#     firstName: str
#     lastName: str

app = FastAPI()


app.include_router(ec2.router)  # Include the EC2 router to handle EC2-related endpoints
app.include_router(billing.router)  # Include the billing router to handle billing-related endpoints
app.include_router(metrics.router)  # Include the metrics router to handle metrics-related endpoints

@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# @app.post("/name")
# async def return_message(name: Name):
#     return_msg="Hi "+name.firstName+" "+name.lastName+"!"
#     return return_msg

