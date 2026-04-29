from fastapi import APIRouter, HTTPException
import boto3
from app.services.aws_service import AWSService
router = APIRouter()

aws_service = AWSService()  # Initialize the AWS service ( profile)

@router.get("/ec2/instances")
def get_ec2_instances(region:str="eu-north-1"):
    try:
        instances = aws_service.get_ec2_instances(region)
        return {
                "instances": instances,
                "count": len(instances)
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))