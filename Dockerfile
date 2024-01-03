# Build stage
FROM python:3.9.18 as build

ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /opt


# Test stage
FROM build as test

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=src:app

COPY test_requirements.txt .
RUN pip install --no-cache-dir -r test_requirements.txt

COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build /usr/local/lib /usr/local/lib
COPY --from=build /opt /opt

WORKDIR /opt

# Run stage
FROM python:3.9.18 as final

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=src:app

COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build /usr/local/lib /usr/local/lib
COPY --from=build /opt /opt

WORKDIR /opt

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--access-logformat", "{'time': '%(t)s', 'method': '%(r)s', 'path': '%(U)s', 'status': '%(s)s', 'type': '%(L)s', 'level':'%(l)s', 'time_to_process': '%(T)s', 'size': '%(b)s', 'referer': '%(f)s', 'protocol': '%(H)s', 'remote_host': '%(a)s', 'log_type': 'access'}", "enquiry_api:app", "--reload"]

