locals {
  env = {
    environment = "dev"
    project     = "aws-gg-handson"
    region      = "ap-northeast-1"
  }
  iot = {
    rule = {
      weather_command = {
        sql = "SELECT * FROM 'cmd/aws_gg_handson/wc_led/+/weather/req'"
        lambda = [
          {
            function_arn = "arn:aws:lambda:${local.env.region}:${data.aws_caller_identity.self.account_id}:function:${local.env.environment}-${local.env.project}-wc-led-e-weather-check"
          }
        ]
      }
    }
  }
  dynamodb = {
    device-address = {
      hash_key = "ThingId"

      attributes = [
        {
          name = "ThingId"
          type = "S"
        }
      ]
      ttl = {
        # attribute_name = null
        ttl_enabled = false
      }
      server_side_encryption_enabled = true
    }
  }
  s3 = {
    tts = {
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
        }
        noncurrent_version_expiration = {
          noncurrent_days = 1
        }
      }]
    }
  }
  cloudwatch = {
    log_group = {
      weather_check = {
        name              = "/aws/greengrass/UserComponent/${local.env.region}/com.ShiroUz.WeatherCheckLED"
        retention_in_days = 7
      }
      system = {
        name              = "/aws/greengrass/GreengrassSystemComponent/${local.env.region}/System"
        retention_in_days = 7
      }
    }
  }
  ecr = {
    repository = {
      wc_led = {
        name                 = "wc-led"
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
      python_base_image = {
        name                 = "wc-led/arm32v7/python"
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