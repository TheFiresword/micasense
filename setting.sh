#!/bin/bash
# Script pour configurer l'adresse IP de l'interface ethernet de la raspberry à 192.168.1.40
# Nécéssaire pour pouvoir communiquer avec la caméra en liaison ethernet
# Pour le lancer :
#   - accorder les droits d'exécution -> chmod +x setting.sh
#   - exécuter le script -> ./setting.sh

eth_name=$(nmcli -t -f NAME,TYPE con show | grep "ethernet" | head -n 1 | cut -d: -f1)
if [ -z "$eth_name" ]; then
 echo "Aucun interface ethernet trouvé."
 exit 1
fi

RASPBERRY_IP_ADDRESS = "192.168.1.40/24"
nmcli connection modify "$eth_name" ipv4.method manual ipv4.addresses $RASBERRY_IP_ADDRESS
nmcli connection up "$eth_name"

echo "Configuration de l'interface ethernet de la raspberry pi terminée :)"
