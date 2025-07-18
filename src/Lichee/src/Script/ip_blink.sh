#!/bin/bash

GPIO=99  #pin 34  

# Exportar GPIO si aún no lo está
if [ ! -d /sys/class/gpio/gpio$GPIO ]; then
    echo "$GPIO" > /sys/class/gpio/export
    sleep 0.2
fi

echo "out" > /sys/class/gpio/gpio$GPIO/direction

# Función para blink
blink_times() {
    local count=$1
    local duration=${2:-0.3}

    for i in $(seq 1 "$count"); do
        echo 1 > /sys/class/gpio/gpio$GPIO/value
        sleep "$duration"
        echo 0 > /sys/class/gpio/gpio$GPIO/value
        sleep "$duration"
    done
}

# Loop infinito
while true; do
    IP=$(ip route get 1.1.1.1 2>/dev/null | grep -oP 'src \K[\d.]+')

    if [[ "$IP" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        LAST_BYTE=$(echo "$IP" | awk -F. '{print $4}')
        blink_times "$LAST_BYTE" 0.3
        sleep 3
    else
        # Sin conexión: 3 parpadeos rápidos cada 5 segundos
        blink_times 3 0.1
        sleep 5
    fi
done
