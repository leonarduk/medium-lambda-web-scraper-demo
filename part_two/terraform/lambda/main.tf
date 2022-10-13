## From Part One

resource "aws_lambda_layer_version" "lambda_layer_homestats" {
  filename            = "../../python/TrackHouseInventory/track_house_inventory_layer.zip"
  layer_name          = "homestats-layer-local"
  source_code_hash    = filebase64sha256("../../python/TrackHouseInventory/track_house_inventory_layer.zip")
  compatible_runtimes = ["python3.9"]
}

module "TrackHouseInventoryLambda" {
  source = "../common/scheduled_lambda"

  function_name        = "TrackOverallHouseInventoryStats"
  function_description = "Saves overall house price stats to the HomeStatsDB DynamoDB"
  function_source      = "../../python/TrackHouseInventory"

  tags = "home_stats"

  environment_variables = {
    site = "https://www.home.co.uk/company/stats.htm"
  }

  layers           = [aws_lambda_layer_version.lambda_layer_homestats.arn]
  cron_schedule    = "rate(1 day)"
  cron_description = "Every day"

  aws_cloudwatch_event_rule_name = "TrackHouseInventory_rule"
  lambda_permission_statement_id = "LeonardUKAllowExecutionFromCloudWatch"
}

resource "aws_iam_role_policy" "TrackHouseInventory_db_policy" {
  name   = "TrackInventoryByPostcode_db_policy"
  role   = module.TrackHouseInventoryLambda.lambda_function_lambda_role_name
  policy = file("policy.json")
}

## Added in  Part Two

module "QueryHomeStats" {
  source = "../common/lambda_function"

  function_name        = "QueryHomeStats"
  function_description = "Lambda to query the HomeStatsDB DynamoDB"
  function_source      = "../../python/QueryHomeStats"

  tags = "home_stats"
}

resource "aws_iam_role_policy" "QueryHomeStats_db_policy" {
  name   = "QueryHomeStats_db_policy"
  role   = module.QueryHomeStats.lambda_function_lambda_role_name
  policy = file("policy.json")
}
