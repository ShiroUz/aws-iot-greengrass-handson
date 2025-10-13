data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

resource "aws_bedrock_inference_profile" "ai_driving_partner" {
  name        = "aiDrivingPartnerProfile"
  description = "Profile with tag for cost allocation tracking"

  model_source {
    copy_from = "arn:aws:bedrock:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:inference-profile/apac.amazon.nova-pro-v1:0"
    # Include account ID to use inference profiles
    # copy_from = "arn:aws:bedrock:eu-central-1:${data.aws_caller_identity.current.account_id}:inference-profile/eu.anthropic.claude-3-5-sonnet-20240620-v1:0"
  }
}


# Execution Role for Nova
# resource "aws_iam_role" "nova_execution_role" {
#   name = "${local.env.project}-nova-execution-role"

#   assume_role_policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Action = "sts:AssumeRole"
#         Effect = "Allow"
#         Principal = {
#           Service = "application-inference.amazonaws.com"
#         }
#       }
#     ]
#   })
# }

# # Policy for Nova to access S3
# resource "aws_iam_policy" "nova_s3_access" {
#   name        = "${local.env.project}-nova-s3-access"
#   description = "Allow Nova to access S3 bucket for near-miss images"

#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Action = [
#           "s3:GetObject",
#           "s3:PutObject",
#           "s3:ListBucket"
#         ]
#         Effect   = "Allow"
#         Resource = [
#           module.s3_bucket.s3_bucket_arn,
#           "${module.s3_bucket.s3_bucket_arn}/*"
#         ]
#       }
#     ]
#   })
# }

# # Attach policy to role
# resource "aws_iam_role_policy_attachment" "nova_s3_access_attachment" {
#   role       = aws_iam_role.nova_execution_role.name
#   policy_arn = aws_iam_policy.nova_s3_access.arn
# }