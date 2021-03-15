This repo is another in my series of MLops examples to show the basics, such as:
* Saving and loading a trained model
* Versioning models
* scikit-learn pipelines to bundle preprocessing and modeling
* Serving a model from a web service
* Hosting the web service
* Pull request / review concepts, like reviewing a model build, reviewing service changes, and basic testing for the service

This repo uses CDK for deployment to AWS Lambda with Docker. I saw a recent AWS blog post on how you can make Docker images up to 10 GB in size, and it showed a demo of using that to deploy a fairly large machine learning package.

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
