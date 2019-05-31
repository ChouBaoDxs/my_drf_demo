from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    MALE = 1
    FAMALE = 0
    GENDER_CHOICE = {
        MALE: '男性',
        FAMALE: '女性'
    }

    name = models.CharField(verbose_name='姓名', max_length=16)
    age = models.PositiveSmallIntegerField(verbose_name='年龄', default=0)
    # gender = models.SmallIntegerField(verbose_name='性别', choices=GENDER_CHOICE.items(), default=MALE)  # 这样django_filter会报错'TypeError: can't pickle dict_keys objects'
    gender = models.SmallIntegerField(verbose_name='性别', choices=list(GENDER_CHOICE.items()), default=MALE)
    # gender = models.SmallIntegerField(verbose_name='性别', choices=((MALE, '男性'), (FAMALE, '女性')), default=MALE)
    learn_time = models.IntegerField(verbose_name='学习时长', default=0, editable=False)

    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, help_text='创建时间', editable=False)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True, help_text='修改时间', editable=False)
    is_active = models.BooleanField(verbose_name='是否可用', default=True, help_text='是否可用')
