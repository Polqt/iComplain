from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0005_ticketattachment_exactly_one_parent"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="archived_at",
            field=models.DateTimeField(blank=True, help_text="Set when ticket is soft-deleted (archived).", null=True),
        ),
    ]
