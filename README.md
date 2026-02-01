# aws-lambda-github-actions

### Step 1: Create Identity provider
1. Login to AWS Console
2. Go to IAM → Identity providers
3. Click Add Provider
    * Provider Type: OpenID Connect
    * Provider URL: https://token.actions.githubusercontent.com
    * Audience: sts.amazonaws.com
4. Click Add provider

### Step 2: Create IAM Role for GitHub Actions
1. Login to AWS Console
2. Go to IAM → Roles
3. Click Create role
4. Select Web identity and Choose:
    * Identity provider: token.actions.githubusercontent.com
    * Audience: sts.amazonaws.com
    * GitHub Org Name: <>
    * Github repository
    * Github Branch 

### Step 3: Configure Trust Policy - Review
This should build automatically but it is good to review
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<YOUR_ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:<ORG>/<REPO>:ref:refs/heads/main"
        }
      }
    }
  ]
}
```

### Step 4: Attach Permissions Policy (Least Privilege)
Attach the IAM Policy which required for the AWS Lambda function deploymnenbt:
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CloudFormation",
      "Effect": "Allow",
      "Action": [
        "cloudformation:*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "Lambda",
      "Effect": "Allow",
      "Action": [
        "lambda:GetFunction",
        "lambda:CreateFunction",
        "lambda:UpdateFunctionCode",
        "lambda:UpdateFunctionConfiguration",
        "lambda:PublishVersion",
        "lambda:CreateAlias",
        "lambda:UpdateAlias"
      ],
      "Resource": "arn:aws:lambda:*:*:function:my-lambda-*"
    },
    {
      "Sid": "IAMPassRole",
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::*:role/lambda-execution-role-*"
    },
    {
      "Sid": "S3Artifacts",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::sam-artifacts-bucket",
        "arn:aws:s3:::sam-artifacts-bucket/*"
      ]
    }
  ]
}
```