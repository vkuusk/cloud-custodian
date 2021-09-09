resource "aws_s3_bucket" "example" {
  bucket_prefix = "my-custodian-test-bucket"
  acl    = "private"

  tags = {
    original-tag = "original-value"
  }
}
