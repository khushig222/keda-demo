output "queue_url" {
  value = aws_sqs_queue.keda_queue.id
}

output "queue_arn" {
  value = aws_sqs_queue.keda_queue.arn
}
