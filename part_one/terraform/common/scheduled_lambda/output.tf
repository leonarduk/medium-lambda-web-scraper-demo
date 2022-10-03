output "lambda_function_lambda_role_name" {
  description = "The name of the IAM role created for the Lambda Function"
  value       = module.scheduled_lambda.lambda_function_lambda_role_name
}