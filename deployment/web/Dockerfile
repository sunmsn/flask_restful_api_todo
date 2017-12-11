# flask
FROM python:alpine
MAINTAINER PengShaw

# Install requirements, and create work dir
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt  && mkdir -p /var/www/html

# Define mountable directories.
VOLUME ["/var/www/html"]

# Define work dir
WORKDIR /var/www/html

# Expose ports.
EXPOSE 5000

# Define default command.
CMD ["python", "manage.py","runserver"]
 
