#################################
# Lambda Layer (storing locally)
#################################


resource "aws_lambda_layer_version" "lambda_layer_homestats" {
  filename            = "../python/track_house_inventory_layer.zip"
  layer_name          = "homestats-layer-local"
  source_code_hash    = filebase64sha256("../python/track_house_inventory_layer.zip")
  compatible_runtimes = ["python3.9"]
}

module "TrackHouseInventory" {
  source = "../../common/terraform/modules/scheduled_lambda"

  function_name        = "HS_TrackOverallHouseInventoryStats"
  function_description = "Tracks overall house price stats"
  function_source      = "../python/TrackHouseInventory"

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

module "TrackInventoryByPostcode" {
  source = "../../common/terraform/modules/scheduled_lambda"

  function_name        = "HS_TrackInventoryByPostcode"
  function_description = "Tracks house price stats by post code"
  function_source      = "../python/TrackPostcodeInventory"

  tags   = "home_stats"
  layers = [aws_lambda_layer_version.lambda_layer_homestats.arn]

  environment_variables = {
    site     = "https://www.home.co.uk/search/property.htm?location="
    postcode = "sw19,e11"
  }


  cron_schedule    = "rate(1 day)"
  cron_description = "Every day"

  aws_cloudwatch_event_rule_name = "TrackInventoryByPostcode_rule"
  lambda_permission_statement_id = "LeonardUKAllowExecutionFromCloudWatch"
}

module "ImportHomeStats" {
  source = "../../common/terraform/modules/lambda_function"

  function_name        = "HS_ImportHomeStats"
  function_description = "Import CSV"
  function_source      = "../python/ImportCSVfile"

  tags                  = "home_stats"
  environment_variables = {
    FILE = "base_rates.csv"
  }

  layers = [aws_lambda_layer_version.lambda_layer_homestats.arn]

}

module "QueryHomeStats" {
  source = "../../../../common/terraform/modules/lambda_function"

  function_name        = "HS_QueryHomeStats"
  function_description = "QueryHomeStats"
  function_source      = "../python/QueryHomeStats"

  tags = "home_stats"
}

resource "aws_iam_role_policy" "TrackInventoryByPostcode_db_policy" {
  name   = "TrackInventoryByPostcode_db_policy"
  role   = module.TrackInventoryByPostcode.lambda_function_lambda_role_name
  policy = file("policy.json")
}

resource "aws_iam_role_policy" "TrackHouseInventory_db_policy" {
  name   = "TrackInventoryByPostcode_db_policy"
  role   = module.TrackHouseInventory.lambda_function_lambda_role_name
  policy = file("policy.json")
}

resource "aws_iam_role_policy" "ImportHomeStats_db_policy" {
  name   = "TrackInventoryByPostcode_db_policy"
  role   = module.ImportHomeStats.lambda_function_lambda_role_name
  policy = file("policy.json")
}

resource "aws_iam_role_policy" "QueryHomeStats_db_policy" {
  name   = "TrackInventoryByPostcode_db_policy"
  role   = module.QueryHomeStats.lambda_function_lambda_role_name
  policy = file("policy.json")
}

