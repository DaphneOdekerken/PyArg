FROM python:3.11-bookworm

# Create a working directory.
WORKDIR /usr/src/app

# Install Python dependencies.
RUN apt update
RUN apt install -y gringo
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install uwsgi

# Copy the rest of the codebase into the image
COPY . ./

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/src"

# Finally, run gunicorn.
CMD ["uwsgi", "wsgi.ini"]

