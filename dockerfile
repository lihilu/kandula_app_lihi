FROM python:3.9-slim

RUN useradd -ms /bin/bash kandulaproject
USER kandulaproject
WORKDIR /home/kandulaproject

RUN mkdir /kandula

COPY . /kandula/

WORKDIR /kandula
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["/bin/bash", "bin/run"]


