import boto3
import logging
from botocore.exceptions import ClientError
from typing import Dict, List, Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
sts = boto3.client("sts")


def get_account_id() -> str:
    response = sts.get_caller_identity()
    return response["Account"]


def list_s3_buckets() -> List[str]:
    response = s3.list_buckets()
    return [bucket["Name"] for bucket in response.get("Buckets", [])]


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    logger.info("Lambda execution started")

    try:
        account_id = get_account_id()
        buckets = list_s3_buckets()

        return {
            "statusCode": 200,
            "account_id": account_id,
            "bucket_count": len(buckets),
            "buckets": buckets,
        }

    except ClientError as e:
        logger.error("AWS ClientError", exc_info=e)
        return {
            "statusCode": 500,
            "error": "AWS service error",
        }

    except Exception:
        logger.exception("Unhandled exception")
        return {
            "statusCode": 500,
            "error": "Internal server error",
        }
