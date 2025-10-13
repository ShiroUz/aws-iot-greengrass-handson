provider "aws" {
  region = local.env.region

  default_tags {
    tags = {
      Environment = local.env.environment
      Project     = local.env.project
      SubSID      = "common"
    }
  }
}
