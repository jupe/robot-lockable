FROM python:3.7-slim-stretch

# Install dependencies
RUN apt-get update && apt-get install -y git
RUN pip3 install --upgrade pip

# Copy source
WORKDIR /robot_lockable
COPY . .

# Install project dependencies
RUN pip install -e .[dev]
RUN pip install -e .

# Run tests
RUN nosetests --with-xunit

# Remove dependency needed in tests
RUN rm -rf example

# Entrypoint command
ENTRYPOINT ["robot_lockable"]
