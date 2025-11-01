"""Modelo para series disponibles en el catalogo."""
from datetime import datetime as dt, timezone as t

from src.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, foreign
from sqlalchemy import and_
from typing import List


class Serie(db.Model):
    """Representa una serie cargada por los usuarios."""

    __tablename__ = "serie"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(255), nullable=False)
    created_at: Mapped[dt] = mapped_column(default=dt.now(t.utc), nullable=False)
    updated_at: Mapped[dt] = mapped_column(
        default=dt.now(t.utc),
        onupdate=dt.now(t.utc),
        nullable=False,
    )
    
    # TODO: configurar relacion con Season (one-to-many) y WatchEntry.
    seasons: Mapped[List['Season']] = db.relationship()

    watch_entries: Mapped[List['WatchEntry']] = db.relationship(
        "WatchEntry",
        back_populates="serie",
        # Se trae los watch entries relacionados a esta serie cuando los solicitamos
        # por ejemplo Serie.watch_entries
        primaryjoin=lambda: _serie_watch_entries_join(),
        lazy='select',
        viewonly=True,
    )  # Relacion con WatchEntry (definida en WatchEntry)
    def __repr__(self) -> str:
        """Devuelve una representacion legible del modelo."""
        return f"<Series id={getattr(self, 'id', None)} title={getattr(self, 'title', None)}>"

    def to_dict(self, include_seasons: bool = False) -> dict:
        """Serializa la serie y opcionalmente sus temporadas."""
        # TODO: reemplazar por serializacion real usando marshmallow o similar.
        data = {
            "id": getattr(self, "id", None),
            "title": getattr(self, "title", None),
            "total_seasons": getattr(self, "total_seasons", None),
            "created_at": getattr(self, "created_at", dt.now(t.utc)),
        }
        if include_seasons:
            # TODO: serializar temporadas reales en lugar de lista vacia.
            data["seasons"] = []
        return data


from .season import Season  # Importar Season para la relacion

def _serie_watch_entries_join():
    from .watch_entry import WatchEntry
    return and_(
        foreign(WatchEntry.content_id) == Serie.id,
        WatchEntry.content_type == 'serie',
    )