FROM node:20-alpine AS frontend

WORKDIR /app

RUN apk add --no-cache brotli

COPY package.json package-lock.json  ./

RUN npm install

COPY webpack.config.js tailwind.config.js postcss.config.js ./
COPY ./app/templates ./app/templates
COPY ./app/src ./app/src
RUN npm run build

RUN find ./app/static/build -type f \
        \( -name "*.js" -o -name "*.css" -o -name "*.ico" -o -name "*.svg" \) \
        -exec brotli -f -k -Z {} +


FROM python:3.12.0-bookworm as application

WORKDIR /app

COPY . .

RUN python -m pip install --no-cache-dir poetry

RUN poetry config virtualenvs.in-project true \
    && poetry install --without dev,test --no-interaction --no-ansi

COPY --from=frontend /app/app/static/build ./app/static/build

RUN mkdir logs database cache app/static/storage -p

CMD /app/.venv/bin/gunicorn -c gunicorn_config.py app:app
