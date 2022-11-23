import unittest
from ping_me import main, get_hosts, get_hosts_to_skip, ping_hosts, ping

class TestPing(unittest.TestCase):
    def test_string(self):
        a = 'some'
        b = 'some'
        self.assertEqual(a, b)

    def test_boolean(self):
        a = True
        b = True
        self.assertEqual(a, b)
    
    def test_0_main(self):
        a = True
        b = True
        self.assertEqual(a, b)
    
    def test_1_get_hosts(self):
        network_range = '10.10.10.0/31'
        host_list = get_hosts(network_range)
        expected_range = ['10.10.10.0', '10.10.10.1']

        self.assertEqual(host_list, expected_range)
    
    def test_2_get_hosts_to_skip(self):
        network_range = ['10.10.10.0/31', '192.168.0.0/24']
        skip = '12'
        skip_list = get_hosts_to_skip(network_range, skip)
        expected_skip_list = ['10.10.10.12', '192.168.0.12']

        self.assertEqual(skip_list, expected_skip_list)

    def test_3_ping_hosts(self):
        network_hosts = ['10.99.10.0', '10.99.10.1']
        retries = 1
        exp_up = []
        exp_down = ['10.99.10.0', '10.99.10.1']
        up_hosts, down_hosts = ping_hosts(network_hosts, retries)
        self.assertEqual(sorted(list(up_hosts)), exp_up)
        self.assertEqual(sorted(list(down_hosts)), exp_down)

    def test_4_ping(self):
        target = '10.99.10.0'
        retries = 1
        up_hosts = []
        down_hosts = []
        ping(target, retries, up_hosts, down_hosts)

        self.assertEqual(sorted(list(up_hosts)), [])
        self.assertEqual(sorted(list(down_hosts)), ['10.99.10.0'])


    def test_5_main_no_skip(self):
        networks = ['10.99.10.0/31']
        retries = 1

        results = main(networks, retries, None)
        except_result = {'down': 
        ['10.99.10.0', '10.99.10.1'],
        'skipped': [],
        'up': []}
        self.assertEqual(results, except_result)


    def test_6_main_with_skip(self):
        networks = ['10.99.10.0/31']
        retries = 1
        skip = '12'
        results = main(networks, retries, skip)

        except_result = {'down': 
        ['10.99.10.0', '10.99.10.1'],
        'skipped': ['10.99.10.12'],
        'up': []}

        self.assertEqual(results, except_result)


if __name__ == '__main__':
    unittest.main()