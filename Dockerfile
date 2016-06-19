FROM ubuntu

RUN apt-get update && \
    apt-get install -y python3 && \
    rm -rf /var/lib/apt/lists/*
    
EXPOSE 8080 8081

ADD *.py ./

CMD python3 Main.py 8080 8081


