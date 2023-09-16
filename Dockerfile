FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org -r requirements.txt

# port number that container should expose
EXPOSE 5004

# run
RUN python patch.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5004"]