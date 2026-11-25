FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.14

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ ./

RUN chmod -R a+rX .

CMD [ "cfn_secret_handler.handler" ]
