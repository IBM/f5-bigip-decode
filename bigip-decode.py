#!/usr/bin/env python3

from optparse import OptionParser
from sys import exit


# Decodes F5 BigIP cookies
# Based on instructions at https://support.f5.com/csp/article/K6917
# Usage: bigip-decode.py -c 0000000000.00000.000
# Where -c is the F5 BigIP cookie
# October 2020, Ken Mininger, kmininger@us.ibm.com

def get_port(c_port) -> str:
    # convert the second part of the cookie to hex
    hh_port = (hex((int(c_port))))
    # reverse the byte order
    r_port = reverse_bytes(hh_port)
    # turn it back into a hex number
    r_port2 = "{0}".format((r_port.replace('0x', '')))
    return str(int(r_port2, 16))


def get_host(c_host) -> str:
    # convert the first part of the cookie to hex
    hh_host = (hex((int(c_host)))[2:])
    # reverse the byte order
    r_host = reverse_bytes(hh_host)
    # make a list of pairs of bytes from above
    dh_host = [r_host[i:i + 2] for i in range(0, len(r_host), 2)]
    # convert those reversed bytes to decimal
    xhosts = [int(dh_host[pos], 16) for pos in range(len(dh_host))]
    # print out the ip address
    return '.'.join([str(octet) for octet in xhosts])


def reverse_bytes(payload) -> str:
    return "".join(reversed([payload[i:i + 2] for i in range(0, len(payload), 2)]))


def main():
    parser = OptionParser()
    parser.add_option("-c", "--cookie", type="string")
    (options, args) = parser.parse_args()
    if not options.cookie:
        parser.error("Cookie not provided. Please provide the F5 BigIP cookie.")
        exit(1)
    # initial value of cookie
    cookie = options.cookie
    # echo the cookie
    print("F5 BigIP cookie: ", cookie)
    # split the cookie into 2 parts, splitting at the '.' and ignoring the right-most value
    [c_host, c_port] = cookie.split('.')[:2]
    host = get_host(c_host)
    port = get_port(c_port)
    print("Decoded cookie (IP address:Port): {0}".format(str(":".join([host, port]))))


if __name__ == '__main__':
    main()
