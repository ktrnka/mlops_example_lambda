FROM public.ecr.aws/lambda/python:3.8

# requirements
COPY requirements.txt ./
RUN python3.8 -m pip install --no-cache-dir -r requirements.txt

# code
COPY app.py ./

# data
COPY data ./data

# This reduces joblib warnings.
# Some docs say it'll speed things up, others say it'll slow things down. I've only done 1 test
#ENV OPENBLAS_NUM_THREADS=1

CMD ["app.lambda_handler"]
