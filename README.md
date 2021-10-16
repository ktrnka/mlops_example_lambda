This repo is another in my series of MLops examples to show the basics, such as:
* Saving and loading a trained model
* Versioning models
* scikit-learn pipelines to bundle preprocessing and modeling
* Serving a model from a web service
* Hosting the web service
* Pull request / review concepts, like reviewing a model build, reviewing service changes, and basic testing for the service

This repo uses CDK for deployment to AWS Lambda with Docker. I saw a recent AWS blog post on how you can make Docker images up to 10 GB in size, and it showed a demo of using that to deploy a fairly large machine learning package.

# Setup

I've only set this up once so take this with a grain of salt.

1. Install Terraform and run the code in `infrastructure`. This creates an S3 bucket for DVC and an IAM user for Github Actions. Be sure to find and save: the S3 bucket name, the IAM user ID, and the IAM user secret key.
1. Edit `.dvc/config` and point it to your new S3 bucket.
1. Setup `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in your Github Secrets for the repo so Github Actions can use them.
1. If you haven't run `cdk bootstrap` on your AWS account, do that.
1. Train a model - it's probably easiest to edit anything under `training` and make a PR to trigger github to build it
1. After it's done training and you merge it, it'll deploy to your AWS account.

# What's where?

* `.dvc`: Configuration for DVC, which is how we version models and link the model versions to git
* `.github`: Configuration for the CI/CD pipeline in Github Actions
* `infrastructure`: This sets up AWS resources for the repo and makes a user to run the deployments
* `serving/app`: The actual lambda service code
* `serving/app/data`: The model is stored here
* `serving/deployment`: CDK code to create resources needed for hosting the model and deploy the code/data
* `serving/tests`: Minimal test to make sure the code can load the model
* `training`: Code to build the model

# TO DO
- Organize the infrastructure code better. Right now there's some in serving and some in infrastructure. Some code needs to be run once to set things up, like cdk bootstrap and Terraform. Other code is run on each deploy.
- dev/staging/prod
- Try 10 GB RAM, which also scales the CPU. Test to see how it performs with that.
- DVC installs slowly on Github Actions and adds about 30 seconds each time
- It's too much work to get to logs in AWS console. I bet there's a way to pull the right IDs from CDK and use AWS CLI to watch logs.
- Reduce the permissions available to the IAM user for Github Actions

# Notes on deploying to Lambda

## Good

* It's inexpensive
* It automatically scales up the number of instances without any configuration

## Bad

* If you don't have much volume, it can autoscale down to zero. That saves money but you get a high percent of requests as cold starts: Lambda loads the machine learning model from scratch before handling the request.
* It's hard to set timeouts correctly - cold starts can easily take 30 seconds, and you can't figure it out on your local machine
* Compared to Flask in Docker, it's more work to set up the API for validation and documentation

# Cloudwatch EMF Notes

* aws-embedded-metrics
  * It doesn't add many dependencies!
  * Default dimensions: LogGroup, ServiceName, ServiceType (an example is below)
  * You have to set the namespace manually if you want it to be the function name.
  * You have to set the execution environment to "local" when testing to ensure that it doesn't try opening a bunch of sockets to try streaming cloudwatch logs

## Example EMF log

```{
    "LogGroup": "ExampleTextClassifierStac-ExampleTextClassifierHan-PZQ8yd6C6x3R",
    "ServiceName": "ExampleTextClassifierStac-ExampleTextClassifierHan-PZQ8yd6C6x3R",
    "ServiceType": "AWS::Lambda::Function",
    "executionEnvironment": "AWS_Lambda_python3.8",
    "memorySize": "3008",
    "functionVersion": "$LATEST",
    "logStreamId": "2021/10/16/[$LATEST]f35168a9ad9e40e39422fb6be26a5800",
    "_aws": {
        "Timestamp": 1634401767050,
        "CloudWatchMetrics": [
            {
                "Dimensions": [
                    [
                        "LogGroup",
                        "ServiceName",
                        "ServiceType"
                    ]
                ],
                "Metrics": [
                    {
                        "Name": "input.num_chars",
                        "Unit": "Count"
                    }
                ],
                "Namespace": "aws-embedded-metrics"
            }
        ]
    },
    "input.num_chars": 66
}
```