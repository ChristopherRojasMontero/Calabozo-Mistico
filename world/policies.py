"""
En esta clase estamos haciendo las politicas de juego o sea las reglas intercambiables que definen como se comporta el juego
en vez de que el gridworld tenga unas reglas fijas le vamos a pasar esa decision a un objeto de reglas 
vamos a aplicar el patron policy que es muy parecido al patron strategy y nos ayuda al SOLID


aqui tendremos 
WalkabilityPolicy: una intefaz de caminabilidad 
DefaultWalkabilityPolicy: caminibalidad por defecto
WALL: nunca
FLOOR: siempre
DOOR: si tiene keys_collected >= keys_required

aclaracion de librerias usadas:
future es para importar caracteristicas y sintaxis de versiones futuras de python en versiones anteriores para facilitar migracion
y permitiendo probar nuevas funcionalidades
dataclasses son clases diseñadas para almacenar datos que automatizan la generacion de metodos repetitivos como init, repr y eq
"""
from __future__ import annotations
from dataclasses import dataclass
from world.types import TileType, WalkContext, Pos


class WalkabilityPolicy:
    """Contrato: decide si un tile se puede pisar."""
    def is_walkable(self, tile: TileType, pos: Pos, ctx: WalkContext) -> bool:
        raise NotImplementedError


@dataclass(frozen=True)
class DefaultWalkabilityPolicy(WalkabilityPolicy):
    """Reglas por defecto: WALL nunca, FLOOR siempre, DOOR solo con llaves suficientes."""
    def is_walkable(self, tile: TileType, pos: Pos, ctx: WalkContext) -> bool:
        if tile == TileType.WALL:
            return False
        if tile == TileType.DOOR:
            return ctx.keys_collected >= ctx.keys_required
        return True