{% for service in services %}
server {
    server_name {{ ' '.join(service.vhosts) }};
    listen [::]:443 ssl http2;
    listen 443 ssl http2;

    ssl_certificate {{ service.certificate }};
    ssl_certificate_key {{ service.certificate_key }};

    location / {
        proxy_pass {{ service.protocol }}://{{ service.host }}:{{ service.port }};
    }
}
{% endfor %}
