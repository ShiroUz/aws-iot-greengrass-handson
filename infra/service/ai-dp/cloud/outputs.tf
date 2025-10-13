output "s3_bucket_name" {
  description = "The name of the S3 bucket for storing near-miss images and feedback text/audio"
  value       = { for k, v in module.s3_bucket : k => v.s3_bucket_id }
}

output "s3_bucket_arn" {
  description = "The ARN of the S3 bucket"
  value       = { for k, v in module.s3_bucket : k => v.s3_bucket_arn }
}

output "dynamodb_table_name" {
  description = "The name of the DynamoDB table for near-miss history"
  value       = { for k, v in module.dynamodb_table : k => v.dynamodb_table_id }
}

output "dynamodb_table_arn" {
  description = "The ARN of the DynamoDB table"
  value       = { for k, v in module.dynamodb_table : k => v.dynamodb_table_arn }
}

output "bedrock_inference_profile_id" {
  description = "The ID of the Bedrock Inference Profile"
  value       = aws_bedrock_inference_profile.ai_driving_partner.id
}

output "bedrock_inference_profile_arn" {
  description = "The ARN of the Bedrock Inference Profile"
  value       = aws_bedrock_inference_profile.ai_driving_partner.arn
}

output "ecr_repository_urls" {
  description = "The URLs of the ECR repositories"
  value       = { for k, v in module.ecr : k => v.repository_url }
}

output "ecr_repository_arns" {
  description = "The ARNs of the ECR repositories"
  value       = { for k, v in module.ecr : k => v.repository_arn }
}
