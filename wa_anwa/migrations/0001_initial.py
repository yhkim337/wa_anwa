# Generated by Django 4.1 on 2022-08-20 06:09


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Betting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.IntegerField()),
                ('region', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Participate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.BooleanField()),
                ('point', models.IntegerField()),
                ('betting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participates', to='wa_anwa.betting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participates', to=settings.AUTH_USER_MODEL)),

            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.IntegerField()),
                ('win', models.BooleanField()),
                ('checked', models.BooleanField()),
                ('participation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='wa_anwa.participate')),
            ],
        ),
        migrations.AddField(
            model_name='participate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participates', to='wa_anwa.serviceuser'),
        ),
        migrations.AddConstraint(
            model_name='betting',
            constraint=models.UniqueConstraint(fields=('date', 'time', 'region'), name='unique_betting'),
        ),
        migrations.AddField(
            model_name='answer',
            name='betting',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='wa_anwa.betting'),
        ),
    ]
