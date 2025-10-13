locals {
  env = {
    environment = "dev"
    project     = "aws-gg-handson"
    region      = "ap-northeast-1"
  }
  s3 = {
    content = {
      versioning = "false"
      server_side_encryption_configuration = {
        rule = {
          apply_server_side_encryption_by_default = {
            sse_algorithm = "AES256"
          }
        }
      }
      expected_bucket_owner = "BucketOwnerPreferred"
      lifecycle_rule = [{
        id     = "delete_7_days"
        status = "Enabled"
        expiration = {
          days = 7
          # expired_object_delete_marker = true
        }
        noncurrent_version_expiration = {
          noncurrent_days = 1
        }
      }]
    }
  }
  dynamodb = {
    near-miss = {
      hash_key  = "ThingId"
      range_key = "Timestamp"

      attributes = [
        {
          name = "ThingId"
          type = "S"
        },
        # TimestampはUNIX時間(秒), UTCで保存する。
        {
          name = "Timestamp"
          type = "N"
        }
      ]
      ttl = {
        ttl_attribute_name = "ExpirationTime"
        ttl_enabled        = true
      }
      server_side_encryption_enabled = true
    }
  }
  ecr = {
    repository = {
      ai-driving-partner = {
        name                 = "ai-dp"
        image_tag_mutability = "IMMUTABLE"
        lifecycle_policy = {
          rules = [{
            rulePriority = 1
            description  = "Keep last 30 images"
            selection = {
              countType     = "imageCountMoreThan"
              countNumber   = 30
              tagStatus     = "tagged"
              tagPrefixList = ["v"]
            }
            action = {
              type = "expire"
            }
          }]
        }
      }
      python-base-image = {
        name                 = "ai-dp/arm32v7/python"
        image_tag_mutability = "IMMUTABLE"
        lifecycle_policy = {
          rules = [{
            rulePriority = 1
            description  = "Delete images older than 365 days"
            selection = {
              countType     = "imageCountMoreThan"
              countNumber   = 365
              tagStatus     = "tagged"
              tagPrefixList = ["v"]
            }
            action = {
              type = "expire"
            }
          }]
        }
      }
    }
  }
}