import config
import unittest
import rules_checker as rc

SWISS_IP = '84.55.213.166'
BRITISH_IP = '185.86.151.11'
FRENCH_IP = '148.64.19.38'


class TestRulesChecker(unittest.TestCase):
    def test_get_country_from_ip(self):
        self.assertEqual(rc.get_country_from_ip(SWISS_IP), 'CH')
        self.assertEqual(rc.get_country_from_ip(BRITISH_IP), 'GB')
        self.assertEqual(rc.get_country_from_ip(FRENCH_IP), 'FR')

    def test_is_country_allowed(self):
        self.assertTrue(rc.is_country_allowed(SWISS_IP))
        self.assertFalse(rc.is_country_allowed(BRITISH_IP))
        self.assertFalse(rc.is_country_allowed(FRENCH_IP))

    def test_override_white_list(self):
        config.WHITE_LIST_OVERRIDE = True
        self.assertTrue(rc.is_country_allowed(BRITISH_IP))
        self.assertTrue(rc.is_country_allowed(FRENCH_IP))
        config.WHITE_LIST_OVERRIDE = False


if __name__ == '__main__':
    unittest.main()
