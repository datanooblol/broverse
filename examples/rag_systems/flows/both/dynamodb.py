import boto3
from datetime import datetime, timezone
import os

DYNAMODB_REGION_NAME = os.getenv("DYNAMODB_REGION_NAME", None)
DOCUMENT_TABLE = os.getenv("DOCUMENT_TABLE", None)
dynamodb = boto3.resource('dynamodb', region_name=DYNAMODB_REGION_NAME)
table = dynamodb.Table(DOCUMENT_TABLE)

def create_document(user_id, document_id, username, source, vector_path, status='pending'):
    now = datetime.now(timezone.utc).isoformat()

    table.put_item(
        Item={
            'user_id': user_id,
            'document_id': document_id,
            'username': username,
            'source': source,
            'vector_path': vector_path,
            'document_status': status,
            'created_at': now,
            'updated_at': now
        }
    )

def update_document_status(user_id, document_id, new_status):
    table.update_item(
        Key={
            'user_id': user_id,
            'document_id': document_id
        },
        UpdateExpression='SET document_status = :new_status, updated_at = :updated',
        ExpressionAttributeValues={
            ':new_status': new_status,
            ':updated': datetime.now(timezone.utc).isoformat()
        }
    )

def delete_document(user_id, document_id):
    table.delete_item(
        Key={
            'user_id': user_id,
            'document_id': document_id
        }
    )

def get_user_documents(user_id):
    response = table.query(
        KeyConditionExpression='user_id = :user_id',
        ExpressionAttributeValues={
            ':user_id': user_id
        }
    )
    return response['Items']

def get_document(user_id, document_id):
    response = table.get_item(
        Key={
            'user_id': user_id,
            'document_id': document_id
        }
    )
    return response.get('Item')