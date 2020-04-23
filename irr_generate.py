#!/usr/bin/env python

from netaddr import *
from datetime import date
from datetime import datetime
import requests

__author__ = 'James Di Trapani <james@ditrapani.com.au>'

class IRRCreation():
  def __init__(self):
    self.dnow = date.today().strftime("%Y%m%d")
    self.data = [x.split() for x in open('subnets.txt', 'r')]
    self.notify_email = 'xxx@xxx.com' # Your NOC email
    self.mnt_obj = 'xxxx' # Your maint object

  def find_prefixes(self, prefix, prefix_len):
    prefix = IPNetwork(prefix)
    data = [list(prefix.subnet(x)) for x in range(prefix_len, 25)]
    return [x for i in data for x in i]

  def logic(self):
    for i in self.data:
      prefix, length = i[0].split('/')
      try:
        prefixes = self.find_prefixes(i[0], int(length))
        self.print_data(prefixes, i[1])
      except:
        print('Invalid IP Format! {0} is not a valid IPv4 Prefix'.format(i[0]))
        return None

  def print_data(self, prefixes, asn):
    asname = self.asn_desc(asn)
    for prefix in prefixes:
      print("route: {0}".format(prefix.cidr))
      print("descr: {0}".format(asname))
      print("origin: {0}".format(asn))
      print("notify: {0}".format(self.notify_email))
      print("mnt-by: {0}".format(self.mnt_obj))
      print("changed: {0} {1}".format(self.notify_email, self.dnow))
      print("source: NTTCOM\n")
  
  def asn_desc(self, asn):
    session = requests.session()
    response = session.get('https://bgptoolkit.net/api/asn/{0}'.format(asn.strip('AS')))
    data = response.json().get('data')
    return data.get('name') if data.get('name') is not None else self.mnt_obj

if __name__ == '__main__':
  code = IRRCreation()
  code.logic()
