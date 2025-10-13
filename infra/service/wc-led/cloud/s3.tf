module "s3_bucket" {
  source   = "terraform-aws-modules/s3-bucket/aws"
  for_each = { for k, v in try(local.s3, {}) : k => v }
  bucket   = try("${each.value.bucket_name}", "${local.env.environment}-${local.env.project}-wc-led-${each.key}-${data.aws_caller_identity.self.account_id}")

  control_object_ownership = true
  object_ownership         = "BucketOwnerEnforced"
  versioning = {
    enabled = each.value.versioning
  }
  server_side_encryption_configuration = try(each.value.server_side_encryption_configuration, {})
  lifecycle_rule                       = try(each.value.lifecycle_rule, [])
}