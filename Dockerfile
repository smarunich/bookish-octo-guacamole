FROM alpine:latest
RUN apk add --no-cache bash curl build-base python-dev py-pip openssl-dev libffi-dev
RUN pip install pandas==0.21.0 gunicorn ansible_runner falcon ansible avisdk avimigrationtools
RUN ansible-galaxy install avinetworks.avisdk avinetworks.aviconfig
RUN mkdir /opt/falcon_runner
COPY falcon_runner /opt/falcon_runner
RUN mkdir /opt/modules
COPY modules /opt/modules
EXPOSE 5000
RUN echo '/usr/bin/gunicorn app:api -b 0.0.0.0:5000 --timeout 300 --chdir /opt/falcon_runner' > /opt/falcon_runner/gunicorn.sh
RUN chmod a+x /opt/falcon_runner/gunicorn.sh
CMD ["/opt/falcon_runner/gunicorn.sh"]
