from django.db import models  # noqa F401


class Pokemon(models.Model):
    pokemon_id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='pokemons', null=True, blank=True)
    def __str__(self):
        return self.title
