FROM alpine:latest
RUN apk add --no-cache bash curl build-base python-dev py-pip openssl-dev libffi-dev
RUN pip install pandas==0.21.0 gunicorn ansible_runner falcon ansible avisdk avimigrationtools
RUN ansible-galaxy avinetworks.avisdk avinetworks.aviconfig
RUN mkdir /opt/falcon_runner
COPY falcon_runner /opt/falcon_runner
RUN mkdir /opt/modules
COPY modules /opt/modules
CMD ["gunicorn","-b :5000", "api:app", "--chdir /opt/falcon_runner/", "--timeout 300"]
