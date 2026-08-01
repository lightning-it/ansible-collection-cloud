#!/usr/bin/env python3
"""Exercise the protected S3 principals without emitting credentials or bodies."""

from __future__ import annotations

import json
import os
import sys
from collections.abc import Callable
from typing import Any

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

ENDPOINT = "https://fsn1.your-objectstorage.com"
REGION = "fsn1"
DENIED_CODES = {"AccessDenied", "AllAccessDisabled", "InvalidAccessKeyId", "403"}


def required_environment(name: str) -> str:
    value = os.environ.get(name, "")
    if not value:
        raise RuntimeError(f"required protected environment input is missing: {name}")
    return value


def client(profile: str) -> Any:
    return boto3.client(
        "s3",
        endpoint_url=ENDPOINT,
        region_name=REGION,
        aws_access_key_id=required_environment(f"HETZNER_S3_{profile}_ACCESS_KEY"),
        aws_secret_access_key=required_environment(f"HETZNER_S3_{profile}_SECRET_KEY"),
        config=Config(
            connect_timeout=10,
            read_timeout=30,
            retries={"max_attempts": 3, "mode": "standard"},
        ),
    )


def require_denied(operation: Callable[[], Any], label: str) -> None:
    try:
        operation()
    except ClientError as error:
        code = str(error.response.get("Error", {}).get("Code", ""))
        status = str(
            error.response.get("ResponseMetadata", {}).get("HTTPStatusCode", "")
        )
        if code in DENIED_CODES or status in DENIED_CODES:
            return
        raise RuntimeError(
            f"{label} failed with an unexpected provider response"
        ) from error
    raise RuntimeError(f"{label} was unexpectedly permitted")


def main() -> int:
    if len(sys.argv) != 2:
        raise RuntimeError("exactly one fixture bucket is required")
    bucket = sys.argv[1]
    admin = client("ADMIN")
    writer = client("WRITER")
    reader = client("READER")
    reviewer = client("REVIEWER")
    readable_key = "acceptance/reader-fixture"
    writer_key = "acceptance/writer-fixture"

    admin.put_bucket_tagging(
        Bucket=bucket,
        Tagging={
            "TagSet": [
                {
                    "Key": "owner",
                    "Value": required_environment("MOLECULE_TEST_OWNER")[:256],
                },
                {
                    "Key": "candidate_sha",
                    "Value": required_environment("QUALITY_SOURCE_SHA"),
                },
                {"Key": "expires_after_days", "Value": "31"},
            ]
        },
    )
    admin.put_object(
        Bucket=bucket, Key=readable_key, Body=b"non-sensitive acceptance fixture"
    )
    writer.put_object(Bucket=bucket, Key=writer_key, Body=b"writer acceptance fixture")
    reader.get_object(Bucket=bucket, Key=readable_key)["Body"].close()
    reviewer.get_object_retention(Bucket=bucket, Key=readable_key)

    require_denied(
        lambda: writer.get_object(Bucket=bucket, Key=readable_key), "writer read"
    )
    require_denied(
        lambda: writer.delete_object(Bucket=bucket, Key=writer_key), "writer delete"
    )
    require_denied(
        lambda: writer.put_bucket_policy(Bucket=bucket, Policy="{}"),
        "writer policy mutation",
    )
    require_denied(
        lambda: reader.put_object(
            Bucket=bucket, Key="acceptance/reader-write", Body=b"x"
        ),
        "reader write",
    )
    require_denied(
        lambda: reader.delete_object(Bucket=bucket, Key=readable_key), "reader delete"
    )
    require_denied(
        lambda: reader.put_bucket_policy(Bucket=bucket, Policy="{}"),
        "reader policy mutation",
    )
    require_denied(
        lambda: reader.put_object_retention(
            Bucket=bucket,
            Key=readable_key,
            Retention={"Mode": "GOVERNANCE", "RetainUntilDate": "2038-01-19T03:14:07Z"},
        ),
        "reader retention mutation",
    )
    require_denied(
        lambda: reviewer.get_object(Bucket=bucket, Key=readable_key),
        "reviewer body read",
    )
    require_denied(
        lambda: reviewer.put_object(
            Bucket=bucket, Key="acceptance/reviewer-write", Body=b"x"
        ),
        "reviewer write",
    )
    require_denied(
        lambda: reviewer.delete_object(Bucket=bucket, Key=readable_key),
        "reviewer delete",
    )
    require_denied(
        lambda: reviewer.put_bucket_policy(Bucket=bucket, Policy="{}"),
        "reviewer policy mutation",
    )
    require_denied(
        lambda: reviewer.put_object_retention(
            Bucket=bucket,
            Key=readable_key,
            Retention={"Mode": "GOVERNANCE", "RetainUntilDate": "2038-01-19T03:14:07Z"},
        ),
        "reviewer retention mutation",
    )

    print(json.dumps({"bucket": bucket, "result": "passed"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
