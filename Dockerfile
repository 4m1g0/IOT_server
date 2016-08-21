FROM ubuntu

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install xmltodict requests
    
EXPOSE 8080 8081 9000

ADD *.py *.sh ./
ADD pricingServer/*.py ./pricingServer/ 

CMD ["/bin/bash", "/start.sh"]

