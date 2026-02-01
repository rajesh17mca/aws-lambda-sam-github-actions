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
            "Sid": "CloudFormationDeploy",
            "Effect": "Allow",
            "Action": [
                "cloudformation:CreateStack",
                "cloudformation:UpdateStack",
                "cloudformation:DeleteStack",
                "cloudformation:CreateChangeSet",
                "cloudformation:ExecuteChangeSet",
                "cloudformation:DeleteChangeSet",
                "cloudformation:Describe*",
                "cloudformation:GetTemplate",
                "cloudformation:GetTemplateSummary",
                "cloudformation:ValidateTemplate"
            ],
            "Resource": "arn:aws:cloudformation:us-east-1:096938402899:stack/aws-lambda-github-sam-stack-*/*"
        },
        {
            "Sid": "ServerlessTransformAccess",
            "Effect": "Allow",
            "Action": [
                "cloudformation:CreateChangeSet",
                "cloudformation:DescribeChangeSet",
                "cloudformation:ExecuteChangeSet",
                "cloudformation:DeleteChangeSet",
                "cloudformation:GetTemplate",
                "cloudformation:GetTemplateSummary"
            ],
            "Resource": "*"
        },
        {
            "Sid": "SamArtifactsBucket",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:ListBucket",
                "s3:AbortMultipartUpload",
                "s3:ListMultipartUploadParts"
            ],
            "Resource": [
                "arn:aws:s3:::aws-lambda-github-sam-s3-bucket",
                "arn:aws:s3:::aws-lambda-github-sam-s3-bucket/*"
            ]
        },
        {
            "Sid": "LambdaDeploy",
            "Effect": "Allow",
            "Action": [
                "lambda:CreateFunction",
                "lambda:UpdateFunctionCode",
                "lambda:UpdateFunctionConfiguration",
                "lambda:DeleteFunction",
                "lambda:GetFunction",
                "lambda:PublishVersion",
                "lambda:ListVersionsByFunction",
                "lambda:AddPermission",
                "lambda:RemovePermission",
                "lambda:TagResource",
                "lambda:UntagResource"
            ],
            "Resource": "arn:aws:lambda:us-east-1:096938402899:function:aws-lambda-github-sam-*"
        },
        {
            "Sid": "IamForLambdaExecutionRoles",
            "Effect": "Allow",
            "Action": [
                "iam:CreateRole",
                "iam:DeleteRole",
                "iam:GetRole",
                "iam:PassRole",
                "iam:AttachRolePolicy",
                "iam:DetachRolePolicy"
            ],
            "Resource": "arn:aws:iam::096938402899:role/aws-lambda-github-sam-stack-*"
        },
        {
            "Sid": "IamServiceLinkedRoleForLambda",
            "Effect": "Allow",
            "Action": "iam:CreateServiceLinkedRole",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "iam:AWSServiceName": "lambda.amazonaws.com"
                }
            }
        },
        {
            "Sid": "DenyPrivilegeEscalation",
            "Effect": "Deny",
            "Action": [
                "iam:CreatePolicy",
                "iam:DeletePolicy",
                "iam:PutRolePolicy",
                "iam:UpdateAssumeRolePolicy"
            ],
            "Resource": "*"
        }
    ]
}
```