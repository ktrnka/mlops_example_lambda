# This will install or upgrade an install
# Note: This doesn't work on github actions (ubuntu); it needs to run under sudo there
install-cdk:
	npm install -g aws-cdk@latest


# commands to get DVC setup
# totally untested if you can run this as-is
#setup-dvc:
#	cd infrastructure && terraform init && terraform plan && terraform apply


# env just for development that has pretty much everything so I don't need to maintain 3 local envs
# SYSTEM_VERSION_COMPAT=1 is a workaround for python modules that don't install correctly on Big Sur
setup-development-pipenv:
	rm -rf Pipfile
	SYSTEM_VERSION_COMPAT=1 pipenv --python 3.8
	SYSTEM_VERSION_COMPAT=1 pipenv install --skip-lock -r training/requirements.txt
	SYSTEM_VERSION_COMPAT=1 pipenv install --skip-lock -r serving/app/requirements.txt

	# maybe pipenv doesn't support this style? it throws a syntax error trying to parse the setup.py reference
	#SYSTEM_VERSION_COMPAT=1 cd serving/deployment/ && pipenv install --skip-lock -r requirements.txt

# run this inside the virtual environment
train:
	dvc repro train

# run this inside the virtual environment
test-service:
	PYTHONPATH=serving/app/ python serving/tests/test_lambda_handler.py
