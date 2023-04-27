from django.db import models

# Create your models here.


def get_path_for_uploaded_photos(instance, file):
    return f'photo/pereval-{instance.pereval.id}/{file}'

#Таблица данных о каждом пользователе
class UsersData(models.Model):
    firstname = models.CharField(max_length=30, verbose_name='Имя')
    lastname = models.CharField(max_length=30, verbose_name='Отчество')
    surname = models.CharField(max_length=30, verbose_name='Фамилия')
    phone = models.CharField(max_length=15, verbose_name='Номер телефона')
    email = models.EmailField(max_length=150, verbose_name='E-mail')


class Coords(models.Model):
    latitude = models.FloatField(max_length=50, verbose_name="Широта", blank=True, null=True)
    longitude = models.FloatField(max_length=50, verbose_name="Долгота", blank=True, null=True)
    height = models.IntegerField(verbose_name="Высота", blank=True, null=True)

    def __str__(self):
        return f"{self.latitude} {self.longitude} {self.height}"

    # class Meta:
    #     verbose_name = "Координаты"
    #     verbose_name_plural = "Координаты"



class PerevalAdded(models.Model):
    # new = "new"
    # pending = "pending"
    # accepted = "accepted"
    # rejected = "rejected"
    # STATUS = [
    #     ("new", "новый"),
    #     ("pending", "модератор взял в работу"),
    #     ("accepted", "модерация прошла успешно"),
    #     ("rejected", "модерация прошла, информация не принята"),
    # ]

    beauty_title = models.CharField(max_length=255, verbose_name="Название местности", blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name="Название перевала", blank=True, null=True)
    other_titles = models.CharField(max_length=255, verbose_name="Другое название", blank=True, null=True)

    add_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default="new")
    connect = models.TextField(blank=True, null=True)

    level_winter = models.CharField(max_length=10, verbose_name='Зима', blank=True, null=True)
    level_summer = models.CharField(max_length=10, verbose_name='Лето', blank=True, null=True)
    level_autumn = models.CharField(max_length=10, verbose_name='Осень', blank=True, null=True)
    level_spring = models.CharField(max_length=10, verbose_name='Весна', blank=True, null=True)

    #Связи: пользователь, координаты, уровень сложности
    user = models.ForeignKey(UsersData, on_delete=models.CASCADE, related_name="user")
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.pk}: {self.beauty_title}"


class PerevalImages(models.Model):
    date_added = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=255, verbose_name="Название", blank=True, null=True)
    #обдумать директорию загрузки фото
    data = models.ImageField(upload_to=get_path_for_uploaded_photos, verbose_name="Изображение", blank=True, null=True)

    pereval = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE, related_name="images", blank=True, null=True)

    def __str__(self):
        return f"{self.pk}: {self.title}"