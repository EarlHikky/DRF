from django.db import models
from django.urls import reverse
from django.utils import timezone
from pytils.translit import slugify

tz = timezone.get_default_timezone()


class Staff(models.Model):
    name = models.CharField(max_length=25, db_index=True, verbose_name="ФИО")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    slug = models.SlugField(max_length=25, unique=True, db_index=True, verbose_name="URL")


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('staff', kwargs={'staff_slug': self.slug})

    def save(self,  *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Staff, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['name']


class Sales(models.Model):
    fio = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, null=True, verbose_name="ФИО")
    extradition = models.IntegerField(verbose_name="Выдачи")
    ti = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="ТИ")
    kis = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="КИС")
    trener = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Тренер")
    client = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Клиент")
    total = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Итого")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время")
    time_update = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total = sum([self.extradition, self.ti, self.kis, self.trener, self.client])
        super(Sales, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sale', kwargs={'sale_id': self.fio_id})
        # return reverse('sale', kwargs={'sale_id': self.pk, 'name': self.fio.slug})

    def __str__(self):
        return f"Продажа {self.fio} от {self.time_create}"

    class Meta:
        verbose_name = 'Продажи'
        verbose_name_plural = 'Продажи'
        ordering = ['-time_create', 'fio']
