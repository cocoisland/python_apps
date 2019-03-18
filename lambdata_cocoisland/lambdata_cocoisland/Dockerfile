FROM debian

# So logging/io works reliably w/ Docker
ENV PYTHONBUFFERED=1

### Basic Python dev dependencies
RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install python3-pip curl -y && \
  pip3 install pandas  && \
  pip3 install -i https://test.pypi.org/simple lambdata-cocoisland && \
  python3 -c "import lambdata_cocoisland ; print(lambdata_cocoisland)"
