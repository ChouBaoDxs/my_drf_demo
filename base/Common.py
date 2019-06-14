from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, help_text='创建时间', db_index=True)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True, help_text='修改时间', db_index=True)
    is_delete = models.BooleanField(verbose_name='删除标记', default=False, help_text='删除标记', editable=False)

    class Meta:
        abstract = True

    def update_is_delete(self, value: bool = True, save=True):
        self.is_delete = value
        if save:
            self.save(update_fields=['is_delete'])
