FROM centos:centos7
ENV PATH=/usr/lib:$PATH

#RUN yum install java-11-openjdk -y 
RUN yum install wget -y 
RUN yum install glibc -y

RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.1-linux-aarch64.tar.gz \
    && wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.1-linux-aarch64.tar.gz.sha512 
RUN yum install perl-Digest-SHA -y 
RUN shasum -a 512 -c elasticsearch-7.17.1-linux-aarch64.tar.gz.sha512 \ 
    && tar -xzf elasticsearch-7.17.1-linux-aarch64.tar.gz \
    && yum upgrade -y
    
RUN rm elasticsearch-7.17.1-linux-aarch64.tar.gz \
    && rm elasticsearch-7.17.1-linux-aarch64.tar.gz.sha512
    
ADD elasticsearch.yml /elasticsearch-7.17.1/config/
ENV ES_HOME=/elasticsearch-7.17.1
RUN groupadd elasticsearch \
    && useradd -g elasticsearch elasticsearch
    
RUN mkdir /var/lib/logs \
    && chown elasticsearch:elasticsearch /var/lib/logs \
    && mkdir /var/lib/data \
    && chown elasticsearch:elasticsearch /var/lib/data \
    && chown -R elasticsearch:elasticsearch /elasticsearch-7.17.1/
RUN mkdir /elasticsearch-7.17.1/snapshots \
    && chown elasticsearch:elasticsearch /elasticsearch-7.17.1/snapshots
    
USER elasticsearch
CMD ["/usr/sbin/init"]
CMD ["/elasticsearch-7.17.1/bin/elasticsearch"]
