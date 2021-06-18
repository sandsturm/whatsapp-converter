from unittest import TestCase

import whatsapp_converter

class TestParse(TestCase):
    def test_is_string(self):
        s=whatsapp_converter.parse("2/20/19, 10:14 PM - Messages to this group are now secured with end-to-end encryption. Tap for more info.", 1)
