import time
from datetime import datetime, timezone
from azure.servicebus import ServiceBusClient, ServiceBusReceiveMode
from azure.core.exceptions import AzureError

CONNECTION_STR = "<connection-string>"
QUEUE_NAME = "keda-asb"


def log(message, level="INFO"):
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"[{timestamp}] [{level}] {message}", flush=True)


def main():
    log("Starting Azure Service Bus consumer...")

    while True:
        try:
            with ServiceBusClient.from_connection_string(CONNECTION_STR) as client:
                with client.get_queue_receiver(
                    queue_name=QUEUE_NAME,
                    receive_mode=ServiceBusReceiveMode.PEEK_LOCK
                ) as receiver:

                    log("Connected to queue. Waiting for messages...")

                    messages = receiver.receive_messages(
                        max_message_count=10,
                        max_wait_time=10
                    )

                    if not messages:
                        log("No messages received.")
                    else:
                        log(f"Received {len(messages)} message(s)")

                    for msg in messages:
                        try:
                            # Safe body extraction
                            body = b"".join(msg.body).decode("utf-8")
                            log(f"Consumed message: {body}")

                            receiver.complete_message(msg)
                            log("Message completed (removed from queue).")

                        except Exception as msg_err:
                            log(f"Message processing error: {msg_err}", "ERROR")
                            receiver.abandon_message(msg)

        except AzureError as e:
            log(f"Service Bus error: {e}", "ERROR")

        except Exception as e:
            log(f"Unexpected error: {e}", "ERROR")

        time.sleep(5)


if __name__ == "__main__":
    main()
