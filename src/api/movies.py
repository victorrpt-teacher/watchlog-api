"""Endpoints relacionados con peliculas."""
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from src.extensions import db

bp = Blueprint("movies", __name__, url_prefix="/movies")

class MovieService:
    """Orquesta la logica de negocio para el recurso Movie."""

    # TODO: inyectar dependencias necesarias (db.session, modelos, esquemas, etc.).
    def __init__(self):
        from src.models.movie import Movie  # noqa: F401
        self.Movie = Movie

    def list_movies(self) -> list[dict]:
        """Retorna todas las peliculas registradas."""
        movies = self.Movie.query.all()
        movie_list = []

        for movie in movies:
            movie_list.append(movie.to_dict())

        return jsonify(movie_list)

    def create_movie(self, payload: dict) -> dict:
        """Crea una nueva pelicula."""
        required = ("title", "genre", "release_year")
        missing = [field for field in required if field not in payload]
        if missing:
            return (jsonify({
                "detail": f"Faltan campos requeridos: {', '.join(missing)}"
            }), 400)
        try:
            release_year = int(payload["release_year"])
        except (ValueError, TypeError):
            return (jsonify({
                "detail": "El campo 'release_year' debe ser un entero valido."
            }), 400)
        new_movie = self.Movie(
            title=payload["title"].strip(),
            genre=payload["genre"].strip(),
            release_year=release_year,
        )
        db.session.add(new_movie)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return (jsonify({
                "detail": "Error al crear la pelicula.",
                "error": str(e)
            }), 500)
        return jsonify(new_movie.to_dict()), 201

    def get_movie(self, movie_id: int) -> dict:
        """Obtiene una pelicula por su identificador."""
        # TODO: buscar la pelicula y manejar el caso de no encontrada.
        pass

    def update_movie(self, movie_id: int, payload: dict) -> dict:
        """Actualiza los datos de una pelicula."""
        # TODO: aplicar cambios permitidos y guardar en la base de datos.
        pass

    def delete_movie(self, movie_id: int) -> None:
        """Elimina una pelicula existente."""
        if movie_id is None:
            return (jsonify({
                "detail": "El identificador de la pelicula es requerido."
            }), 400)
        
        movie = self.Movie.query.get(movie_id)
        if movie is None:
            return (jsonify({
                "detail": "Pelicula no encontrada."
            }), 404)
        try:
            db.session.delete(movie)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return (jsonify({
                "detail": "Error al eliminar la pelicula.",
                "error": str(e)
            }), 500)
        return '', 204


service = MovieService()


@bp.get("/")
def list_movies():
    """Lista todas las peliculas disponibles."""
    return service.list_movies(), 200


@bp.post("/")
def create_movie():
    """Crea una pelicula a partir de los datos enviados."""
    payload = request.get_json(silent=True) or {}
    return service.create_movie(payload)


@bp.get("/<int:movie_id>")
def retrieve_movie(movie_id: int):
    """Devuelve el detalle de una pelicula concreta."""
    # TODO: invocar service.get_movie y manejar 404 cuando corresponda.
    return (
        jsonify(
            {
                "detail": "TODO: implementar recuperacion de pelicula",
                "movie_id": movie_id,
            }
        ),
        501,
    )


@bp.put("/<int:movie_id>")
def update_movie(movie_id: int):
    """Actualiza la informacion de una pelicula."""
    payload = request.get_json(silent=True) or {}
    # TODO: invocar service.update_movie y devolver el recurso actualizado.
    return (
        jsonify(
            {
                "detail": "TODO: implementar actualizacion de pelicula",
                "movie_id": movie_id,
                "payload_example": payload,
            }
        ),
        501,
    )


@bp.delete("/<int:movie_id>")
def delete_movie(movie_id: int):
    """Elimina una pelicula del catalogo."""
    return service.delete_movie(movie_id)
