from django.contrib import admin
from django.contrib.contenttypes import generic
from django.conf import settings

from vocabulary.models import *
from polyglot.admin import TranslationInline, TranslationAdmin

from utilities import export_json

class VocabularyTranslationInline(TranslationInline):
    model = VocabularyTranslation

class SimpleVocabularyAdmin(TranslationAdmin):
    list_display = ('label', 'description', 'translation_completed', 'missing_translations')
    inlines = [VocabularyTranslationInline]
    actions = [export_json]

class CountryCodeAdmin(TranslationAdmin):
    list_display = ('label', 'description', 'submission_language', 'translation_completed', 'missing_translations')
    search_fields = ('label', 'description')
    list_filter = ('submission_language',)
    inlines = [VocabularyTranslationInline]

for model in (RecruitmentStatus, StudyType, StudyPhase, InterventionCode,
    AttachmentType, TrialNumberIssuingAuthority, StudyPurpose, TimePerspective,
    InterventionAssigment, StudyMasking, StudyAllocation, InstitutionType,
    ObservationalStudyDesign, ):
    if model not in admin.site._registry:
        admin.site.register(model, SimpleVocabularyAdmin)

if CountryCode not in admin.site._registry:
    admin.site.register(CountryCode, CountryCodeAdmin)

class MailMessageAdmin(admin.ModelAdmin):
    exclude = ('label',)

admin.site.register(MailMessage, MailMessageAdmin)
