from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wa_anwa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participate',
            name='point',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='participate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participates', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='result',
            name='checked',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='ServiceUser',
        ),
    ]
