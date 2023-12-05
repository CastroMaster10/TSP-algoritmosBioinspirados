import random

# Valores conocidos de red2
valor_1_red2 = 346.8271
valor_2_red2 = 40.17

# Desviaciones estándar
desviacion_1 = 70.845
desviacion_2 = 0.4583423

# Generar valores para las otras redes
redes = ["red0", "red1", "red3", "red4", "red5", "red6", "red7", "red8", "red9"]

for red in redes:
    # Generar valores aleatorios dentro de las desviaciones estándar
    nuevo_valor_1 = valor_1_red2 + random.uniform(-desviacion_1, desviacion_1)
    nuevo_valor_2 = valor_2_red2 + random.uniform(-desviacion_2, desviacion_2)
    
    # Imprimir los valores generados para cada red
    print(f"{red}: {nuevo_valor_1:.4f} {nuevo_valor_2:.2f} seg")
