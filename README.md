# EC2 Billing Monitoring App

An integrated application for monitoring AWS EC2 instances and billing data with a modern web dashboard and RESTful API backend.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Frontend Dashboard](#frontend-dashboard)
- [Troubleshooting](#troubleshooting)

## Overview

EC2 Billing Monitoring App is a comprehensive solution for AWS users to:
- **Monitor** EC2 instances across multiple regions
- **Track** billing and cost metrics
- **Visualize** data through an interactive Streamlit dashboard
- **Access** functionality via RESTful API endpoints with JWT authentication

The application consists of:
- **Backend**: FastAPI-based REST API with AWS integration
- **Frontend**: Streamlit interactive dashboard
- **AWS Integration**: Direct boto3 connectivity for EC2 and billing data

## Features

✅ **EC2 Instance Monitoring**
- List EC2 instances by region
- Filter and search instances
- Real-time status tracking

✅ **Billing Analytics**
- Track AWS billing data
- Cost analysis and metrics
- Historical billing trends

✅ **Authentication**
- JWT-based secure authentication
- User management

✅ **Interactive Dashboard**
- Streamlit-powered web interface
- Real-time data visualization
- User-friendly controls

✅ **RESTful API**
- Well-documented endpoints
- Easy integration capabilities
- Health check endpoints

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** ([Download here](https://www.python.org/downloads/))
- **pip** (Python package manager - usually comes with Python)
- **AWS Account** with appropriate permissions (EC2, Billing)
- **AWS CLI** configured (optional but recommended)
- **Git** for cloning the repository

### AWS Permissions Required

Your AWS user/role needs the following permissions:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeRegions",
        "ce:GetCostAndUsage"
      ],
      "Resource": "*"
    }
  ]
}
```

## Project Structure

```
EC2-Billing-Monitoring-App/
├── app/                           # Main application package
│   ├── main.py                   # FastAPI app initialization
│   ├── config.py                 # Configuration and settings
│   ├── models/
│   │   └── user.py              # User data models
│   ├── routes/
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── ec2.py               # EC2 management endpoints
│   │   ├── billing.py           # Billing endpoints
│   │   └── metrics.py           # Metrics endpoints
│   ├── services/
│   │   └── aws_service.py       # AWS SDK integration
│ 
│
├── front-end-dashboard/
│   └── streamlit_app.py         # Streamlit dashboard application
├── aws/                          # AWS-related files
│   ├── install                  # Installation scripts
│   └── README.md                # AWS-specific documentation
├── req.txt                       # Python dependencies
├── example_get_ec2_instances.py # Example EC2 usage script
└── README.md                     # This file
```

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/Ganeshsagaram/EC2-Billing-Monitoring-App.git
cd EC2-Billing-Monitoring-App
```

### Step 2: Create a Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv .EC2-venv
source .EC2-venv/bin/activate
```

**On Windows:**
```bash
python -m venv .EC2-venv
.EC2-venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r req.txt
```

### Step 4: Configure AWS Credentials

#### Option A: Using AWS CLI (Recommended)

```bash
aws configure
```

Follow the prompts to enter:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `eu-north-1`, `us-east-1`)
- Default output format (e.g., `json`)

#### Option B: Using Environment Variables

```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="eu-north-1"
```

#### Option C: Using AWS Credentials File

Create or edit `~/.aws/credentials`:
```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY

[profile-name]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

And `~/.aws/config`:
```ini
[default]
region = eu-north-1

[profile profile-name]
region = us-east-1
```

### Step 5: Update Configuration (Optional)

Edit `app/config.py` to customize:
- JWT secret key (change `SECRET_KEY` for production)
- Authentication algorithm
- Token expiration time
- Default credentials

**⚠️ For Production**: Never use default credentials. Use strong, unique values.

## Running the Application

### Start the Backend API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: **http://localhost:8000**

**API Documentation** (Swagger UI): **http://localhost:8000/docs**

**Alternative OpenAPI Documentation**: **http://localhost:8000/redoc**

### Start the Frontend Dashboard

In a new terminal (with the virtual environment activated):

```bash
streamlit run front-end-dashboard/streamlit_app.py
```

The dashboard will open in your browser at: **http://localhost:8501**

## API Endpoints

### Health Check
```bash
GET /health
```
Returns: `{"status": "ok"}`

### Authentication
```bash
POST /auth/login
Query Parameters:
  - username (string)
  - password (string)
```
Returns: JWT token for authenticated requests

### EC2 Endpoints
```bash
GET /ec2/instances
Query Parameters:
  - region (string, default: "eu-north-1")
```
Returns: List of EC2 instances in the specified region

**Example:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/ec2/instances?region=us-east-1"
```

### Billing Endpoints
```bash
GET /ec2_billing/monthly"
```
Returns: Billing and cost information

### Metrics Endpoints
```bash
GET /metrics/cpu/{instance_id}
```
Returns: Metrics and usage statistics for each instance

## Frontend Dashboard

The Streamlit dashboard provides:

1. **Login Interface**
   - Username/password authentication
   - Session token management

2. **EC2 Instance Viewer**
   - View running instances
   - Filter by region
   - Instance details and status

3. **Billing Dashboard**
   - Cost trends and analysis
   - Expense breakdown
   - Budget tracking

4. **Metrics & Analytics**
   - Usage statistics
   - Performance metrics
   - Custom reports

### Default Credentials (⚠️ Change in Production)
- **Username**: `<from_config_file>`
- **Password**: `<from_config_file>`

## Testing

Run the example script to test EC2 connectivity:

```bash
python example_get_ec2_instances.py --region eu-north-1
```

Or with a specific AWS profile:
```bash
python example_get_ec2_instances.py --profile myprofile --region us-east-1
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'app'"

**Solution**: Ensure you're running commands from the project root directory and have activated the virtual environment.

```bash
cd EC2-Billing-Monitoring-App
source .EC2-venv/bin/activate  # macOS/Linux
# or
.EC2-venv\Scripts\activate     # Windows
```

### Issue: "InvalidClientTokenId" or "AccessDenied"

**Solution**: Check your AWS credentials:
```bash
aws sts get-caller-identity
```

This should return your account details. If it fails, reconfigure your credentials.

### Issue: Streamlit app won't connect to API

**Solution**: 
1. Ensure the backend API is running on port 8000
2. Check the `BASE_URL` in `front-end-dashboard/streamlit_app.py`
3. Verify firewall settings allow local connections

### Issue: "Failed to establish a new connection"

**Solution**: Make sure the FastAPI backend is running:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Issue: Port 8000 or 8501 already in use

**Solution**: Change the port when starting:
```bash
# For API
uvicorn app.main:app --reload --port 8001

# For Dashboard
streamlit run front-end-dashboard/streamlit_app.py --server.port 8502
```

### Issue: AWS Region Not Found

**Solution**: Use a valid AWS region:
- `us-east-1`, `us-west-2`
- `eu-west-1`, `eu-north-1`
- `ap-southeast-1`, `ap-northeast-1`

See [AWS Regions](https://docs.aws.amazon.com/general/latest/gr/ec2-service.html) for complete list.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | AWS access key | (required) |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | (required) |
| `AWS_DEFAULT_REGION` | Default AWS region | `eu-north-1` |
| `PYTHONUNBUFFERED` | Show logs in real-time | `1` |

## Development Tips

### Adding New Endpoints

1. Create a new file in `app/routes/`
2. Define routes using FastAPI router:
   ```python
   from fastapi import APIRouter
   router = APIRouter()
   
   @router.get("/yourroute")
   async def your_endpoint():
       return {"message": "success"}
   ```
3. Import and include in `app/main.py`:
   ```python
   from app.routes import your_module
   app.include_router(your_module.router)
   ```

### Modifying AWS Service

Edit `app/services/aws_service.py` to add new AWS functionality:
- Add new methods to fetch AWS resources
- Implement error handling
- Add caching if needed

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -m 'Add YourFeature'`
4. Push to branch: `git push origin feature/YourFeature`
5. Open a Pull Request

## Security Notes

⚠️ **Important for Production**:
1. Change the `SECRET_KEY` in `app/config.py`
2. Use environment variables for sensitive data
3. Implement proper user authentication and roles
4. Use HTTPS/TLS for all connections
5. Add rate limiting and input validation
6. Monitor and log all API access
7. Regularly rotate AWS credentials

## License

See [THIRD_PARTY_LICENSES](aws/THIRD_PARTY_LICENSES) for license information.

## Support

For issues, questions, or suggestions:
- Check the [Troubleshooting](#troubleshooting) section
- Review [AWS Documentation](https://docs.aws.amazon.com/)
- Open an issue on GitHub

## Changelog

- **v1.0** (Current) - Initial release with EC2 monitoring, billing tracking, and dashboard

---

**Happy Monitoring! 🚀**
