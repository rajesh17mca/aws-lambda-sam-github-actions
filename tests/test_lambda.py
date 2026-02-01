import pytest
import lambda_function as app
from botocore.exceptions import ClientError
from unittest.mock import patch, MagicMock


def test_get_account_id_success():
    with patch.object(app, "sts") as mock_sts:
        mock_sts.get_caller_identity.return_value = {
            "Account": "123456789012"
        }

        account_id = app.get_account_id()
        assert account_id == "123456789012"


def test_list_s3_buckets_success():
    with patch.object(app, "s3") as mock_s3:
        mock_s3.list_buckets.return_value = {
            "Buckets": [
                {"Name": "bucket-1"},
                {"Name": "bucket-2"},
            ]
        }

        buckets = app.list_s3_buckets()
        assert buckets == ["bucket-1", "bucket-2"]


def test_lambda_handler_success():
    with patch.object(app, "get_account_id", return_value="123456789012"), \
         patch.object(app, "list_s3_buckets", return_value=["b1", "b2"]):

        response = app.lambda_handler({}, {})

        assert response["statusCode"] == 200
        assert response["account_id"] == "123456789012"
        assert response["bucket_count"] == 2
        assert response["buckets"] == ["b1", "b2"]


def test_lambda_handler_client_error():
    error = ClientError(
        error_response={"Error": {"Code": "AccessDenied", "Message": "Denied"}},
        operation_name="ListBuckets"
    )

    with patch.object(app, "get_account_id", side_effect=error):
        response = app.lambda_handler({}, {})

        assert response["statusCode"] == 500
        assert response["error"] == "AWS service error"


def test_lambda_handler_unhandled_exception():
    with patch.object(app, "get_account_id", side_effect=Exception("Boom")):
        response = app.lambda_handler({}, {})

        assert response["statusCode"] == 500
        assert response["error"] == "Internal server error"
