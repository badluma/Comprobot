FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .

VOLUME ["/root/.local/share/Comprobot"]
ENTRYPOINT ["comprobot"]
CMD ["start"]
