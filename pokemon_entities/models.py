from django.db import models  # noqa F401

class Pokemon(models.Model):
    pokemon_id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=200, unique=True)
    #title_en = models.CharField(max_length=200, unique=True)
    #title_jp = models.CharField(max_length=200, unique=True)
    #description = models.TextField()
    #img_url = models.TextField()
    #entities = models.ForeignKey()
    #next_evolution = models.ForeignKey()
