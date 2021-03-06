#!/usr/bin/env python3

import argparse
import etcdlib
import jinja2
import os
import os.path

parser = argparse.ArgumentParser()
parser.add_argument('--name', help='Name of the docker host to request certificates for', default='unknown')
parser.add_argument('--etcd-port', type=int, help='Port to connect to etcd on', default=2379)
parser.add_argument('--etcd-host', help='Host to connect to etcd on', default='etcd')
parser.add_argument('--etcd-prefix', help='Prefix to use when retrieving keys from etcd', default='/docker')
parser.add_argument('--trusted-cert-path', help='Path to use for trusted CA certificate. Use "%s" for hostname', default='/letsencrypt/certs/%s/chain.pem')
parser.add_argument('--cert-path', help='Path to use for certificates. Use "%s" for hostname', default='/letsencrypt/certs/%s/fullchain.pem')
parser.add_argument('--cert-key-path', help='Path to use for certificate private keys. Use "%s" for hostname', default='/letsencrypt/certs/%s/privkey.pem')
parser.add_argument('--wellknown-path', help='Path to use for wellknown directory for http-01 challenge.', default='/letsencrypt/well-known/')
args = parser.parse_args()

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('/'))
template = jinja_env.get_template('nginx.tpl')
fetcher = etcdlib.Connection(args.etcd_host, args.etcd_port, args.etcd_prefix)

while True:
  wroteConfig = False;
  services = {}
  domains = {k: v.split(',') for k, v in fetcher.get_label('com.chameth.vhost').items()}
  protocols = fetcher.get_label('com.chameth.proxy.protocol')
  defaults = fetcher.get_label('com.chameth.proxy.default')
  loadbalance = fetcher.get_label('com.chameth.proxy.loadbalance')
  for container, values in fetcher.get_label('com.chameth.proxy').items():
    networks = fetcher.get_networks(container)
    certfile = args.cert_path % domains[container][0];
    up = 'lb_' + loadbalance[container] if container in loadbalance else 'ct_' + container
    if os.path.isfile(certfile):
      if not up in services:
        services[up] = {
          'upstream': up,
          'protocol': protocols[container] if container in protocols else 'http',
          'vhosts': domains[container],
          'hosts': [],
          'certificate': args.cert_path % domains[container][0],
          'trusted_certificate': args.trusted_cert_path % domains[container][0],
          'certificate_key': args.cert_key_path % domains[container][0],
          'default': container in defaults,
        }

      services[up]['hosts'].append({
        'host': next(iter(networks.values())), # TODO: Pick a bridge sensibly?
        'port': values,
      })

  if wroteConfig or len(services) > 0 or not os.path.isfile('/nginx-config/vhosts.conf'):
    with open('/nginx-config/vhosts.conf', 'w') as f:
      print('Writing vhosts.conf...', flush=True)
      f.write(template.render(services=services, wellknown_path=args.wellknown_path))
      wroteConfig = True;
    print('Done writing config.', flush=True)
  else:
    print('Not writing empty config. Ensure that your letsencrypt certificates are accessible to this container.')

  print('Done writing config.', flush=True)

  fetcher.wait_for_update()

