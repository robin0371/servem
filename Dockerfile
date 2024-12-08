FROM python:3.12

ARG APP=/opt/servem

COPY . $APP/

WORKDIR $APP
RUN pip install -U pip && pip install -r requirements.txt

CMD ["python", "-V"]

