from modeltranslation.translator import register, TranslationOptions

from .models import Rubric, Bb


@register(Rubric)
class RubricTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Bb)
class BbTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'price', 'contacts', 'created_at')
