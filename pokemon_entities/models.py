from django.db import models  # noqa F401


class Pokemon(models.Model):
    pokemon_id = models.AutoField(
        auto_created=True,
        primary_key=True,
        verbose_name='id покемона'
    )
    title_ru = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Имя на русском языке'
    )
    title_en = models.CharField(
        max_length=200,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Имя на английском языке'
    )
    title_jp = models.CharField(
        max_length=200,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Имя на японском языке'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание покемона'
    )
    image = models.ImageField(
        upload_to='pokemons',
        null=True, blank=True,
        verbose_name='Картинка покемона'
    )
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='next_evolutions',
        verbose_name='Предыдущая эволюция покемона'
    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='pokemon_entities',
        verbose_name='Тип покемона'
    )
    lat = models.FloatField(verbose_name='Ширина')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата и время появления'
    )
    disappeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата и время исчезновения'
    )
    level = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Уровень покемона'
    )
    health = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Здоровье покемона'
    )
    strength = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Атака покемона'
    )
    defence = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Защита покемона'
    )
    stamina = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Выносливость покемона'
    )

    def __str__(self):
        return f'{self.pokemon.title_ru}, {self.level}, {self.lat}, {self.lon}'
