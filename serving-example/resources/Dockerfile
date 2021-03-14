FROM public.ecr.aws/lambda/python:3.8

# requirements
COPY requirements.txt ./
RUN python3.8 -m pip install -r requirements.txt

# code
COPY app.py ./

# data
COPY data ./data

# maybe this will silence joblib warnings
ENV OPENBLAS_NUM_THREADS=1

CMD ["app.lambda_handler"]
