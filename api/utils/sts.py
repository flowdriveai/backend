import json

import boto3

def generate_policy(uid):
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowRootListing",
                "Action": ["s3:ListBucket"],
                "Effect": "Allow",
                "Resource": ["arn:aws:s3:::fdusermedia"],
                "Condition": {
                    "StringEquals": {
                        "s3:prefix": [f"processed/{uid}", f"unprocessed/{uid}"]
                    }
                },
            },
            {
                "Sid": "AllowUserToListObjects",
                "Action": ["s3:ListBucket"],
                "Effect": "Allow",
                "Resource": ["arn:aws:s3:::fdusermedia"],
                "Condition": {
                    "StringLike": {
                        "s3:prefix": [f"processed/{uid}/*", f"unprocessed/{uid}/*"]
                    }
                },
            },
            {
                "Sid": "AllowUserToGetObjects",
                "Action": ["s3:GetObject"],
                "Effect": "Allow",
                "Resource": [
                    f"arn:aws:s3:::fdusermedia/unprocessed/{uid}/*",
                    f"arn:aws:s3:::fdusermedia/processed/{uid}/*",
                ],
            },
            {
                "Sid": "AllowUserToPutObjects",
                "Action": ["s3:PutObject"],
                "Effect": "Allow",
                "Resource": [f"arn:aws:s3:::fdusermedia/unprocessed/{uid}/*"],
            },
        ],
    }
    return json.dumps(policy)


def generate_sts(uid):
    sts_client = boto3.client('sts')

    assumed_role=sts_client.assume_role(
        RoleArn="arn:aws:iam::758099803433:role/fdusermedia_role",
        RoleSessionName=f"session_{uid}",
        Policy=generate_policy(uid)
    )

    credentials=assumed_role['Credentials']

    sts = {
        "access_key": credentials['AccessKeyId'],
        "secret_access_key": credentials['SecretAccessKey'],
        "session_token": credentials['SessionToken'],
    }

    return sts
