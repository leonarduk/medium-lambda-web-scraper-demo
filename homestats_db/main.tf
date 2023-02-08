resource "aws_dynamodb_table" "ddbtable" {
  name             = "HomeStatsDb"
  hash_key         = "Field"
  range_key        = "Date"
  billing_mode   = "PROVISIONED" # or PAY_PER_REQUEST
  read_capacity  = 1
  write_capacity = 1
  attribute {
    name = "Field"
    type = "S"
  }

  attribute {
    name = "Date"
    type = "S"
  }

}
