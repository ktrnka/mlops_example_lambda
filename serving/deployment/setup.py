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

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
