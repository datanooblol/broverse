# DynamoDB Table Structure

## Table Design

**Table Name:** `user_documents`

### Primary Key
- **Partition Key (PK):** `user_id` (String)
- **Sort Key (SK):** `document_id` (String)

### Attributes
- `username` (String)
- `document_file_path` (String) 
- `document_vector_path` (String)
- `document_status` (String)
- `created_at` (String) - ISO format
- `updated_at` (String) - ISO format

### Global Secondary Index (GSI)
**GSI Name:** `username-document_id-index`
- **Partition Key:** `username` (String)
- **Sort Key:** `document_id` (String)

## Code Examples

### Setup
```python
import boto3
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
table = dynamodb.Table('user_documents')
```

### Create Record
```python
def create_document(user_id, document_id, username, file_path, vector_path, status='pending'):
    now = datetime.now(timezone.utc).isoformat()
    
    table.put_item(
        Item={
            'user_id': user_id,
            'document_id': document_id,
            'username': username,
            'document_file_path': file_path,
            'document_vector_path': vector_path,
            'document_status': status,
            'created_at': now,
            'updated_at': now
        }
    )
```

### Update Record
```python
def update_document_status(user_id, document_id, new_status):
    table.update_item(
        Key={
            'user_id': user_id,
            'document_id': document_id
        },
        UpdateExpression='SET document_status = :status, updated_at = :updated',
        ExpressionAttributeValues={
            ':status': new_status,
            ':updated': datetime.now(timezone.utc).isoformat()
        }
    )
```

### Delete Record
```python
def delete_document(user_id, document_id):
    table.delete_item(
        Key={
            'user_id': user_id,
            'document_id': document_id
        }
    )
```

### Query by User ID
```python
def get_user_documents(user_id):
    response = table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': user_id}
    )
    return response['Items']
```

### Query by Username (using GSI)
```python
def get_documents_by_username(username):
    response = table.query(
        IndexName='username-document_id-index',
        KeyConditionExpression='username = :uname',
        ExpressionAttributeValues={':uname': username}
    )
    return response['Items']
```

### Get Specific Document
```python
def get_document(user_id, document_id):
    response = table.get_item(
        Key={
            'user_id': user_id,
            'document_id': document_id
        }
    )
    return response.get('Item')
```