#!/usr/bin/env python3

from collections import defaultdict
import argparse
import etcdlib
import jinja2
import os

parser = argparse.ArgumentParser()
parser.add_argument('--name', help='Name of the docker host to request certificates for', default='unknown')
parser.add_argument('--etcd-port', type=int, help='Port to connect to etcd on', default=2379)
parser.add_argument('--etcd-host', help='Host to connect to etcd on', default='etcd')
parser.add_argument('--etcd-prefix', help='Prefix to use when retrieving keys from etcd', default='/docker')
args = parser.parse_args()

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('/'))
template = jinja_env.get_template('nginx.tpl')
fetcher = etcdlib.Connection(args.etcd_host, args.etcd_port, args.etcd_prefix)

while True:
  services = []
  domains = fetcher.get_label('com.chameth.vhost')
  for container, values in fetcher.get_label('com.chameth.proxy').items():
    networks = fetcher.get_networks(container)
    services.append({
      'protocol': 'http', # TODO: Support HTTPS
      'vhost': domains[container], # TODO: Handle SANs
      'host': next(iter(networks.values())), # TODO: Pick a bridge sensibly?
      'port': values      
    })

  print(template.render(services=services)) # TODO: Actually write it out
  print('Done writing config.', flush=True)

  fetcher.wait_for_update()

