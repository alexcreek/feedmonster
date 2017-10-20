FROM python:2
LABEL name='feedmonster' \
      version='1'
RUN pip install --upgrade feedparser
ADD feedmonster.py /mnt/
WORKDIR /mnt
CMD python feedmonster.py
