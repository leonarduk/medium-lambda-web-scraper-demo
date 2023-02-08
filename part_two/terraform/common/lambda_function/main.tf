
module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = var.function_name
  description   = var.function_description
  handler       = var.function_handler


  # https://docs.aws.amazon.com/lambda/latest/dg/API_CreateFunction.html#SSS-CreateFunction-request-Runtime
  # Valid Values: nodejs | nodejs4.3 | nodejs6.10 | nodejs8.10 | nodejs10.x | nodejs12.x | nodejs14.x | nodejs16.x
  # | java8 | java8.al2 | java11 | python2.7 | python3.6 | python3.7 | python3.8 | python3.9 | dotnetcore1.0
  # | dotnetcore2.0 | dotnetcore2.1 | dotnetcore3.1 | dotnet6 | nodejs4.3-edge | go1.x | ruby2.5 | ruby2.7
  # | provided | provided.al2
  runtime       = var.function_runtime

  source_path = var.function_source

  timeout = var.timeout
  tags = {
    Name = var.tags
  }

  layers = var.layers

  environment_variables = var.environment_variables
}

