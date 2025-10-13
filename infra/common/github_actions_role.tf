# Create GitHub Actions Role
data "aws_iam_policy_document" "assume_role" {
  statement {
    actions = [
      "sts:AssumeRoleWithWebIdentity",
    ]
    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values = [
        "repo:${local.role.repository}:*"
      ]
    }
    principals {
      type = "Federated"
      # 
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.self.account_id}:oidc-provider/token.actions.githubusercontent.com"]
    }
  }
}
# Create Image Role
data "aws_iam_policy_document" "images_release_gha_policy" {
  statement {
    sid = "GithubActionsS3SyncPut"
    actions = [
      "s3:PutObject",
    ]
    resources = [
      "arn:aws:s3:::${local.env.environment}-${local.env.project}-images-${data.aws_caller_identity.self.account_id}/*"
    ]
  }
  statement {
    sid = "GithubActionsS3List"
    actions = [
      "s3:ListBucket*",
    ]
    resources = [
      "arn:aws:s3:::${local.env.environment}-${local.env.project}-images-${data.aws_caller_identity.self.account_id}"
    ]
  }
  statement {
    sid = "GithubActionsGetParameterStoreSecrets"
    actions = [
      "ssm:GetParameter*",
    ]
    resources = [
      "arn:aws:ssm:${local.env.region}:${data.aws_caller_identity.self.account_id}:parameter/*"
    ]
    condition {
      test     = "StringEquals"
      variable = "aws:ResourceTag/Project"
      values = [
        "${local.env.project}"
      ]
    }
  }
}

resource "aws_iam_role" "images_release_gha_role" {
  name               = "${local.env.project}-images-release-gha-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_policy" "images_release_gha_policy" {
  name   = "${local.env.project}-images-release-gha-policy"
  policy = data.aws_iam_policy_document.images_release_gha_policy.json
}

resource "aws_iam_role_policy_attachment" "images_release_gha_policy_attachment" {
  role       = aws_iam_role.images_release_gha_role.name
  policy_arn = aws_iam_policy.images_release_gha_policy.arn
}

## Greengrass Release Role
data "aws_iam_policy_document" "gg_component_release_gha_policy" {
  statement {
    sid = "ECRPush"
    actions = [
      "ecr:CompleteLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:InitiateLayerUpload",
      "ecr:BatchCheckLayerAvailability",
      "ecr:PutImage",
      "ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer",
      "ecr:DescribeRepositories",
      "ecr:ListImages"
    ]
    resources = [
      "arn:aws:ecr:${local.env.region}:${data.aws_caller_identity.self.account_id}:repository/${local.env.project}*"
    ]
  }
  statement {
    sid = "ECRAuth"
    actions = [
      "ecr:GetAuthorizationToken",
    ]
    resources = [
      "*"
    ]
  }
  statement {
    sid = "UploadGreengrassComponents"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]
    resources = [
      "arn:aws:s3:::*-${local.env.project}-gg-components-${data.aws_caller_identity.self.account_id}/*"
    ]
  }
  statement {
    sid = "S3ListComponent"
    actions = [
      # "s3:CreateBucket",
      "s3:GetBucketLocation",
      "s3:ListBucket",
    ]
    resources = [
      "arn:aws:s3:::*-${local.env.project}-gg-components-${data.aws_caller_identity.self.account_id}"
    ]
  }
  statement {
    sid = "GreengrassCreateComponentsVersion"
    actions = [
      "greengrass:CreateComponentVersion",
    ]
    resources = [
      "arn:aws:greengrass:${local.env.region}:${data.aws_caller_identity.self.account_id}:components:*"
    ]
  }
  statement {
    sid = "GreengrassReadDeleteComponentsVersion"
    actions = [
      "greengrass:DeleteComponent",
      "greengrass:GetComponent",
      "greengrass:DescribeComponent",
      "greengrass:ListComponentVersions",
      "greengrass:ListComponents",
    ]
    resources = [
      "*"
    ]
  }
}
resource "aws_iam_role" "gg_component_release_gha_role" {
  name               = "${local.env.project}-gg-component-release-gha-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}
resource "aws_iam_policy" "gg_component_release_gha_policy" {
  name   = "${local.env.project}-gg-component-release-gha-policy"
  policy = data.aws_iam_policy_document.gg_component_release_gha_policy.json
}
resource "aws_iam_role_policy_attachment" "gha_ecr_push_policy_attachment" {
  role       = aws_iam_role.gg_component_release_gha_role.name
  policy_arn = aws_iam_policy.gg_component_release_gha_policy.arn
}

### Greengrass Deployment Role
data "aws_iam_policy_document" "gg_component_deploy_gha_policy" {
  statement {
    sid = "IoTThingGroup"
    actions = [
      "iot:DescribeThingGroup",
      "iot:CreateJob",
    ]
    resources = [
      "arn:aws:iot:${local.env.region}:${data.aws_caller_identity.self.account_id}:thinggroup/*"
    ]
  }
  statement {
    sid = "IoTJobs"
    actions = [
      "iot:DescribeJob",
      "iot:CreateJob",
      "iot:CancelJob",
    ]
    resources = [
      "arn:aws:iot:${local.env.region}:${data.aws_caller_identity.self.account_id}:job/*"
    ]
  }
  statement {
    sid = "S3UploadGreengrassComponents"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]
    resources = [
      "arn:aws:s3:::*-${local.env.project}-gg-components-${data.aws_caller_identity.self.account_id}/*"
    ]
  }
  statement {
    sid = "S3PublishComponent"
    actions = [
      # "s3:CreateBucket",
      "s3:GetBucketLocation",
      "s3:ListBucket",
    ]
    resources = [
      "arn:aws:s3:::*-${local.env.project}-gg-components-${data.aws_caller_identity.self.account_id}"
    ]
  }
  statement {
    sid = "GreengrassCreateComponentsVersion"
    actions = [
      "greengrass:CreateComponentVersion",
    ]
    resources = [
      "*"
    ]
  }
  statement {
    sid = "GreengrassListComponents"
    actions = [
      "greengrass:ListComponentVersions",
    ]
    resources = [
      "*"
    ]
  }
  statement {
    sid = "GreengrassDeployment"
    actions = [
      "greengrass:CreateDeployment",
      "greengrass:TagResource",
      "iot:DescribeJob",
      "iot:DescribeThing",
      "iot:GetThingShadow",
      "iot:UpdateJob",
      "iot:UpdateThingShadow"
    ]
    resources = [
      "*"
    ]
  }
}

resource "aws_iam_role" "gg_component_deploy_gha_role" {
  name               = "${local.env.project}-gg-component-deploy-gha-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_policy" "gg_component_deploy_gha_policy" {
  name   = "${local.env.project}-gg-component-deploy-gha-policy"
  policy = data.aws_iam_policy_document.gg_component_deploy_gha_policy.json
}

resource "aws_iam_role_policy_attachment" "gha_gg_poc_policy_attachment" {
  role       = aws_iam_role.gg_component_deploy_gha_role.name
  policy_arn = aws_iam_policy.gg_component_deploy_gha_policy.arn
}

