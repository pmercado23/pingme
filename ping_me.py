import ipaddress
import subprocess
import argparse
from multiprocessing import Manager, Pool
import pprint
import logging


def ping(target, retries, up_hosts, down_hosts):
    """Runs ping on target host with given options. will retry given number of times.

    Args:
        target (str): Target IP of ping
        retries (str): Number of retries
        up_hosts (List): List of up hosts to append to if host is up.
        down_hosts (List): List of down hosts to append to if host is down.
    """
    if not retries:
        retries = 2
    for i in range(1, retries + 1):
        logging.info("Ping attempt {} for {}".format(i, target))
        res = subprocess.call(['ping', '-c', '1', '-q', target],
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.STDOUT)

        if res == 0:
            break

    if res == 0:
        up_hosts.append(target)
    else:
        down_hosts.append(target)
    return


def get_hosts(network_range):
    """Creates a list of hosts from given network range.

    Args:
        network_range (str): Network range, i.e. 192.1.1.0/24 format

    Returns:
        List: List of network hosts in given range.
    """
    network = ipaddress.ip_network(network_range)
    host_list = list(network.hosts())
    readable_list = [format(x) for x in host_list]

    return readable_list


def pool_ping_hosts(network_hosts, retries):
    """Create pool of Processes for dividing work. This creates a Process for each ping job.

    Args:
        network_hosts (List(str)): List of hosts to ping.
        retries (str): Number of retries for failed pings.

    Returns:
        Lists: List objects of up hosts and down hosts.
    """
    up_hosts = Manager().list()
    down_hosts = Manager().list()
    pool = Pool()

    for host in network_hosts:
        pool.apply_async(ping, args=(host, retries, up_hosts, down_hosts,))

    pool.close()
    pool.join()

    return up_hosts, down_hosts


def get_hosts_to_skip(network, skipped):
    """Turns list of network ranges and finds the correct address to skip in each range.

    Args:
        network (List(str)): List of network ranges
        skipped (str): address to skip

    Returns:
        str: full address to skip
    """
    skip_networks = []
    for n in network:
        top = n.split('/')[0]
        t = top.rsplit('.', 1)[0]
        skip_value = "{}.{}".format(t, skipped)
        skip_networks.append(skip_value)
    logging.info("Skipping hosts: {}".format(skip_networks))
    return skip_networks


def main(networks, retries=None, skip=None):
    """This is the main function for running the ping_me script

    Args:
        networks (List(str)): List of network ranges.
        retries (str, optional): Number of ping retires. Defaults to None.
        skip (str, optional): Address to skip in ranges. Defaults to None.

    Returns:
        jsonObject: json Object of ping results.
    """
    logging.info("Running with retries: {}".format(retries))
    network_hosts = []
    skip_hosts = []
    for n in networks:
        hosts = get_hosts(n)
        network_hosts.extend(hosts)

    if skip:
        skip_hosts = get_hosts_to_skip(networks, skip)
        network_hosts = list(set(network_hosts) - set(skip_hosts))

    up_hosts, down_hosts = pool_ping_hosts(network_hosts, retries)
    results = {
        "up": sorted(list(up_hosts)),
        "down": sorted(list(down_hosts)),
        "skipped": skip_hosts,
    }

    return results


if __name__ == '__main__':
    """This is the main part of the script that parses in incoming args and outputs results.
    """
    parser = argparse.ArgumentParser(
        prog='PingMe',
        description='This script takes in a list of network ranges in the format x.x.x.x/x and converts them into a list of network addresses. This then will send a ping to detect if the host is reachable via ping. ping will wait 1 second per address.',
        epilog='Note: This only works with IPv4 addresses at this time.')
    parser.add_argument("--networks", action="extend", nargs="+", type=str)
    parser.add_argument(
        '--retries',
        type=int,
        help='define number of retries for a ping. default is 2')
    parser.add_argument(
        '--skip',
        type=int,
        help='Address to skip, this will skip in all networks provided, default is None')
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    args = parser.parse_args()
    print("Running...")
    results = main(args.networks, args.retries, args.skip)
    print("*********")
    pprint.pprint(results)
    print("*********")
    print("Finished!")
