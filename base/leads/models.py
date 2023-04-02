from django.db import models
from django.contrib.auth import get_user_model

class Lead(models.Model):
    nombre = models.CharField(max_length=255)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    numero = models.CharField(max_length=20)
    closer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre
