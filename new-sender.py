from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "<connection-string>"
QUEUE_NAME = "keda-asb"


def send_messages_to_queue():
    client = ServiceBusClient.from_connection_string(CONNECTION_STR)
    result = {
        "success": True,
        "sent_count": 0,
        "error": None
    }

    try:
        with client:
            sender = client.get_queue_sender(queue_name=QUEUE_NAME)
            with sender:
                for i in range(10):
                    message = ServiceBusMessage(f"Order #{i}")
                    sender.send_messages(message)
                    result["sent_count"] += 1

    except AzureError as e:
        result["success"] = False
        result["error"] = str(e)

    return result


if __name__ == "__main__":
    response = send_messages_to_queue()
    print(response)
