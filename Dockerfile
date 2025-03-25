FROM python:3.9.1
ENV PYTHONUNBUFFERED 1

WORKDIR /automation

COPY requirements ./requirements
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements/prod.txt

COPY automation ./automation
COPY bin .

CMD ["python", "update_sidebar.py"]
