module "scheduled_lambda" {
  source = "../lambda_function"

  function_name        = var.function_name
  function_description = var.function_description
  function_source      = var.function_source
  tags                 = var.tags

  layers = var.layers
  environment_variables = var.environment_variables
}

resource "aws_cloudwatch_event_rule" "check_lambda_function_event_rule" {
  name                = var.aws_cloudwatch_event_rule_name
  description         = var.cron_description
  schedule_expression = var.cron_schedule
}

resource "aws_cloudwatch_event_target" "check_lambda_function_target" {
  arn  = module.scheduled_lambda.lambda_function_arn
  rule = aws_cloudwatch_event_rule.check_lambda_function_event_rule.name
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda_function" {
  statement_id  = var.lambda_permission_statement_id
  action        = "lambda:InvokeFunction"
  function_name = module.scheduled_lambda.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.check_lambda_function_event_rule.arn
}
