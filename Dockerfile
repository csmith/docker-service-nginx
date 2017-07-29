FROM csmith/service-reporter-lib:latest 
MAINTAINER Chris Smith <dke@chameth.com> 

RUN \
  pip install \
    jinja2

COPY *.py *.tpl /

VOLUME ["/nginx-config"]
ENTRYPOINT ["python", "/generate.py"]
