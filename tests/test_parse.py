from unittest import TestCase
from whatsapp_converter import whatsapp_converter

class TestParse(TestCase):

    def test_is_string(self):
        # s=whatsapp_converter.parse("2/20/19, 10:14 PM - Messages to this group are now secured with end-to-end encryption. Tap for more info.", 1)
        s=whatsapp_converter.parse("23.12.18, 21:06 - Thomas: Auf alle Fälle. Lass uns schauen, dass wir uns nächstes Jahr mal treffen.", 1)
        self.assertEqual(s, 'FOO')

if __name__ == '__main__':
    unittest.main()
