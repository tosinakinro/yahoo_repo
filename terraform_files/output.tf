output "bucket_name" {
  value = aws_s3_bucket.my_bucket.bucket
}

output "kms_key_id" {
  value = aws_kms_key.my_key.key_id
}