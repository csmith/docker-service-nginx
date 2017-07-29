{% for service in services %}
server {
    server_name {{ ' '.join(service.vhosts) }};
    listen [::]:443{{ ' default_server' if service.default }} ssl http2;
    listen 443{{ ' default_server' if service.default }} ssl http2;

    ssl_certificate {{ service.certificate }};
    ssl_trusted_certificate {{ service.trusted_certificate }};
    ssl_certificate_key {{ service.certificate_key }};

    include /etc/nginx/conf.d/{{ service.vhosts[0] }}/*.conf;

    location / {
        proxy_pass {{ service.protocol }}://{{ service.host }}:{{ service.port }};
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
}
{% endfor %}
