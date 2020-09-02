FROM continuumio/anaconda3:latest
RUN apt-get install -y nodejs npm git tmux libpq-dev

COPY requirements.txt /init/requirements.txt
RUN pip3 install -r /init/requirements.txt

#COPY ./ibapi /init/ibapi
#WORKDIR /init/ibapi
#RUN python3 setup.py install
RUN pip3 install ib_insync
WORKDIR /

RUN jupyter contrib nbextension install --user
RUN jupyter nbextension enable --py --sys-prefix qgrid
RUN jupyter nbextension enable --py --sys-prefix widgetsnbextension
RUN jt -t monokai -f fira -fs 13 -nf ptsans -nfs 11 -N -kl -cursw 5 -cursc r -cellw 95% -T

ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["jupyter", "notebook", "--no-browser", "--port=8888","--ip=0.0.0.0", "--allow-root","--NotebookApp.token=''"]