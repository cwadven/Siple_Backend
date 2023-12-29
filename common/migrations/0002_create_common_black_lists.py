from django.db import migrations


def forward(apps, schema_editor):
    BlackListSection = apps.get_model('common', 'BlackListSection')
    BlackListWord = apps.get_model('common', 'BlackListWord')

    # 블랙 리스트 섹션
    BlackListSection.objects.create(
        id=1,
        name='닉네임',
        description='닉네임 생성 혹은 수정 시 블랙리스트에 등록된 단어가 포함되어 있으면 블랙리스트 처리됩니다.'
    )

    # 블랙 리스트 문구
    BlackListWord.objects.create(
        id=1,
        wording='비회원',
        black_list_section_id=1,
    )


def backward(apps, schema_editor):
    BlackListSection = apps.get_model('common', 'BlackListSection')
    BlackListWord = apps.get_model('common', 'BlackListWord')

    # 블랙 리스트 문구
    BlackListWord.objects.filter(
        black_list_section_id=1
    ).delete()

    # 블랙 리스트 섹션
    BlackListSection.objects.filter(
        id=1
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forward, backward)
    ]
