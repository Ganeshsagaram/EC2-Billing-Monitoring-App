from fastapi import APIRouter, HTTPException,Depends
import boto3
from app.services.aws_service import AWSService
from app.routes.auth import get_current_user
router = APIRouter()

aws_service = AWSService()  # Initialize the AWS service ( profile)

@router.get("/ec2/instances")
def get_ec2_instances(region:str="eu-north-1",user: str = Depends(get_current_user)):
    try:
        instances = aws_service.get_ec2_instances(region)
        return {
                "instances": instances,
                "count": len(instances)
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))