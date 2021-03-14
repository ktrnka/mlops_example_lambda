provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "b" {
  bucket_prefix = "trnka-dvc-"
  acl = "private"
}

resource "aws_iam_user" "github_actions" {
  name = "github_actions_lambda_ml"
  force_destroy = true
}

resource "aws_iam_user_policy" "dvc_policy" {
  name = "dvc_policy"
  user = aws_iam_user.github_actions.name

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": ["arn:aws:s3:::${aws_s3_bucket.b.bucket}"]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": ["arn:aws:s3:::${aws_s3_bucket.b.bucket}/*"]
    }
  ]
}

EOF
}

// note: It looks like this does wildcard on anything called via cloud formation which seems sketchy
resource "aws_iam_user_policy" "cdk_policy" {
  name = "cdk_policy"
  user = aws_iam_user.github_actions.name

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
        {
            "Action": [
                "cloudformation:*"
            ],
            "Resource": "*",
            "Effect": "Allow"
        },
        {
            "Condition": {
                "ForAnyValue:StringEquals": {
                    "aws:CalledVia": [
                        "cloudformation.amazonaws.com"
                    ]
                }
            },
            "Action": "*",
            "Resource": "*",
            "Effect": "Allow"
        },
        {
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::cdktoolkit-stagingbucket-*",
            "Effect": "Allow"
        }

  ]
}

EOF
}

resource "aws_iam_access_key" "github_actions" {
  user = aws_iam_user.github_actions.name
}

output "secret" {
  value = aws_iam_access_key.github_actions.secret
}