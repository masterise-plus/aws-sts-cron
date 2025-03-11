# AWS Bedrock Token Refresher

A Python application that refreshes AWS credentials using STS and updates them in LangFlow via API. The application runs continuously and automatically refreshes credentials every 24 hours.

## Environment Variables

Copy the `.env.example` file to `.env` and fill in the required values:

```
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
LANGFLOW_API_BASEURL=your_langflow_api_url

AWS_ACCESS_KEY_VAR_ID=your_langflow_access_key_var_id
AWS_SECRET_KEY_VAR_ID=your_langflow_secret_key_var_id
AWS_SESSION_KEY_VAR_ID=your_langflow_session_key_var_id
```

## Dependencies

The application requires the following Python packages:

```
boto3==1.37.9
botocore==1.37.9
python-dotenv==1.0.1
requests==2.32.3
```

Additional dependencies are listed in the `requirement.txt` file.

## Docker Usage

The application is containerized using a multi-stage Docker build for optimized image size and security.

### Building and Running with Docker Compose

The easiest way to run the application is with Docker Compose:

```bash
docker-compose up -d
```

This will build the Docker image and start the container in detached mode with automatic restart unless explicitly stopped.

### Building the Docker Image Manually

```bash
docker build -t aws-bedrock-token-refresher .
```

### Running the Container Manually

```bash
docker run --env-file .env aws-bedrock-token-refresher
```

## Running Without Docker

1. Install the required dependencies:

```bash
pip install -r requirement.txt
```

2. Run the application:

```bash
python main.py
```

## Security Features

- Multi-stage Docker build for smaller attack surface
- Non-root user execution in container
- Environment variables for sensitive configuration
- Read-only volume mounting for .env file
