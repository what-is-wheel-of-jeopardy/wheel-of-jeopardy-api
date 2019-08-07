FROM python:3.6
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 81
RUN python test.py
CMD ["gunicorn", "-b", "0.0.0.0:81", "app:app"]