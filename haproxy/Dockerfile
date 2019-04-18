FROM haproxy:1.9-alpine

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg

RUN chmod +rw /usr/local/etc/haproxy/haproxy.cfg

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["haproxy", "-f", "/usr/local/etc/haproxy/haproxy.cfg"]
