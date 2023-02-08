variable "QueryHomeStats_lambda_function_name" {
  default = "QueryHomeStats"
}

 variable "QueryHomeStats_lambda_invoke_arn" {
   default = "arn:aws:apigateway:eu-west-1:lambda:path/2015-03-31/functions/arn:aws:lambda:eu-west-1:575836911148:function:QueryHomeStats/invocations"
 }

