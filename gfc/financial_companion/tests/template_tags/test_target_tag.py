from .test_template_tag_base import TemplateTagTestCase
from financial_companion.maps import timespan_map
from financial_companion.templatetags import get_completeness
import os
from freezegun import freeze_time
import datetime


class GetCompletenessTemplateTagTestCase(TemplateTagTestCase):
    """Test for the get_completeness logo template tag"""
