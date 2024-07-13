from django.db import models  # noqa F401


class Pokemon(models.Model):
    pokemon_id = models.AutoField(auto_created=True, primary_key=True)
    title_ru = models.CharField(max_length=200, unique=True)
    title_en = models.CharField(max_length=200, unique=True, null=True, blank=True)
    title_jp = models.CharField(max_length=200, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='pokemons', null=True, blank=True)

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    health = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    defence = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon.title_ru}, {self.level}, {self.lat}, {self.lon}'
