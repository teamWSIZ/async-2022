# creates a deployable image of "clouddrive" image

FROM python:3.10.9-alpine3.17

# docker build -t wsiz/clouddrive:0.0.1 .

# Create app directory
WORKDIR /usr/src/app


# Bundle app source
COPY clouddrive_controller.py /usr/src/app/
COPY utils.py /usr/src/app/
COPY requirements.txt /usr/src/app/

RUN pip install -r requirements.txt
EXPOSE 4001
CMD [ "python", "-u", "clouddrive_controller.py" ]
