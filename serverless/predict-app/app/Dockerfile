FROM public.ecr.aws/lambda/python:3.8

COPY app.py requirements.txt ./
COPY model-weights.hdf5 model-weights.hdf5
RUN yum install -y mesa-libGL

RUN python3.8 -m pip install -r requirements.txt -t .

CMD ["app.lambda_handler"]
