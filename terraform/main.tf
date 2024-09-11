# Configure AWS provider
provider "aws" {
  region = "us-west-2"
}

variable "lambda_zip_path" {
  description = "Path to the Lambda code zip file"
  type = string
}

# Define local file resource for Lambda code
# resource "local_file" "lambda_zip" {
#   filename = "${path.module}/../lambda.zip"
#   content = file("${path.module}/../lambda/lambda.py")
# }

# output "lambda_zip" {
#   value = local_file.lambda_zip.filename
# }

# Define AWS Lambda function
resource "aws_lambda_function" "console_chat_bot_lambda" {
  function_name = "console-chat-bot-lambda"
  handler = "lambda.lambda_handler"
  runtime = "python3.9"
  role = aws_iam_role.lambda_exec.arn
  filename = var.lambda_zip_path
  timeout = 10

  environment {
    variables = {
      OPEN_AI_SECRET_NAME = "prod/open_ai"
    }
  }

  layers = [aws_lambda_layer_version.lambda_layer.arn]

  source_code_hash = filebase64sha256(var.lambda_zip_path)
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename = "../layer_content.zip"
  layer_name = "openai-layer"
  compatible_runtimes = ["python3.9"]
  source_code_hash = filebase64sha256("../layer_content.zip")
}

# Define IAM Role for the Lambda function
resource "aws_iam_role" "lambda_exec" {
  name = "lambda-exec-role"
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Effect": "Allow",
      }
    ]
  })
}

# Define IAM Policy for Lambda access to SSM
resource "aws_iam_policy" "secrets_manager_access_policy" {
  name   = "SecretsManagerAccessPolicy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = "secretsmanager:GetSecretValue",
        Resource = "*"
      },
    ],
  })
}

resource "aws_iam_role_policy_attachment" "lambda_secrets_manager_access_policy_attachment" {
  policy_arn = aws_iam_policy.secrets_manager_access_policy.arn
  role = aws_iam_role.lambda_exec.name
}

# Define IAM Policy Attachment for Lambda access to CloudWatch Logs
resource "aws_iam_policy_attachment" "lambda_logs" {
  name = "lambda-logs"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  roles = [aws_iam_role.lambda_exec.name]
}

# API Gateway Rest API
resource "aws_api_gateway_rest_api" "console_chat_bot_api" {
  name = "console-chat-bot-api"
  description = "API Gateway for Console Chat Bot"
}

# API Gateway Resource
resource "aws_api_gateway_resource" "console_chat_bot_resource" {
  rest_api_id = aws_api_gateway_rest_api.console_chat_bot_api.id
  parent_id = aws_api_gateway_rest_api.console_chat_bot_api.root_resource_id
  path_part = "chat"
}

# Api Gateway Method
resource "aws_api_gateway_method" "console_chat_bot_method" {
  rest_api_id = aws_api_gateway_rest_api.console_chat_bot_api.id
  resource_id = aws_api_gateway_resource.console_chat_bot_resource.id
  http_method = "POST"
  authorization = "NONE"
}

# API Gateway Integration
resource "aws_api_gateway_integration" "console_chat_bot_integration" {
    rest_api_id = aws_api_gateway_rest_api.console_chat_bot_api.id
    resource_id = aws_api_gateway_resource.console_chat_bot_resource.id
    http_method = aws_api_gateway_method.console_chat_bot_method.http_method
    integration_http_method = "POST"
    type = "AWS_PROXY"
    uri = aws_lambda_function.console_chat_bot_lambda.invoke_arn
}

# API Gateway Deployment
resource "aws_api_gateway_deployment" "console_chat_bot_deployment" {
  depends_on = [aws_api_gateway_integration.console_chat_bot_integration]
  rest_api_id = aws_api_gateway_rest_api.console_chat_bot_api.id
  stage_name = "prod"
}

# Permissions for API Gateway to invoke Lambda
resource "aws_lambda_permission" "console_chat_bot_permission" {
  statement_id = "AllowExecutionFromAPIGateway"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.console_chat_bot_lambda.function_name
  principal = "apigateway.amazonaws.com"
  source_arn = "${aws_api_gateway_rest_api.console_chat_bot_api.execution_arn}/*/*"
}