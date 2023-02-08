variable "cron_schedule" {
  default = "rate(1 hour)"
}
variable "cron_description" {
  default = "retry scheduled every 1 hour"
}
variable "function_name" {}
variable "function_description" {}
variable "tags" {}
variable "function_source" {
  default = "../python/lambda/check_website"
}
variable "aws_cloudwatch_event_rule_name" {}
variable "lambda_permission_statement_id" {}

variable "environment_variables" {
  description = "A map that defines environment variables for the Lambda Function."
  type        = map(string)
  default     = {}
}
variable "layers" {
  default = []
}
