resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}


resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-unique-yahoo-bucket-name-${random_string.suffix.result}"

}

resource "aws_s3_bucket_versioning" "my_bucket_versioning" {
  bucket = aws_s3_bucket.my_bucket.bucket
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_kms_key" "my_key" {
  description             = "KMS key for S3 encryption"
  deletion_window_in_days = 14
}


