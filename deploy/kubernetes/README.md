# CloudNative deployment

This is the best way to deploy `ProdManager` app for production deployment.

## Requirements

- Any [Kubernetes][kubernetes] cluster
- [kubectl][kubectl] binary

## Usage

Create a dedicated namespace for the application

```shell
kubectl create namespace prod-manager
```

Then deploy the app

```shell
kubectl apply \
  --namespace prod-manager \
  --filename deploy/kubernetes/
```

If you have an ingress controller, the service should be exposed through it. If not use the builtin kubectl port fowarder : 

```shell
kubectl port-forward \
  --namespace prod-manager \
  service/prod-manager-proxy 8080:80
```

Then access to http://localhost:8080


## Customisation

You can edit the [Kubernetes manifests file](.) to best match your needs.

<!-- Links -->

[kubernetes]: https://kubernetes.io
[kubectl]: https://kubernetes.io/docs/reference/kubectl/kubectl/