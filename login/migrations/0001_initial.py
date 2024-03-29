# Generated by Django 3.2.4 on 2021-08-23 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssChar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AssChar', models.CharField(max_length=100)),
                ('CountryCode', models.CharField(default='IN', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CharMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CountryCode', models.CharField(default='IN', max_length=100)),
                ('pSuperGroup', models.CharField(max_length=100)),
                ('pGroup', models.CharField(max_length=100)),
                ('pModule', models.CharField(max_length=100)),
                ('pClass', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('CountryCode', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('CountryName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ParamDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CountryCode', models.CharField(default='IN', max_length=100)),
                ('pType', models.CharField(max_length=500)),
                ('pCode', models.CharField(max_length=100)),
                ('pDesc', models.CharField(max_length=500)),
                ('pActivity', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='pGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='pSupergroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supergroup', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Userdetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Username', models.CharField(max_length=100)),
                ('Password', models.CharField(max_length=100)),
                ('CountryCode', models.CharField(default='IN', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='pModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(max_length=100)),
                ('gid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.pgroup')),
            ],
        ),
        migrations.AddField(
            model_name='pgroup',
            name='sid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.psupergroup'),
        ),
        migrations.CreateModel(
            name='pClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pclass', models.CharField(max_length=100)),
                ('supergroup', models.CharField(max_length=500)),
                ('group', models.CharField(max_length=500)),
                ('module', models.CharField(max_length=500)),
                ('CountryCode', models.CharField(default='IN', max_length=100)),
                ('gid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.pgroup')),
                ('mid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.pmodule')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.psupergroup')),
            ],
        ),
        migrations.CreateModel(
            name='CharDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CountryCode', models.CharField(default='IN', max_length=100)),
                ('CharName', models.CharField(default=None, max_length=100)),
                ('CharNature', models.CharField(default=None, max_length=100)),
                ('BaseChar', models.CharField(default=None, max_length=100)),
                ('CharScope', models.CharField(default=None, max_length=100)),
                ('CharCategory', models.CharField(default=None, max_length=100)),
                ('ValueList', models.CharField(max_length=100)),
                ('Mandatory', models.CharField(max_length=100)),
                ('Charmaster_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.pclass')),
            ],
        ),
    ]
