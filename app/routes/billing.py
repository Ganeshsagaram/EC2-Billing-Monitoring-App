from fastapi import APIRouter, HTTPException,Depends
from app.routes.auth import get_current_user
from app.services.aws_service import AWSService
from app.routes.auth import get_current_user

router = APIRouter()

aws_service = AWSService()


@router.get("/ec2_billing/monthly")
def get_monthly_billing( region: str = "eu-north-1",user: str = Depends(get_current_user)):
    try:
        billing_data = aws_service.get_monthly_cost(region)
        return billing_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))