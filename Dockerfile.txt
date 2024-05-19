FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY streamlit_app2.py .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app2.py", "--server.port=8501", "--server.address=0.0.0.0"]
