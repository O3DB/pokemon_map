import folium
import json
import os

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Pokemon, PokemonEntity


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.select_related().all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        try:
            image_url = basedir + pokemon_entity.pokemon.image.url
        except ValueError:
            image_url = DEFAULT_IMAGE_URL
        add_pokemon(
            folium_map, 
            pokemon_entity.latitude, 
            pokemon_entity.longitude,
            pokemon_entity.pokemon.title_ru, 
            image_url
            )

    pokemons_on_page = []
    pokemons = Pokemon.objects.select_related().all()
    for pokemon in pokemons:
        try:
            image_url = pokemon.image.url
        except:
            image_url = DEFAULT_IMAGE_URL
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': image_url,
            'title_ru': pokemon.title_ru,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_entities = PokemonEntity.objects.select_related().filter(pokemon__id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, 
            pokemon_entity.latitude, 
            pokemon_entity.longitude,
            pokemon_entity.pokemon.title_ru, 
            basedir + pokemon_entity.pokemon.image.url
            )

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon,
                                                    })
