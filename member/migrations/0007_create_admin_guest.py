from django.db import migrations


def forward(apps, schema_editor):
    Member = apps.get_model('member', 'Member')
    member = Member.objects.get(
        username='admin'
    )
    Guest = apps.get_model('member', 'Guest')
    Guest.objects.get_or_create(
        temp_nickname='관리자',
        ip='000.000.000.000',
        email='admin@admin.com',
        member=member,
    )


def backward(apps, schema_editor):
    Guest = apps.get_model('member', 'Guest')
    Guest.objects.filter(member__username='admin').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0006_alter_guest_last_joined_at'),
    ]

    operations = [
        migrations.RunPython(forward, backward)
    ]
