import folium
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from pokemon_entities.models import PokemonEntity
from pokemon_entities.models import Pokemon
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def get_full_url(request, url):
    return f'http://{request.get_host()}{url}'


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
    pokemon_entitites = PokemonEntity.objects.filter(
        disappeared_at__gt=local_time,
        appeared_at__lt=local_time
    )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entitity in pokemon_entitites:
        add_pokemon(
            folium_map,
            entitity.lat,
            entitity.lon,
            get_full_url(request, entitity.pokemon.image.url)
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': get_full_url(request, pokemon.image.url),
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    local_time = localtime()
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    pokemon_entitites = requested_pokemon.entities.filter(
        disappeared_at__gt=local_time,
        appeared_at__lt=local_time
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemon_entitites:
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            get_full_url(request, entity.pokemon.image.url)
        )
    pokemon_to_view = {
        'pokemon_id': requested_pokemon.id,
        'img_url': get_full_url(request, requested_pokemon.image.url),
        'description': requested_pokemon.description,
        'title_ru': requested_pokemon.title_ru,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
    }
    if requested_pokemon.previous_evolution:
        previous_evolution = {
            'pokemon_id': requested_pokemon.previous_evolution.id,
            'img_url': get_full_url(
                request,
                requested_pokemon.previous_evolution.image.url
            ),
            'title_ru': requested_pokemon.previous_evolution.title_ru
        }
        pokemon_to_view['previous_evolution'] = previous_evolution
    next_evolutions = requested_pokemon.next_evolutions.all()
    if next_evolutions:
        next_evolution = next_evolutions[0]
        next_evolution = {
            'pokemon_id': next_evolution.id,
            'img_url': get_full_url(request, next_evolution.image.url),
            'title_ru': next_evolution.title_ru
        }
        pokemon_to_view['next_evolution'] = next_evolution
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_to_view
    })
