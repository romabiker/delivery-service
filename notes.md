
alembic init -t async migration

alembic revision --autogenerate -m "Initial revision"

alembic revision -m "Tron wallet" --autogenerate

 my-service:
    image: ubuntu:latest
    user: ${MY_UID}:${MY_GID}
    volumes:
      - /etc/passwd:/etc/passwd:ro
      - /etc/group:/etc/group:ro
and define these variables where you are starting your compose:

MY_UID="$(id -u)" MY_GID="$(id -g)" docker-compose up

addr = 'TTzPiwbBedv7E8p4FkyPyeqq4RVoqRL3TW'  # todo rm

--mount=type=bind,source=./backend/pyproject.toml,target=./backend/pyproject.toml uv sync --frozen --no-install-project