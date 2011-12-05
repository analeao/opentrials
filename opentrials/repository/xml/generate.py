import datetime

from django.template.loader import render_to_string
from django.conf import settings

from repository import choices
from repository.xml import OPENTRIALS_XML_VERSION
from repository.templatetags.repository_tags import prep_label_for_xml

from vocabulary.models import CountryCode, InterventionCode, StudyPurpose
from vocabulary.models import InterventionAssigment, StudyMasking, StudyAllocation
from vocabulary.models import StudyPhase, StudyType, RecruitmentStatus, InstitutionType

VALID_FUNCTIONS = (
    'xml_ictrp',
    'xml_opentrials',
    'xml_opentrials_mod',
    )

def formatted_institution_address(institution):
    """Return a formatted string like: ICICT - Rio de Janeiro, RJ, Brasil"""
    return institution['name']+' - '+', '.join(
        i for i in [institution.get('city'),institution.get('state'),
                    institution['country']['description']
                    ] if i
        )

def xml_ictrp(fossils, **kwargs):
    """Generates an ICTRP XML for a given Clinical Trial and returns as string."""

    trials = []

    for fossil in fossils:
        trial = {}
        ct_fossil = fossil.get_object_fossil()
        trial['ct_fossil'] = ct_fossil
        trial['public_contact'] = ct_fossil.public_contact if ct_fossil.public_contact \
                                            else ct_fossil.scientific_contact
        trial['primary_sponsor'] = formatted_institution_address(ct_fossil.primary_sponsor)
        trial['secondary_sponsors'] = [formatted_institution_address(sponsor['institution'])
                                        for sponsor in ct_fossil.secondary_sponsors]
        trial['source_support'] = [formatted_institution_address(source['institution'])
                                        for source in ct_fossil.support_sources]
        trial['hash_code'] = fossil.pk
        trial['previous_revision'] = fossil.previous_revision
        trial['version'] = fossil.revision_sequential
        trials.append(trial)

    return render_to_string(
            'repository/xml/all_xml_ictrp.xml', # old clinicaltrial_detail.xml
            {'trial_list': trials, 'reg_name': settings.REG_NAME},
            )

def xml_opentrials(trials, include_translations=True, **kwargs):
    """Generates an Opentrials XML for a given Clinical Trial and returns as string."""
    prepared_trials = []
    for trial in trials:
        for translation in trial.translations:
            translation['primary_outcomes'] = []
            for outcome in trial.primary_outcomes:
                for out_trans in outcome['translations']:
                    if out_trans['language'] == translation['language']:
                        translation['primary_outcomes'].append(out_trans)

            translation['secondary_outcomes'] = []
            for outcome in trial.secondary_outcomes:
                for out_trans in outcome['translations']:
                    if out_trans['language'] == translation['language']:
                        translation['secondary_outcomes'].append(out_trans)

        persons = set(trial.scientific_contact + trial.public_contact + trial.site_contact)

        prepared_trials.append( (trial, persons) )

    return render_to_string(
            'repository/xml/xml_opentrials.xml',
            {'object_list': prepared_trials,
             'default_language':settings.DEFAULT_SUBMISSION_LANGUAGE,
             'reg_name': settings.REG_NAME,
             'include_translations': include_translations,
             'opentrials_xml_version': OPENTRIALS_XML_VERSION},
            )

MOD_TEMPLATE = """<!-- ===========================================================================
File: opentrials-vocabularies.mod

OpenTrials: Latin-American and Caribbean Clinical Trial Record XML DTD
DTD Version 1.0: %(generation)s

Entity definitions used by the opentrials.dtd file.
This file should be generated automatically from controlled vocabulary data
such as those from Vocabulary application.
=========================================================================== -->

%(entities)s"""

def xml_opentrials_mod(**kwargs):
    """Generates the MOD file with valid vocabularies for Opentrials XML standard."""
    entities = []

    # Languages
    #entities.append('\n'.join([
    #        '<!ENTITY % language.options',
    #        '    "en|es|fr|pt|other">'
    #        ]))

    # Health conditions
    entities.append('\n'.join([
            '<!-- TRDS 12: health condition attributes -->',
            '<!ENTITY % vocabulary.options',
            '    "decs|icd10|other">',
            ]))

    # Intervention codes
    icodes = map(prep_label_for_xml, InterventionCode.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!-- TRDS 13: intervention descriptor attributes -->',
            '<!-- attribute options cannot contain slashes "/" -->',
            '<!ENTITY % interventioncode.options',
            '    "%s">' % '|'.join(icodes), # FIXME: check why labels were defined with
                                            # '-' replacing ' ' on old .mod
            ]))

    # Study statuses
    statuses = map(prep_label_for_xml, RecruitmentStatus.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % requirementstatus.options',
            '    "%s">' % '|'.join(statuses),
            ]))

    # Age units
    entities.append('\n'.join([
            '<!ENTITY % ageunit.options',
            '    "null|years|months|weeks|days|hours">',
            ]))

    # Genders
    entities.append('\n'.join([
            '<!ENTITY % gender.options',
            '    "female|male|both">',
            ]))

    # Purposes
    purposes = map(prep_label_for_xml, StudyPurpose.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!-- TRDS 15b: study_design attributes -->',
            '<!ENTITY % purpose.options',
            '    "%s">' % '|'.join(purposes),
            ]))

    # Assignment
    assignments = map(prep_label_for_xml, InterventionAssigment.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % assignment.options',
            '    "%s">' % '|'.join(assignments),
            ]))

    # Masking
    maskings = map(prep_label_for_xml, StudyMasking.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % masking.options',
            '    "%s">' % '|'.join(maskings),
            ]))

    # Allocation
    allocations = map(prep_label_for_xml, StudyAllocation.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % allocation.options',
            '    "%s">' % '|'.join(allocations),
            ]))

    # Phases
    phases = map(prep_label_for_xml, StudyPhase.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!-- TRDS 15c -->',
            '<!ENTITY % phase.options',
            '    "%s">' % '|'.join(phases), # FIXME: replace N/A for null?
            ]))

    # Contact types
    entities.append('\n'.join([
            '<!ENTITY % contacttype.options',
            '    "public|scientific|site">',
            ]))

    # Countries
    countries = CountryCode.objects.values_list('label', flat=True)
    entities.append('\n'.join([
            '<!ENTITY % country.options',
            '    "%s">' % '|'.join(countries),
            ]))

    # Trial Statuses
    statuses = [st[0] for st in choices.TRIAL_RECORD_STATUS]
    entities.append('\n'.join([
            '<!ENTITY % trialstatus.options',
            '    "%s">' % '|'.join(statuses),
            ]))

    # Study Types
    study_types = map(prep_label_for_xml, StudyType.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % study_type.options',
            '    "%s">' % '|'.join(study_types),
            ]))

    # Institution Types
    institution_types = map(prep_label_for_xml, InstitutionType.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % institution_type.options',
            '    "%s">' % '|'.join(institution_types),
            ]))

    return MOD_TEMPLATE%{
            'generation': datetime.date.today().strftime('%Y-%m-%d'),
            'entities': '\n\n'.join(entities),
            }

