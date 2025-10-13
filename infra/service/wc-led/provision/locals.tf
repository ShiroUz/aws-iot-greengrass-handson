locals {
  env = {
    region      = "ap-northeast-1"
    environment = "dev"
    project     = "aws-gg-handson"
  }
  greengrass = {
    wc-led = {
      extra_iot_policy_statement = [
        {
          effect = "Allow"
          actions = [
            "iot:Publish",
            "iot:Receive",
          ]
          resources = [
            "arn:aws:iot:${local.env.region}:${data.aws_caller_identity.self.account_id}:topic/cmd/aws_gg_handson/wc_led/*/weather/*",
            # "arn:aws:iot:${local.env.region}:${data.aws_caller_identity.self.account_id}:topic/*",
          ]
        },
        {
          effect = "Allow"
          actions = [
            "iot:Subscribe",
          ]
          resources = [
            "arn:aws:iot:${local.env.region}:${data.aws_caller_identity.self.account_id}:topicfilter/cmd/aws_gg_handson/wc_led/*/weather/res",
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
        # # Test用に広めに許可
        # {
        #   effect = "Allow"
        #   actions = [
        #     "iot:Publish",
        #     "iot:Subscribe",
        #     "iot:Receive",
        #     "iot:Connect",
        #     # "greengrass:*",
        #   ]
        #   resources = [
        #     "*",
        #   ]
        # }
      ]
      extra_policy_statement = [
        {
          effect = "Allow"
          actions = [
            "s3:ListBucket",
          ]
          resources = [
            "arn:aws:s3:::${local.env.environment}-${local.env.project}-wc-led-tts-${data.aws_caller_identity.self.account_id}",
          ]
        },
        {
          effect = "Allow"
          actions = [
            "s3:GetObject",
          ]
          resources = [
            "arn:aws:s3:::${local.env.environment}-${local.env.project}-wc-led-tts-${data.aws_caller_identity.self.account_id}/*"
          ]
        },
        # {
        #   effect = "Allow"
        #   actions = [
        #     "iot:Publish",
        #     "iot:Receive",
        #   ]
        #   resources = [
        #     "arn:aws:iot:${local.env.region}:${data.aws_caller_identity.self.account_id}:topic/cmd/aws_gg_handson/wc_led/*/weather/*",
        #   ]
        # },
        # {
        #   effect = "Allow"
        #   actions = [
        #     "iot:Subscribe",
        #   ]
        #   resources = [
        #     "arn:aws:iot:${local.env.region}:${data.aws_caller_identity.self.account_id}:topicfilter/cmd/aws_gg_handson/wc_led/*/weather/res",
        #   ]
        # },
        # {
        #   effect = "Allow"
        #   actions = [
        #     "iot:Connect",
        #   ]
        #   resources = [
        #     "arn:aws:iot:${local.env.region}:${data.aws_caller_identity.self.account_id}:client/*",
        #   ]
        # },
        # # Test用に広めに許可
        # {
        #   effect = "Allow"
        #   actions = [
        #     "iot:Publish",
        #     "iot:Subscribe",
        #     "iot:Receive",
        #     "iot:Connect",
        #     # "greengrass:*",
        #   ]
        #   resources = [
        #     "*",
        #   ]
        # }
      ]
    }
  }
}