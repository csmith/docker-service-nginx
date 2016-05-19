FROM csmith/service-reporter-lib:latest 
MAINTAINER Chris Smith <chris87@gmail.com> 

RUN \
  pip install \
    jinja2

COPY *.py *.tpl /

VOLUME ["/nginx-config"]
ENTRYPOINT ["python", "/generate.py"]
