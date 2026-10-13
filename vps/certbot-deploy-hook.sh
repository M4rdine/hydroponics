#!/bin/sh
# /etc/letsencrypt/renewal-hooks/deploy/torre-mosquitto.sh
# Copia o certificado renovado para o Mosquitto (roda como uid 1883,
# sem acesso a /etc/letsencrypt) e reinicia o broker.
set -eu
DOMINIO=__DOMINIO__
DESTINO=/opt/torre/mosquitto/certs

case "${RENEWED_LINEAGE:-}" in
  */live/$DOMINIO) ;;
  *) exit 0 ;;
esac

install -o 1883 -g 1883 -m 0644 "$RENEWED_LINEAGE/fullchain.pem" "$DESTINO/fullchain.pem"
install -o 1883 -g 1883 -m 0600 "$RENEWED_LINEAGE/privkey.pem" "$DESTINO/privkey.pem"
docker compose -f /opt/torre/docker-compose.yml restart mosquitto
