from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="country",
            name="photo_url",
            field=models.CharField(blank=True, max_length=255, verbose_name="фото"),
        ),
        migrations.AlterField(
            model_name="hotel",
            name="photo_url",
            field=models.CharField(blank=True, max_length=255, verbose_name="фото"),
        ),
        migrations.AlterField(
            model_name="tourimage",
            name="image_url",
            field=models.CharField(max_length=255, verbose_name="изображение"),
        ),
    ]
