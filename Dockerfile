# PURPOSE:
# - run project in container

# WHY:
# - required for deployment

# MUST:
# - docker build works
# - docker run works

# PURPOSE:
# - run project in container

# WHY:
# - required for deployment

# MUST:
# - docker build works
# - docker run works

FROM python:3.11-slim

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "app.api.routes:app", "--host", "0.0.0.0", "--port", "7860"]