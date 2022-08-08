from datetime import date, timedelta
from django.utils.translation import gettext as _
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .forms import SubRubricForm
from .models import AdvUser, SuperRubric, SubRubric, AdditionalImage, Bb, Comment
from .utilities import send_activation_notification


def send_activation_notifications(modeladmin, request, queryset):
    """Send activation notifications"""
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, _('Лист активації відправлено на електронну пошту'))


send_activation_notifications.short_description = \
    _('Відправка листа з активацією')


class NonactivatedFilter(admin.SimpleListFilter):
    """User activation filtering tools"""
    title = _('Пройшли активацію?')
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', _('Пройшов')),
            ('threedays', _('Не пройшов більш ніж 3 дні тому')),
            ('week', _('Не пройшов більш ніж тиждень тому')),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = date.today() - timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False,
                                   date_joined__date__lt=d)
        elif val == 'week':
            d = date.today() - timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False,
                                   date_joined__date__lt=d)


class AdvUserAdmin(admin.ModelAdmin):
    """Tools for user administration"""
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = (('username', 'email'), ('first_name', 'last_name'),
              ('send_messages', 'is_active', 'is_activated'),
              ('is_staff', 'is_superuser'),
              'groups', 'user_permissions',
              ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,)


class SubRubricInline(admin.TabularInline):
    model = SubRubric


class SuperRubricAdmin(admin.ModelAdmin):
    """Tools for rubrics administration"""
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)


class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage


class CommentInline(admin.TabularInline):
    model = Comment


class BbAdmin(TranslationAdmin):
    """Tools for rubrics administration"""
    list_display = ('rubric', 'title', 'content', 'author', 'created_at')
    fields = (('rubric', 'author'), 'title', 'content', 'price',
              'contacts', 'image', 'is_active')
    inlines = (AdditionalImageInline, CommentInline)


admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(SubRubric, SubRubricAdmin)
admin.site.register(Bb, BbAdmin)
