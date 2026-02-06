resource "aws_sqs_queue" "keda_queue" {
  name = var.queue_name

  visibility_timeout_seconds = 30
  message_retention_seconds  = 345600   
  delay_seconds              = 0
  receive_wait_time_seconds  = 0
  max_message_size           = 262144   

  sqs_managed_sse_enabled = true

  fifo_queue = false

  redrive_policy = null

  tags = {}
}

data "aws_caller_identity" "current" {}

resource "aws_sqs_queue_policy" "queue_policy" {
  queue_url = aws_sqs_queue.keda_queue.id

  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "__default_policy_ID"
    Statement = [
      {
        Sid    = "__owner_statement"
        Effect = "Allow"

        Principal = {
          AWS = data.aws_caller_identity.current.account_id
        }

        Action   = "SQS:*"
        Resource = aws_sqs_queue.keda_queue.arn
      }
    ]
  })
}

