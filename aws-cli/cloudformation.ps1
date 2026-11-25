aws cloudformation create-stack --stack-name Sandbox `
    --template-body file://cloudformation\cicd-pipeline.yaml `
    --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND `
    --region us-east-1 --profile 831603884703_AWS-Analyzer-Admin
