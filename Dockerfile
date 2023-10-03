##
## Copyright (c) 2023 Felix Huettner.
##
## This file is part of Essensliste 
## (see https://github.com/huettner94/essensliste).
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.
##

# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-alpine

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements

WORKDIR /app
COPY . /app
RUN python -m pip install -r requirements.txt && \
    adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app

USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["/app/entrypoint.sh"]
