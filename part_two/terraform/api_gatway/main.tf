module "gateway" {
  source = "../common/api_gateway"

  lambda_function_name  = var.QueryHomeStats_lambda_function_name
  lambda_invoke_arn     = var.QueryHomeStats_lambda_invoke_arn
  gateway_description   = "HomeStats Query"
  gateway_name          = "HomestatsQuery"
  deployment_stage_name = "dev"
}