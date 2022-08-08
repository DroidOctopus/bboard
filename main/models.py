from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from .utilities import get_timestamp_path, send_new_comment_notification


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True,
                            verbose_name=_('Назва'))
    order = models.SmallIntegerField(default=0, db_index=True, unique=True,
                                     verbose_name=_('Порядок'))
    super_rubric = models.ForeignKey('SuperRubric',
                                     on_delete=models.PROTECT, null=True,
                                     blank=True, verbose_name=_('Надрубрика'))


class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    """Super rubric model"""
    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = _('Надрубрика')
        verbose_name_plural = _('Надрубрики')


class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    """Sub-rubric model"""
    objects = SubRubricManager()

    def __str__(self):
        return '%s - %s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = _('Подрубрика')
        verbose_name_plural = _('Подрубрики')


class AdvUser(AbstractUser):
    """User model"""
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name=_('Пройшов активацію?'))
    send_messages = models.BooleanField(default=True,
                                        verbose_name=_('Відправляти сповіщення про нові коментарі?'))

    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


class Bb(models.Model):
    """Announcement model"""
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT,
                               verbose_name=_('Рубрика'))
    title = models.CharField(max_length=40, verbose_name=_('Товар'))
    content = models.TextField(verbose_name=_('Опис'))
    price = models.FloatField(default=0, verbose_name=_('Ціна'))
    contacts = models.TextField(verbose_name=_('Контакти'))
    image = models.ImageField(blank=True, upload_to=get_timestamp_path,
                              verbose_name=_('Зображення'))
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE,
                               verbose_name=_('Автор оголошення'))
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name=_('Виводити в список?'))
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name=_('Опубліковано'))
    language = models.CharField(max_length=5, default='uk',
                                verbose_name=_('Мова оголошення'))

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = _('Оголошення')
        verbose_name = _('Оголошення')
        ordering = ['-created_at']


class AdditionalImage(models.Model):
    """Additional illustrations model"""
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE,
                           verbose_name=_('Оголошення'))
    image = models.ImageField(upload_to=get_timestamp_path,
                              verbose_name=_('Зображення'))

    class Meta:
        verbose_name_plural = _('Додаткові зображення')
        verbose_name = _('Додаткове зображення')


class Comment(models.Model):
    """Comment model"""
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE,
                           verbose_name=_('Оголошення'))
    author = models.CharField(max_length=30, verbose_name=_('Автор'))
    content = models.TextField(verbose_name=_('Вміст'))
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name=_('Виводити на екран?'))
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name=_('Опубліковано'))

    class Meta:
        verbose_name_plural = _('Коментарі')
        verbose_name = _('Коментар')
        ordering = ['created_at']


def post_save_dispatcher(sender, **kwargs):
    """A function call to send a notification about a new comment"""
    author = kwargs['instance'].bb.author
    if kwargs['created'] and author.send_messages:
        send_new_comment_notification(kwargs['instance'])


post_save.connect(post_save_dispatcher, sender=Comment)
