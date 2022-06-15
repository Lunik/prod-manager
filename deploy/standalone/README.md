# Standalone deployment

This is the easiest way to deploy `ProdManager` app and try it.

**Disclaimer:** This deployment is not intended for production deployment

## Requirements

- Any [Docker][docker] installation

## Usage

```shell
docker run \
  --detach \
  --name prod-manager \
  --publish 8080:8080 \
  --env PM_STANDALONE='true' \
  --env PM_SECRET_KEY='changeit' \
  registry.gitlab.com/prod-manager/prod-manager:latest
```

Then access to http://localhost:8080

<!-- Links -->

[docker]: https://www.docker.com
[make]: https://www.gnu.org/software/make/