# CALABOZO MISTICO  
## Proyecto de Programacion

---

## Integrantes del Equipo

- **Christopher Rojas Montero**
- **Camila Fallas Jimenez**

**Curso:** Estructura de Datos  
**Institucion:** Universidad Nacional de Costa Rica  
**Periodo:** Verano 2026  

---

## Tabla de Contenidos

1. [Descripcion del Proyecto](#descripcion-del-proyecto)  
2. [Instalacion y Requisitos](#instalacion-y-requisitos)  
3. [Estructura del Proyecto](#estructura-del-proyecto)  
4. [Controles del Juego](#controles-del-juego)  
5. [Objetivo del Juego](#objetivo-del-juego)  
6. [Mecanicas del Juego](#mecanicas-del-juego)  
7. [Dragones](#dragones)  
8. [Formato de los Niveles JSON](#formato-de-los-niveles-json)  
9. [Sistema de Guardado](#sistema-de-guardado)  
10. [Sistema de Replay](#sistema-de-replay)  
11. [Limitaciones y Trabajo Futuro](#limitaciones-y-trabajo-futuro)  
12. [Creditos y Licencia](#creditos-y-licencia)  

---

## Descripcion del Proyecto

**Calabozo Mistico** es un videojuego 2D basado en un tablero tipo cuadrícula (grid), desarrollado en Python.  
El jugador controla un personaje que debe escapar de un calabozo recolectando **4 llaves** y abriendo la puerta de salida.

El mapa contiene paredes, llaves, una puerta y tres dragones que intentan atrapar al jugador.  
Si un dragon alcanza al jugador, la partida termina.

El proyecto incluye:

- Sistema de multiples niveles cargados desde archivos JSON.
- Guardado y carga de partidas.
- Sistema de repeticion (replay) al finalizar el juego.
- Interfaz en consola y version grafica.

---

## Instalacion y Requisitos

### Requisitos del Sistema

- **Python:** 3.8 o superior  
- **Sistema Operativo:** Windows, macOS o Linux  

### Instalacion

```bash
# Clonar repositorio
git clone https://github.com/tuusuario/calabozo-mistico.git
cd calabozo-mistico

# Ejecutar el juego
python main.py
```

---

## Estructura del Proyecto

```
calabozo-mistico/
├── entities/          # Jugador y dragones
├── game/              # Controlador, estado del juego y logica
├── world/             # Carga de niveles y manejo del mapa
├── levels/            # Archivos JSON de niveles
├── saves/             # Partidas guardadas
├── replay/            # Archivos de repeticion
├── ui/                # Interfaz consola y grafica
└── main.py            # Punto de entrada
```

---

## Controles del Juego

### Movimiento

- **W** → Arriba  
- **A** → Izquierda  
- **S** → Abajo  
- **D** → Derecha  

### Sistema

- **G** → Guardar partida  
- **L** → Cargar partida  
- **Q** → Salir  

---

## Objetivo del Juego

Para ganar la partida el jugador debe:

1. Recolectar las **4 llaves** del mapa.
2. Llegar a la **puerta de salida**.
3. Abrir la puerta (solo si tiene las 4 llaves).
4. Escapar del calabozo.

### Condicion de Derrota

- Si un dragon ocupa la misma celda que el jugador.

---

## Mecanicas del Juego

- El mapa es una cuadricula de celdas.
- El jugador solo puede moverse en 4 direcciones.
- No se puede atravesar paredes.
- Cada llave recolectada se elimina del mapa.
- La puerta solo se abre si el jugador tiene todas las llaves.
- Despues de cada movimiento del jugador, los dragones tambien se mueven.

---

## Dragones

El juego incluye tres dragones con comportamientos distintos:

### Dragon A
Persigue directamente la posicion actual del jugador.

### Dragon B
Intenta anticiparse al movimiento del jugador apuntando hacia la direccion en la que se mueve.

### Dragon C
Combina comportamientos para intentar acorralar al jugador.

---

## Formato de los Niveles JSON

Cada nivel se define en un archivo `.json` dentro de la carpeta `levels/`.

Ejemplo simplificado:

```json
{
  "rows": 15,
  "cols": 15,
  "walls": [[0,0],[0,1],[0,2]],
  "player": [1,1],
  "dragons": {
    "A": [3,3],
    "B": [5,5],
    "C": [7,7]
  },
  "keys": [[2,8],[6,4],[10,3],[12,9]],
  "door": [13,13]
}
```

El archivo define:

- Dimensiones del mapa
- Posicion inicial del jugador
- Posiciones iniciales de los dragones
- Ubicacion de las llaves
- Ubicacion de la puerta

---

## Sistema de Guardado

El juego permite guardar el estado actual en archivos dentro de la carpeta `saves/`.

Se guarda:

- Nivel actual
- Posicion del jugador
- Posiciones de los dragones
- Llaves recolectadas
- Estado general del juego

Al cargar una partida, el juego continua exactamente desde el punto guardado.

---

## Sistema de Replay

Al completar el juego, se ofrece la opcion de ver la repeticion.

El replay reconstruye:

- Movimientos del jugador
- Movimientos de los dragones
- Evolucion del mapa

Puede reproducirse automaticamente paso a paso.

Los archivos de repeticion se almacenan en la carpeta `replay/`.

---

## Limitaciones y Trabajo Futuro

- Mejorar interfaz grafica.
- Agregar mas niveles.
- Agregar efectos visuales y sonido.
- Implementar selector de nivel en GUI.
- Mejorar comportamiento de los dragones.

---

## Creditos y Licencia

### Tecnologias Utilizadas

- Python 3
- JSON
- Programacion orientada a objetos

### Licencia

Este proyecto fue desarrollado con fines educativos.

