terraform {
  required_version = ">= 0.14.9"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.14"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 2.0"
    }
  }
}