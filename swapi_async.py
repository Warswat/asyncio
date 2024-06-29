import datetime

import asyncio
import aiohttp
from more_itertools import chunked

from models import init_orm, SwapiPeople, Session

MAX_REQUESTS = 5


async def get_people(http_session, person_id):

    response = await http_session.get(f"https://swapi.py4e.com/api/people/{person_id}/")
    json_data = await response.json()
    films = json_data.get("films", "Not found")
    films_names = []
    species = json_data.get("species", "Not found")
    species_names = []
    starships = json_data.get("starships", "Not found")
    starships_names = []
    vehicles = json_data.get("vehicles", "Not found")
    vehicles_names = []
    if films != "Not found":
        await get_films(films, films_names, http_session)
        json_data["films"] = ', '.join(films_names)
    if species != "Not found":
        await get_species(species, species_names, http_session)
        json_data["species"] = ', '.join(species_names)
    if starships != "Not found":
        await get_starships(starships, starships_names, http_session)
        json_data["starships"] = ', '.join(starships_names)
    if vehicles != "Not found":
        await get_vehicles(vehicles, vehicles_names, http_session)
        json_data["vehicles"] = ', '.join(vehicles_names)
    return json_data


async def get_films(films, films_names, http_session):
    for film in films:
        film_response = await http_session.get(film)
        film_data = await film_response.json()
        films_names.append(film_data.get("title"))


async def get_species(species, species_names, http_session):
    for kind in species:
        kind_response = await http_session.get(kind)
        kind_data = await kind_response.json()
        species_names.append(kind_data.get("name"))


async def get_starships(films, films_names, http_session):
    for film in films:
        film_response = await http_session.get(film)
        film_data = await film_response.json()
        films_names.append(film_data.get("name"))


async def get_vehicles(films, films_names, http_session):
    for film in films:
        film_response = await http_session.get(film)
        film_data = await film_response.json()
        films_names.append(film_data.get("name"))
async def insert_to_database(json_list):
    async with Session() as session:
        orm_objects = [SwapiPeople(birth_year=item.get("birth_year"), eye_color=item.get("eye_color"), films=item.get("films"),
                                   gender=item.get("gender"), hair_color=item.get("hair_color"), height=item.get("height"),
                                   homeworld=item.get("homeworld"), mass=item.get("mass"), name=item.get("name"),
                                   skin_color=item.get("skin_color"), species=str(item.get("species")), starships=str(item.get("starships")),
                                   vehicles=str(item.get("vehicles"))) for item in json_list]
        session.add_all(orm_objects)
        await session.commit()


async def main():
    await init_orm()
    http_session = aiohttp.ClientSession()
    for chunk_i in chunked(range(1,100), MAX_REQUESTS):
        coros = [get_people(http_session, i) for i in chunk_i]
        result = await asyncio.gather(*coros)
        print(result)
        await insert_to_database(result)
    await http_session.close()

asyncio.run(main())
