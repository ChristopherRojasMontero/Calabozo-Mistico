"""
tiles: son pequeños bloques graficos o texturas que componen el mapa del juego como un rompecabezas para construir escenarios
Almacenamos los tiles del mapa como la estructura de datos, guardamos rows/cols, 1D de tiles, permite get/set dado en un Pos
"""
from __future__ import annotations
from dataclasses import dataclass
from world.types import Pos, TileType

@dataclass
class TileGrid:
    rows: int
    cols: int
    _tiles: list[TileType] #un arreglo 1D
    
    @staticmethod
    def filled(rows: int, cols: int, tile: TileType) -> TileGrid:
        """Crea un TileGrid lleno con el mismo tile """
        return TileGrid(rows, cols, [tile] * (rows * cols))
    
    def _idx(self, pos: Pos) -> int:
        r, c = pos
        return r * self.cols + c
    def get(self, pos: Pos) -> TileType:
        return self._tiles[self._idx(pos)]
    def set(self, pos: Pos, tile: TileType) -> None:
        self._tiles[self._idx(pos)] = tile
    