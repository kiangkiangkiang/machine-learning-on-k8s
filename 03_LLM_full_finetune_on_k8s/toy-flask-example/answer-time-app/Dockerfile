FROM python:3.9

WORKDIR /app

COPY answer-time.py .

RUN pip install Flask

EXPOSE 5000

CMD ["python", "answer-time.py"]