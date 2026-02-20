import boto3

sqs = boto3.client(
    "sqs",
    region_name="us-west-2",
    aws_access_key_id="<access-key-id>",
    aws_secret_access_key="<access-key>"
)

QUEUE_URL = "https://sqs.us-west-2.amazonaws.com/976374902508/keda-sqs-queue"

for i in range(25):
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=f"msg {i}"
    )
    print("sent", i)
