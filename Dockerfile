FROM python:3.9-slim

#makedir to download repoo
RUN mkdir /kandula
COPY . /kandula/

WORKDIR /kandula
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000

CMD ["/bin/bash", "bin/run"]