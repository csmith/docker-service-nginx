# Automatic Nginx proxy config generator 

This uses my [docker-service-reporter](https://github.com/csmith/docker-service-reporter/)
container to generate an nginx config file defining virtual hosts that proxy
to docker containers with appropriate labels.

## How? 

The `service-reporter` container populates `etcd` with details about
known containers.

This container monitors `etcd` for a label specifying vhosts and proxy ports,
and puts them into a template file for nginx to use. 

## Labels

You must label any container that you wish to proxy. The following labels
are understood:

* `com.chameth.proxy=<port>` -- specifies the port on the container that the
  proxy should connect to
* `com.chameth.proxy.protocol=<protocol>` -- the protocol to use when
  connecting to the container. Optional, defaults to HTTP.
* `com.chameth.vhost=<host>` -- the virtual host that the proxy will accept
  connections on. You can specify alternate hosts/aliases by separating them
  with commas.

## Usage

Create a named volume for your nginx config, if you don't already have one:

```
docker volume create --name nginx-config
```

This should be mounted at `/nginx-config`.

Then run this container. It takes the same arguments as `service-reporter`:

```
  --etcd-host (default: etcd) hostname where ectd is running
  --etcd-port (default: 2379) port to connect to ectd on
  --etcd-prefix (default: /docker) prefix to read keys from
  --name (default: unknown) name of the host running docker
```

And some additional arguments:

```
  --cert-path (default: /letsencrypt/certs/%s/fullchain.pem) path to the SSL cert.
  --cert-key-path (default: /letsencrypt/certs/%s/privkey.pem) path to the SSL cert's private key.
```

For certificate paths, '%s' will be replaced with the (primary) vhost for each
site.

So running the container will look something like:

```
docker run -d \
  --name service-nginx \
  --restart always \
  -v nginx-config:/nginx-config \
  csmith/service-nginx:latest
```

