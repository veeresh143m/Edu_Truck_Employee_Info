from django.db import migrations


def create_default_departments(apps, schema_editor):
    department_model = apps.get_model("employees", "Department")
    database = schema_editor.connection.alias
    for name in ["IT", "HR", "Finance", "Sales"]:
        department_model.objects.using(database).get_or_create(name=name)


class Migration(migrations.Migration):
    dependencies = [
        ("employees", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_departments, migrations.RunPython.noop),
    ]