from fastapi import APIRouter, HTTPException
from app.services.aws_service import AWSService

router = APIRouter()

aws_service = AWSService()


@router.get("/ec2_billing/monthly")
def get_monthly_billing(region:str="eu-north-1"):
    try:
        billing_data = aws_service.get_monthly_cost(region)
        return billing_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))