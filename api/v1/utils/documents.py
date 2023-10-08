#!/usr/bin/python3
"""Upload files to the specified directory or server."""

import os
from datetime import datetime
import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile
from fastapi.responses import FileResponse
from api.v1.configurations.settings import settings

UPLOAD_DIR = "documents/uploads"
up_date = f"_{datetime.now().date()}"


async def upload_file(uuid_pk: str, file: UploadFile):
    """Upload a document file to local storage."""
    if file.filename:
        file.filename = uuid_pk + up_date + file.filename
    else:
        file.filename = uuid_pk + up_date + file.filename
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return {"filename": file.filename}


s3 = boto3.client(
    's3', aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY
)


async def aws_s3_upload_file(uuid_pk: str, file: UploadFile):
    """Upload a file to the AWS Cloud Storage."""
    if file.filename:
        file.filename = uuid_pk + up_date + file.filename
    else:
        file.filename = uuid_pk + up_date + file.filename
    try:
        s3.upload_fileobj(
            file.file,
            settings.AWS_BUCKET_NAME,
            file.filename
        )
        return {"message": f"File '{file.filename}' uploaded successfully."}
    except NoCredentialsError:
        return {"error": "AWS credentials not found."}


async def download_file(file_name: str) -> FileResponse:
    """Download a file."""
    for root, dirs, files in os.walk(UPLOAD_DIR):
        for file in files:
            if file_name in file:
                file_path = os.path.join(root, file)

    return FileResponse(file_path)
