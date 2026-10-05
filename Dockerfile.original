FROM python:3.9-slim

WORKDIR /app

COPY data_analysis.py .
COPY All_Diets.csv .

RUN pip install pandas matplotlib seaborn

CMD ["python", "data_analysis.py"]


