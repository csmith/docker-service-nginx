# Automatic Nginx proxy config generator 

This uses my [docker-service-reporter](https://github.com/csmith/docker-service-reporter/)
container to generate an nginx config file defining virtual hosts that proxy
to docker containers with appropriate labels.

## How? 

The `service-reporter` container populates `etcd` with details about
known containers.

This container monitors `etcd` for a label specifying vhosts and proxy ports,
and puts them into a template file for nginx to use. 

## Usage

TODO: Finish this!

Then run this container. It takes the same arguments as `service-reporter`:

```
  --etcd-host (default: etcd) hostname where ectd is running
  --etcd-port (default: 2379) port to connect to ectd on
  --etcd-prefix (default: /docker) prefix to read keys from
  --name (default: unknown) name of the host running docker
```

