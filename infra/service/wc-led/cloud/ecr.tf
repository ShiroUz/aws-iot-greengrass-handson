module "ecr" {
  source          = "terraform-aws-modules/ecr/aws"
  for_each        = { for k, v in local.ecr.repository : k => v if local.env.environment == "dev" }
  repository_name = "${local.env.project}/${each.value.name}"

  repository_lifecycle_policy = jsonencode({
    rules = each.value.lifecycle_policy.rules
  })
}