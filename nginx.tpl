{% for service in services %}
server {
    server_name {{ ' '.join(service.vhosts) }};
    listen [::]:443 ssl http2;

    location / {
        proxy_pass {{ service.protocol }}://{{ service.host }}:{{ service.port }};
    }
}
{% endfor %}
