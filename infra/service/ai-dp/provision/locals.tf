locals {
  env = {
    region      = "ap-northeast-1"
    environment = "dev"
    project     = "aws-gg-handson"
  }
  greengrass = {
    ai-dp = {
      extra_iot_policy_statement = [
        {
          effect = "Allow"
          actions = [
            "iot:Receive",
          ]
          resources = [
            "arn:aws:iot:${local.env.region}:${data.aws_caller_identity.self.account_id}:topic/cmd/aws_gg_handson/ai_dp/*/near-miss/feedback",
          ]
        },
        {
          effect = "Allow"
          actions = [
            "iot:Subscribe",
          ]
          resources = [
            "arn:aws:iot:${local.env.region}:${data.aws_caller_identity.self.account_id}:topicfilter/cmd/aws_gg_handson/ai_dp/*/near-miss/feedback",
          ]
        },
        {
          effect = "Allow"
          actions = [
            "iot:Connect",
          ]
          resources = [
            "arn:aws:iot:${local.env.region}:${data.aws_caller_identity.self.account_id}:client/*",
          ]
        },
      ]
      extra_policy_statement = [
        {
          effect = "Allow"
          actions = [
            "s3:ListBucket",
          ]
          resources = [
            "arn:aws:s3:::${local.env.environment}-${local.env.project}-ai-dp-content-${data.aws_caller_identity.self.account_id}",
          ]
        },
        {
          effect = "Allow"
          actions = [
            "s3:GetObject",
            "s3:PutObject",
          ]
          resources = [
            "arn:aws:s3:::${local.env.environment}-${local.env.project}-ai-dp-content-${data.aws_caller_identity.self.account_id}/*"
          ]
        },
      ]
      things_amount = 1
    }
  }
}