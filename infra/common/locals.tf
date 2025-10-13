locals {
  env = {
    region      = "ap-northeast-1"
    environment = "dev"
    project     = "aws-gg-handson"
  }
  s3 = {
    tfstate = {
      versioning = "false"
      server_side_encryption_configuration = {
        rule = {
          apply_server_side_encryption_by_default = {
            sse_algorithm = "AES256"
          }
        }
      }
      expected_bucket_owner = "BucketOwnerPreferred"
    }
    images = {
      versioning = "true"
      server_side_encryption_configuration = {
        rule = {
          apply_server_side_encryption_by_default = {
            sse_algorithm = "AES256"
          }
        }
      }
      expected_bucket_owner = "BucketOwnerPreferred"
    }
    gg-components = {
      versioning = "true"
      server_side_encryption_configuration = {
        rule = {
          apply_server_side_encryption_by_default = {
            sse_algorithm = "AES256"
          }
        }
      }
      expected_bucket_owner = "BucketOwnerPreferred"
    }
    app-resources = {
      versioning = "true"
      server_side_encryption_configuration = {
        rule = {
          apply_server_side_encryption_by_default = {
            sse_algorithm = "AES256"
          }
        }
      }
      expected_bucket_owner = "BucketOwnerPreferred"
    }
  }
  role = {
    repository = "ShiroUz/aws-iot-greengrass-handson" # TODO: If you execute Change Definition
  }
}
