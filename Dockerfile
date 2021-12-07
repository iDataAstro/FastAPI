# specify python version
FROM python:3.9.7
# specify working directory
WORKDIR /usr/src/app

# copy requirements.txt file to working directory
COPY requirements.txt ./

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy source files to working directory
COPY . .

# start app with following command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]