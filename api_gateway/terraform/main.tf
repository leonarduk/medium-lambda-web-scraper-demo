module "gateway" {
  source = "../../../../common/terraform/modules/api_gateway/terraform"

  lambda_function_name  = var.QueryHomeStats_lambda_function_name
  lambda_invoke_arn     = var.QueryHomeStats_lambda_invoke_arn
  gateway_description   = "HomeStats Query"
  gateway_name          = "HomestatsQuery"
  deployment_stage_name = "dev"
}