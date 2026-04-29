import boto3
from botocore.exceptions import BotoCoreError, ClientError
from datetime import datetime, timedelta

class AWSService:
    def __init__(self, profile_name: str = "IAM_User_Profile"):
        """
        Initialize AWS session (shared across all services)
        This will get from the aws/credentials file, the profile named "IAM_User_Profile" (or any other profile you specify)
        """
        self.session = boto3.Session(profile_name=profile_name)

    def get_ec2_instances(self, region: str) -> list:
        """
        Fetch EC2 instances for a given region
        """
        try:
            ec2_client = self.session.client("ec2", region_name=region)
            response = ec2_client.describe_instances()

            instances = []

            for reservation in response.get("Reservations", []):
                for instance in reservation.get("Instances", []):

                    tags = {
                        t['Key']: t['Value']
                        for t in instance.get("Tags", [])
                    } if instance.get("Tags") else {}

                    instance_data = {
                        "instance_id": instance.get("InstanceId"),
                        "instance_type": instance.get("InstanceType"),
                        "state": instance.get("State", {}).get("Name"),
                        "region": region,
                        "application_name": tags.get("Name", "No application name"),
                    }

                    instances.append(instance_data)

            return instances

        except (BotoCoreError, ClientError) as e:
            raise Exception(f"AWS Error: {str(e)}")

        except Exception as e:
            raise Exception(f"Unexpected Error: {str(e)}")
   
   
    def get_monthly_cost(self, region: str) -> dict:
            try:
                ce_client = self.session.client("ce", region_name="us-east-1") #us-east-1 → AWS billing server location
                                                                                #REGION filter → which data you ask from that server, appiled the filter below.

                end_date = datetime.utcnow().date()
                start_date = end_date - timedelta(days=30)

                response = ce_client.get_cost_and_usage(
                    TimePeriod={
                        "Start": start_date.strftime("%Y-%m-%d"),
                        "End": end_date.strftime("%Y-%m-%d")
                    },
                    Granularity="MONTHLY",
                    Metrics=["UnblendedCost"],
                    Filter={
                        "And": [
                            {
                                "Dimensions": {
                                    "Key": "SERVICE",
                                    "Values": ["Amazon Elastic Compute Cloud - Compute"]
                                }
                            },
                            {
                                "Dimensions": {
                                    "Key": "REGION",
                                    "Values": [region]
                                }
                            }
                        ]
                    }
                )

                results = response.get("ResultsByTime", [])

                if not results:
                    return {
                        "total_cost": 0,
                        "currency": "USD",
                        "region": region
                    }

                amount = results[0]["Total"]["UnblendedCost"]["Amount"]
                currency = results[0]["Total"]["UnblendedCost"]["Unit"]

                return {
                    "total_cost": round(float(amount), 2),
                    "service": "EC2",
                    "region": region,
                    "currency": currency,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d")
                }

            except (BotoCoreError, ClientError) as e:
                raise Exception(f"AWS Billing Error: {str(e)}")

    def get_cpu_utilization(self, instance_id: str, region: str) -> list:
        """
        Fetch CPU utilization for a given EC2 instance 
        """
        try:
            cloudwatch_client = self.session.client("cloudwatch", region_name=region)

            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=7) #for seven days

            response = cloudwatch_client.get_metric_statistics(
                Namespace="AWS/EC2",
                MetricName="CPUUtilization",
                Dimensions=[
                    {
                        "Name": "InstanceId",
                        "Value": instance_id
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=36000,  
                Statistics=["Average"]
            )
            #
            #print(response)
            datapoints = response.get("Datapoints", [])
            #print(datapoints)
            
            # Sort by timestamp (important)
            sorted_points = sorted(datapoints, key=lambda x: x["Timestamp"])

            result = [
                {
                    "timestamp": point["Timestamp"].isoformat(),
                    "value": round(point["Average"], 2)
                }
                for point in sorted_points
            ]
            #print(result)
            return result

        except (BotoCoreError, ClientError) as e:
            raise Exception(f"AWS Metrics Error: {str(e)}")

        except Exception as e:
            raise Exception(f"Unexpected Error: {str(e)}")