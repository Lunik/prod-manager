# Docker Compose deployment

This is the "small project" way to deploy `ProdManager` app and try it.

**Disclaimer:** This deployment is not intended for production deployment

## Requirements

- Any [Docker][docker] installation

## Usage

```shell
docker compose \
  --project-directory="deploy/compose" \
  --project-name="prod-manager" \
  up \
  --detach
```

Then access to http://localhost:8080


## Customisation

You can edit the [Docker compose file](docker-compose.yml) to best match your needs.

<!-- Links -->

[docker]: https://www.docker.com
