import boto3
import os
import requests
import json
import time
from datetime import datetime
from dotenv import load_dotenv

def refresh_aws_credentials():
    sts = boto3.client(
        'sts',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )

    response = sts.get_session_token(DurationSeconds=129600)
    new_creds = response['Credentials']
    
    return new_creds

def update_langflow_variables(new_creds):
    """Update LangFlow variables via API"""
    langflow_api_url = os.getenv('LANGFLOW_API_BASEURL') + '/variables/'
    # api_key = "your-langflow-api-key"
    aws_access_key_var_id = os.getenv('AWS_ACCESS_KEY_VAR_ID')
    aws_secret_key_var_id = os.getenv('AWS_SECRET_KEY_VAR_ID')
    aws_session_key_var_id = os.getenv('AWS_SESSION_KEY_VAR_ID')
    
    headers = {
        "Content-Type": "application/json"
        #"Authorization": f"Bearer {api_key}"
    }

    try:
        # update access key
        responseAccessKey = requests.patch(
            langflow_api_url+aws_access_key_var_id,
            data=json.dumps({
              "id": aws_access_key_var_id,
              "value": new_creds['AccessKeyId']
            }),
            headers=headers
        )
        
        if responseAccessKey.status_code == 200:
            print("Access Key variables updated successfully!")
        else:
            print(f"Failed to update Access Key variables. Status code: {responseAccessKey.status_code}")
            print(f"Response: {responseAccessKey.text}")
            
        
        # update secret key
        responseSecretKey = requests.patch(
            langflow_api_url+aws_secret_key_var_id,
            data=json.dumps({
              "id": aws_secret_key_var_id,
              "value": new_creds['SecretAccessKey']
            }),
            headers=headers
        )
        
        if responseSecretKey.status_code == 200:
            print("Secret Key variables updated successfully!")
        else:
            print(f"Failed to update Secret Key variables. Status code: {responseSecretKey.status_code}")
            print(f"Response: {responseSecretKey.text}")
            
        
        # update session key
        responseSessionKey = requests.patch(
            langflow_api_url+aws_session_key_var_id,
            data=json.dumps({
              "id": aws_session_key_var_id,
              "value": new_creds['SessionToken']
            }),
            headers=headers
        )
        
        if responseSessionKey.status_code == 200:
            print("Session Key variables updated successfully!")
        else:
            print(f"Failed to update Session Key variables. Status code: {responseSessionKey.status_code}")
            print(f"Response: {responseSessionKey.text}")            
            
    except Exception as e:
        print(f"Error updating LangFlow variables: {str(e)}")

if __name__ == "__main__":
    load_dotenv()
    
    # Run indefinitely
    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Starting credential rotation process...")
        
        try:
            # Refresh AWS credentials
            new_creds = refresh_aws_credentials()
            
            # Update LangFlow variables via API
            update_langflow_variables(new_creds)
            
            print(f"[{current_time}] Credential rotation process completed!")
        except Exception as e:
            print(f"[{current_time}] Error during credential rotation: {str(e)}")
        
        # Sleep for 24 hours (86400 seconds)
        print(f"[{current_time}] Next rotation scheduled in 24 hours")
        time.sleep(86400)
