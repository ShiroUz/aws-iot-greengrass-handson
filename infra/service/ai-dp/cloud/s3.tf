data "aws_caller_identity" "self" {}
module "s3_bucket" {
  source   = "terraform-aws-modules/s3-bucket/aws"
  for_each = { for k, v in try(local.s3, {}) : k => v }
  bucket   = try("${each.value.bucket_name}", "${local.env.environment}-${local.env.project}-ai-dp-${each.key}-${data.aws_caller_identity.self.account_id}")

  control_object_ownership = true
  object_ownership         = "BucketOwnerEnforced"
  versioning = {
    enabled = each.value.versioning
  }
  server_side_encryption_configuration = try(each.value.server_side_encryption_configuration, {})
  lifecycle_rule                       = try(each.value.lifecycle_rule, [])
}

resource "aws_s3_bucket_notification" "ai_driving_partner_bucket_notification" {
  bucket      = module.s3_bucket["content"].s3_bucket_id
  eventbridge = true
  depends_on  = [module.s3_bucket]
}