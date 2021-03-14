import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="stacks",
    version="0.0.2",

    description="CDK stacks for an example text classifier API",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Keith Trnka",

    package_dir={"": "stacks"},
    packages=setuptools.find_packages(where="stacks"),

    install_requires=[
        "aws-cdk.core==1.93.0",
        "aws_cdk.aws_apigateway",
        "aws_cdk.aws_lambda"
    ],

    python_requires=">=3.6",
)
