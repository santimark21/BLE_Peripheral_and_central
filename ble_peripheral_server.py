import bluetooth
import random
import time
from simpleBLE import BLEPeripheral
from machine import Pin # Para definir los pines
from machine import ADC # Declaracion de la conversion ADC
import math

# Bluetooth object
ble = bluetooth.BLE() 

# Environmental service
service="ed570147-da2a-4e1f-8ae4-a3e11e4c0eec"

# Temperature characteristic
characteristic="e17d00c6-9212-4bf4-b3fa-cda696999862"

# BLE peripheral object
temp = BLEPeripheral(ble,"par",service,characteristic) 


# Funcion para la lectura de la potencia aparente

def circuit(adc,sensibility,Vrms):
    Vprom = 0
    Vprom2 = 0
    Vn = []
    sumita = 0
    sumita2 = 0
    for i in range(3501):
        val1=adc.read()
        val2=3.3*val1/4095
        Vprom = Vprom + val2

    Vprom2 = Vprom/3500

    # Calculo de la corriente RMS

    # for de la sumatoria para 200 muestras
    for j in range(3501):
        val1=adc.read()
        Vn=3.3*val1/4095
        sumita = (Vn - Vprom2)**2
        sumita2 = sumita2 + sumita
    #valor interno de la raiz
    divisao = sumita2/3500

    #Raiz cuadrada
    raiz = math.sqrt(divisao)

    # Corriente RMS
    Irms = raiz/sensibility
    
    # potencia aparente
    Papp = Vrms*Irms
    return Vprom2,Irms,Papp
    

# parametros fijos
Vrms = 120.0
Sensibility = 0.066
i = 0
Pacu = 0

#lecura de pines
pin = Pin(34)
adc=ADC(pin)
adc.atten(ADC.ATTN_11DB)


while True:
    # Write every second, notify every 10 seconds.
    i = (i + 1) % 10
    Vprom,Irms,Papp = circuit(adc,Sensibility,Vrms)
    Pacu = Pacu + Papp
    print(Pacu)
    temp.set_values([int(Pacu)], notify=False, indicate=False)
    # Random walk the temperature.

    time.sleep_ms(1000)


