#!/usr/bin/env python3
"""
example_get_ec2_instances.py

Small test script that lists running EC2 instances using boto3.

Usage:
  pip install boto3
  # Option A: use environment credentials/role
  python example_get_ec2_instances.py --region us-east-1

  # Option B: use a named profile from ~/.aws/credentials
  python example_get_ec2_instances.py --profile myprofile --region us-east-1
"""

import argparse
import boto3
from botocore.exceptions import BotoCoreError, ClientError


def list_running_instances(region=None, profile=None):
    session_args = {}
    if profile:
        session_args["profile_name"] = profile

    session = boto3.Session(**session_args) if session_args else boto3.Session()
    ec2 = session.resource("ec2", region_name=region)

    filters = [{"Name": "instance-state-name","Values": [ "running","stopped"]}]

    try:
        instances = ec2.instances.filter(Filters=filters)

        if len(list(instances)) == 0:
            print("No running instances found (in the specified region/profile).")
            return
        for inst in instances:
            #print(inst.tags)  # Debugging: Print the raw instance object
            tags = {t['Key']: t['Value'] for t in inst.tags} if inst.tags else {} # if there is any Name given to the instancem, it will converting to dict key value pair, otherwise it will be empty dict
            print(f"InstanceId: {inst.id}")
            print(f"  State: {inst.state['Name']}")
            print(f"  Type: {inst.instance_type}")
            print(f"  AZ: {inst.placement.get('AvailabilityZone')}")
            print(f"  PublicIP: {inst.public_ip_address}")
            if tags:
                print(f"  Tags: {tags}")
            print()
    except (BotoCoreError, ClientError) as e:
        print("Error accessing EC2:", e)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="List running EC2 instances (simple test script)")
    p.add_argument("--region", help="AWS region (e.g. us-east-1)")
    p.add_argument("--profile", help="AWS profile name to use from ~/.aws/credentials")
    args = p.parse_args()

    list_running_instances(region=args.region, profile=args.profile)
