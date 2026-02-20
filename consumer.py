import boto3, os, time

sqs = boto3.client(
    "sqs",
    region_name=os.environ["AWS_REGION"],
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
)

QUEUE_URL = os.environ["QUEUE_URL"]

while True:
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20
    )

    messages = response.get("Messages", [])

    if not messages:
        print("No messages, sleeping...")
        time.sleep(5)
        continue

    for msg in messages:
        print("Processing:", msg["Body"])

        # simulate work
        time.sleep(10)

        sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=msg["ReceiptHandle"]
        )
