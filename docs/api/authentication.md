# Authentication

Most API requests require authentication, or only return public data when authentication isn’t provided. When authentication is not required, the documentation for each endpoint specifies this. For example, the `/incident/:id` endpoint does not require authentication.

There are several ways you can authenticate with the GitLab API:
- [Application secret](#application-secret)
- [Session cookie](#session-secret)

## Application secret

You can use the application secret to authenticate with the API by passing the `APPLICATION-SECRET` header.

Example of using the application secret in a header :

```shell
curl --header "APPLICATION-SECRET: <application_secret>" "http://localhost:8080/api/incident"
```

## Session secret

Signing in to the application sets a session cookie. The API uses this cookie for authentication if it’s present. Using the API to generate a new session cookie isn’t supported.
