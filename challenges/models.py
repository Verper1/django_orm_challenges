from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=256)
    author_full_name = models.CharField(max_length=256)
    isbn = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Laptop(models.Model):
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Ноутбук"
        verbose_name_plural = "Ноутбуки"

    vendor = models.CharField(max_length=50)
    release_year = models.DateField()
    amount_ram = models.PositiveSmallIntegerField()
    space_on_disk = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available_amount = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Строковое представление экземпляра Laptop. Добавлено в {self.created_at}."

    def to_json(self) -> dict:
        """Превращает данные экземпляра класса Laptop в словарь для дальнейшей отдачи в json формате."""

        laptop_data = {
            "id": self.pk,
            "vendor": self.vendor,
            "release_year": self.release_year,
            "amount_ram": self.amount_ram,
            "space_on_disk": self.space_on_disk,
            "price": self.price,
            "available_amount": self.available_amount,
            "created_at": self.created_at
        }

        return laptop_data


class Post(models.Model):
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=[
        ("Опуб", "Опубликован"),
        ("Не опуб", "Не опубликован"),
        ("Бан", "Забанен")
    ])
    created_at = models.DateTimeField()
    posted_at = models.DateTimeField()
    category = models.CharField(max_length=255, choices=[
        ("py", "Python"),
        ("c", "C"),
        ("js", "JavaScript")
    ], null=True)

    def __str__(self):
        return f"Строковое представление экземпляра Post. Добавлено в {self.created_at}."


    def to_json(self) -> dict:
        """Превращает данные экземпляра класса Post в словарь для дальнейшей отдачи в json формате."""

        post_data = {
            "id": self.pk,
            "title": self.title,
            "text": self.text,
            "author": self.author,
            "status": self.status,
            "created_at": self.created_at,
            "posted_at": self.posted_at,
            "category": self.category
        }

        return post_data