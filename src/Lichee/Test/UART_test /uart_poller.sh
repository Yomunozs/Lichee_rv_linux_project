#!/bin/sh

DEVICE="/dev/ttyS0"
OUTPUT="/tmp/data.txt"
INTERVAL=5

# Configurar UART
stty -F $DEVICE 115200 cs8 -cstopb -parenb -echo -icanon min 1 time 1

while true; do
    # Limpiar cualquier dato anterior
    cat < $DEVICE > /dev/null & sleep 0.1; kill $! 2>/dev/null

    # Iniciar lectura antes de enviar
    cat < $DEVICE > "$OUTPUT" &
    CAT_PID=$!

    # Enviar comando (exacto, sin terminadores)
    echo -n "getdata" > $DEVICE

    # Esperar respuesta del dispositivo
    sleep 3

    # Finalizar lectura
    kill $CAT_PID 2>/dev/null
    wait $CAT_PID 2>/dev/null

    sleep $INTERVAL
done
