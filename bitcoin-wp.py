#!/usr/bin/env python3

# BitcoinPrice
# Copyright (C) 2013, Thomas Bertani
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Software for getting the current Bitcoin price. """

import requests
import simplejson


class MarketNotAvailable(Exception):
    pass


class Market(object):

    """A Market object.

    """

    base_url = ''
    currency = ''

    def __init__(self, currency='USD'):
        self.currency = currency

    def ticker(self):
        res = self._ticker()
        return {'price': res['price'], 'volume': res['volume']}


class Bitstamp(Market):
    base_url = 'https://www.bitstamp.net/api/'

    def _ticker(self):
        try:
            ticker_raw = requests.get(url="%sticker/" % self.base_url)
            ticker_json = simplejson.loads(ticker_raw.content)
            price = (float(ticker_json['ask']) + float(ticker_json['bid'])) / 2
            volume = float(ticker_json['volume'])
            return {'price': price, 'volume': volume}
        except:  # FIXME
            raise MarketNotAvailable

    def _eurusd(self):
        try:
            ticker_raw = requests.get(url="%seur_usd/" % self.base_url)
            ticker_json = simplejson.loads(ticker_raw.content)
            eurusd = (
                float(ticker_json['sell']) + float(ticker_json['buy'])) / 2
            return eurusd
        except:  # FIXME
            raise MarketNotAvailable


class Eurofxref(Market):
    r = requests.get('http://www.ecb.int/stats/eurofxref/eurofxref-daily.xml', stream=True)
    from xml.etree import ElementTree as ET
    tree = ET.parse(r.raw)
    root = tree.getroot()
    currency = "USD"

    def _eurusd(self):
        try:
            match = self.root.find('.//ex:Cube[@currency="{}"]'.format(self.currency.upper()))
            eurusd = (float((match.attrib['rate'])))
            return eurusd
        except:  # FIXME
            raise MarketNotAvailable


class MtGox(Market):
    base_url = 'http://data.mtgox.com/api/1/'

    def _ticker(self):
        try:
            ticker_raw = requests.get(url="%sBTCUSD/ticker" % self.base_url)
            ticker_json = simplejson.loads(ticker_raw.content)
            price = (float(ticker_json['return']['buy']['value']) + float(
                ticker_json['return']['sell']['value'])) / 2
            volume = float(ticker_json['return']['vol']['value'])
            return {'price': price, 'volume': volume}
        except:  # FIXME
            raise MarketNotAvailable


class Btce(Market):
    base_url = 'https://btc-e.com/api/2/'

    def _ticker(self):
        try:
            ticker_raw = requests.get(url="%sbtc_usd/ticker" % self.base_url)
            ticker_json = simplejson.loads(ticker_raw.content)
            price = (float(ticker_json['ticker']['sell']) + float(
                ticker_json['ticker']['buy'])) / 2.
            volume = float(ticker_json['ticker']['vol_cur'])
            return {'price': price, 'volume': volume}
        except:  # FIXME
            raise MarketNotAvailable


class WP(object):
    markets = ['MtGox', 'Bitstamp', 'Btce']

    def __init__(self, currency='USD', markets=()):
        self.currency = currency
        # let's choose from which markets we take the data from
        if markets:
            [self.markets.remove(m) for m in self.markets if m not in markets]

    def current_weightedprice(self):
        prices, markets = [], []
        for m in self.markets:
            try:
                c = globals()[m](self.currency).ticker()  # FIXME
                prices.append((c['price'], c['volume']))
                markets.append(m)
            except MarketNotAvailable:
                pass
        price = sum(p[0] * p[1] for p in prices) / sum(p[1]
                                                       for p in prices) / eurusd() # FIXME
        return "%.2f" % price #return (markets, "%.2f" % price)


def eurusd():
        try:
            eurusd = Eurofxref()._eurusd()
        except MarketNotAvailable:
            try:
                eurusd = Bitstamp()._eurusd()
            except MarketNotAvailable:
                eurusd = 1.33
        return eurusd

if __name__ == '__main__':
    wp = WP(markets=['Bitstamp', 'Btce', 'MtGox'])
    print(wp.current_weightedprice())
