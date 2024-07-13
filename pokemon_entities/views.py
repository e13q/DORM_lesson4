import folium
from django.shortcuts import render
from pokemon_entities.models import PokemonEntity
from pokemon_entities.models import Pokemon
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    local_time = localtime()
    pokemons = PokemonEntity.objects.filter(
        disappeared_at__gt=local_time,
        appeared_at__lt=local_time
    )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        add_pokemon(
            folium_map,
            pokemon.lat,
            pokemon.lon,
            f'http://{request.get_host()}{pokemon.pokemon.image.url}'
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.pokemon_id,
            'img_url': f'http://{request.get_host()}{pokemon.image.url}',
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    local_time = localtime()
    requested_pokemon = Pokemon.objects.get(pokemon_id=pokemon_id)
    pokemons_on_map = PokemonEntity.objects.filter(
        pokemon=requested_pokemon,
        disappeared_at__gt=local_time,
        appeared_at__lt=local_time
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons_on_map:
        add_pokemon(
            folium_map,
            pokemon.lat,
            pokemon.lon,
            f'http://{request.get_host()}{pokemon.pokemon.image.url}'
        )
    pokemon_to_view = {
        'pokemon_id': requested_pokemon.pokemon_id,
        'img_url': f'http://{request.get_host()}{requested_pokemon.image.url}',
        'description': requested_pokemon.description,
        'title_ru': requested_pokemon.title_ru,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
    }
    if requested_pokemon.previous_evolution:
        previous_evolution = {
            'pokemon_id': requested_pokemon.previous_evolution.pokemon_id,
            'img_url': f'http://{request.get_host()}{requested_pokemon.previous_evolution.image.url}',
            'title_ru': requested_pokemon.previous_evolution.title_ru
        }
        pokemon_to_view['previous_evolution'] = previous_evolution
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_to_view
    })
