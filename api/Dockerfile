FROM public.ecr.aws/lambda/python:3.8

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}
COPY key.json ${LAMBDA_TASK_ROOT}
COPY data/ ${LAMBDA_TASK_ROOT}/data/
RUN mkdir -p /tmp/data/wiki
# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Perform Data Init

# COPY init_models.py ${LAMBDA_TASK_ROOT}
# RUN mkdir -p ${LAMBDA_TASK_ROOT}/models/
#RUN python3 ${LAMBDA_TASK_ROOT}/init_models.py

# Copy Models
COPY models/ ${LAMBDA_TASK_ROOT}/models/

# Copy Pickles
COPY *.pickle ${LAMBDA_TASK_ROOT}

# Copy SAVs
COPY *.sav ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]
