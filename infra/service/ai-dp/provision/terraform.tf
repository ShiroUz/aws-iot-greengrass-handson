terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
  backend "s3" {
    bucket = "dev-aws-gg-handson-tfstate-xxxxxxxxxxxxx"
    key    = "dev.tfstate"
    region = "ap-northeast-1"
  }
}
