FROM continuumio/anaconda3:latest
RUN apt-get install -y nodejs npm git tmux libpq-dev python-tablib

COPY req0.txt /init/req0.txt
RUN pip3 install -r /init/req0.txt

COPY requirements.txt /init/requirements.txt
RUN pip3 install -r /init/requirements.txt

#RUN apt-get install -y wget
#COPY ta-lib.sh /init/ta-lib.sh
#RUN chmod +x /init/ta-lib.sh
#WORKDIR /init/
#RUN ./ta-lib.sh
#RUN pip3 install TA-lib

#COPY ./ibapi /init/ibapi
#WORKDIR /init/ibapi
#RUN python3 setup.py install

WORKDIR /
RUN pip3 install ib_insync


RUN jupyter contrib nbextension install --user
RUN jupyter nbextension enable --py --sys-prefix qgrid
RUN jupyter nbextension enable --py --sys-prefix widgetsnbextension
RUN jt -t monokai -f fira -fs 13 -nf ptsans -nfs 11 -N -kl -cursw 5 -cursc r -cellw 95% -T

ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["jupyter", "notebook", "--no-browser", "--port=8888","--ip=0.0.0.0", "--allow-root","--NotebookApp.token=''"]