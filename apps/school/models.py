from django.db import models
from base.Common import BaseModel


class Student(BaseModel):
    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'
    GENDER_CHOICES = {
        GENDER_MALE: '男性',
        GENDER_FEMALE: '女性',
    }

    name = models.CharField(verbose_name='姓名', max_length=16)
    age = models.PositiveSmallIntegerField(verbose_name='年龄')
    gender = models.CharField(verbose_name='性别', choices=list(GENDER_CHOICES.items()), max_length=6)

    class Meta:
        verbose_name = "学生(Student)"
        verbose_name_plural = verbose_name
        ordering = ('-created_at',)


class Hobby(BaseModel):
    name = models.CharField(verbose_name='爱好名称', max_length=16)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, db_constraint=False)
