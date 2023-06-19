## Overview
This project is a Python-based web application built with Flask. Its goal is to scrape proxies from the internet and display them on a website. Additionally, the project allows users to grab proxies through a REST API.

## Prerequisites
* Python 3.11
* Poetry ^1.4.0
* Postgres 15
* GeoLite2-City database

## Installation
```bash
git clone https://github.com/kyofu95/proxies
cd proxies
poetry install
cp .env.sample .env
Edit your .env file
docker-compose -f docker-compose.yml up
check localhost:80
```

For local dev and tests you will need GeoLite2-City database. Download it from MaxMind site, and set its path to MAXDBLITE_PATH variable in .env file
For tests you will also need to make test.env based on test.env.sample.