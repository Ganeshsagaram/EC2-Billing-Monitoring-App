from fastapi import APIRouter, HTTPException
from app.services.aws_service import AWSService
router = APIRouter()

aws_service = AWSService()

#“Metrics are fetched using instance ID and region; if they don’t match, CloudWatch returns empty data, so validation can be added as an enhancement.”

@router.get("/metrics/cpu/{instance_id}")
def get_cpu_metrics(instance_id: str, region: str = "eu-north-1"):
    try:
        data = aws_service.get_cpu_utilization(instance_id, region)
        if len(data) == 0:
            return {
                "message": "No CPU activity in given time range",
                "data": []
            }
        return {
            "instance_id": instance_id,
            "region": region,
            "metric": "CPUUtilization",
            "data": data,
            "count": len(data)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))