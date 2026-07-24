# Secure Document Management System

## Overview

The Secure Document Management System is a serverless AWS application that enables authenticated users to securely upload, view, download, share, revoke access to, and delete documents. The system uses Amazon Cognito for authentication, Amazon S3 for secure storage, DynamoDB for metadata management, and AWS Lambda with API Gateway for backend APIs.

---

## Features

- User authentication using Amazon Cognito
- Secure document upload using pre-signed S3 POST URLs
- Document listing based on user roles
- Secure document download using pre-signed URLs
- Share documents with registered users
- Revoke document access
- Delete documents from S3 and DynamoDB
- Role-based access control (User/Admin)
- CloudWatch logging for monitoring

---

## AWS Services Used

- Amazon Cognito
- AWS Lambda
- Amazon API Gateway
- Amazon S3
- Amazon DynamoDB
- Amazon CloudWatch
- AWS IAM

---

## Project Structure

```
Secure-Document-Management-System/
│
├── upload-document/
│   └── lambda_function.py
├── list-documents/
│   └── lambda_function.py
├── download-document/
│   └── lambda_function.py
├── delete-document/
│   └── lambda_function.py
├── share-document/
│   └── lambda_function.py
├── revoke-document/
│   └── lambda_function.py
└── metadata-trigger/
    └── lambda_function.py
```

---

## Authentication

All APIs are protected using **Amazon Cognito**.

```
Authorization: Bearer <ID_TOKEN>
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /upload?fileName={fileName} | Generate a pre-signed S3 POST URL for uploading documents |
| GET | /documents | List documents |
| GET | /documents/{documentId} | Generate a secure download URL |
| DELETE | /documents/{documentId} | Delete a document |
| POST | /documents/{documentId}/share | Share a document |
| POST | /documents/{documentId}/revoke | Revoke document access |
| GET | /shared-documents | View shared documents |

---

## Security Features

- Amazon Cognito authentication
- JWT token validation
- Private Amazon S3 bucket
- Pre-signed S3 POST URLs for uploads
- Pre-signed S3 URLs for downloads
- Role-based authorization
- Least privilege IAM policies
- CloudWatch logging



Developed using AWS Serverless services for secure document management.
