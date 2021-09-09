# s3 global namespace for buckets makes this tricky, we want to ensure that we
# can know which buckets we've created for a specific run so we can't use bucket_prefix
# as it assigns a random string to the end of each bucket name instead of a random
# number for all the created buckets

resource "random_integer" "random" {
  min = 1
  max = 50000
}

resource "aws_s3_bucket" "example_a" {
  bucket = "c7n-aws-s3-encryption-audit-test-a-${random_integer.random.result}"
  acl    = "private"
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "aws:kms"
      }
    }
  }
}

resource "aws_s3_bucket" "example_b" {
  bucket = "c7n-aws-s3-encryption-audit-test-b-${random_integer.random.result}"
  acl    = "private"
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket" "example_c" {
  bucket = "c7n-aws-s3-encryption-audit-test-c-${random_integer.random.result}"
  acl    = "private"
}
