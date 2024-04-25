import json
from pprint import pprint
from settings import DB

"""
films.json 
[
   {"title": "...",
    "desk": "...",
    "url": "...",
    "photo": "..."
    "rating": "..."        
    },
   {....},
]
"""


# CRUD

def get_films(data_file=DB) -> list:
    try:
        with open(data_file) as films_db:
            films = json.load(films_db)
            return films
    except json.decoder.JSONDecodeError:
        print("db is empty")
        return None


def get_film_by_id(film_id: int = 0, data_file=DB) -> dict:
    films = get_films(data_file)
    if films:
        return films[film_id]


def create_film(film: dict, data_file=DB):
    list_films = get_films(data_file)
    movie = {"title": "...",
             "desk": "...",
             "url": "...",
             "photo": "...",
             "rating": "...",
             }

    if list_films is None:
        list_films = []
    list_films.append(film)

    with open(data_file, "w") as films_db:
        json.dump(list_films, films_db, indent=4)

    return True


def edit_film():
    pass


def delete_film():
    pass


if __name__ == "__main__":
    from settings import DB

    db = "films.json"
    print(get_films(db))
