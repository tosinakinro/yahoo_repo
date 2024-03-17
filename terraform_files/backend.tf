terraform {
  backend "s3" {
    bucket         = "luji-tf-state"
    key            = "yahoo_assessment/terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "tf-efuse-locks"
    encrypt        = true
    }
}