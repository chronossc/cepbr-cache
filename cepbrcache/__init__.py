"""
TODO:
 * Cache it with pylibmc, maybe is better let user choice what lib
 * Support user configuration for memcached host and mongodb host, if wanted
 * Write tests
 ."
"""

import os
import re
import json
from cepbr import CEP
from pymongo import MongoClient

try:
    _str = basestring
except:
    _str = str


# settings
CONNECTION_SETTINGS = {
    'CEP_MONGO_HOST': os.environ.get('CEP_MONGO_HOST', 'localhost'),
    'CEP_MONGO_PORT': os.environ.get('CEP_MONGO_PORT', 27017),
    'CEP_DB_NAME': os.environ.get('CEP_DB_NAME', 'ceps'),
    'CEP_MONGO_OPTS': os.environ.get('CEP_MONGO_OPTS', {}),
}

_conn = None  # so we dont use one connection for each object


class CepNotFound(Exception):
    pass


class InvalidCEP(Exception):
    pass


def normalize_cep(cep):
    """
        Normalize a cep to 8 digits string '99999999'.
    """
    if isinstance(cep, (int, long)):
        cep = str(cep).zfill(8)
    elif isinstance(cep, _str):
        cep = re.sub(r'[-\.]', '', cep)
    else:
        raise ValueError("Unknow type for cep, wanna magic?")

    if not cep.isdigit():
        raise InvalidCEP("CEP '%s' has non digit characters." % cep)

    return cep


def get_cep(cep):
    """
    Returns a CepCache instance from DB, or create with cepbr

    >>> cep = get_cep('01310200')
    >>> cep.bairro
    u'Bela Vista'
    >>> cep.localidade
    u'S\xe3o Paulo'
    """
    dbcep = CepCache(cep)
    if dbcep.found:
        return dbcep
    return CepCache(CEP().get_cep(normalize_cep(cep)))


class CepCache(object):

    __db = None

    def __init__(self, cep, **kw):
        self.found = False

        if isinstance(cep, dict):
            if 'cep' not in cep:
                raise ValueError('Cant find cep in without key cep in dict')

            self.cep_attrs = cep
            self.cep = normalize_cep(cep['cep'])
        else:
            self.cep = normalize_cep(cep)
            self.cep_attrs = kw

        self.get_cep()

    @property
    def db(self):
        """
        Keep db connection
        """
        if self.__db:
            return self.__db

        global _conn
        if _conn is None:
            _conn = MongoClient(host=CONNECTION_SETTINGS['CEP_MONGO_HOST'],
                                port=CONNECTION_SETTINGS['CEP_MONGO_PORT'],
                                **CONNECTION_SETTINGS['CEP_MONGO_OPTS'])

        self.__db = getattr(_conn, CONNECTION_SETTINGS['CEP_DB_NAME'])

        return self.__db

    def get_cep(self):
        n_cep = normalize_cep(self.cep)
        if self.cep_attrs:
            cep = self.db.cepcaches.find_and_modify(
                {'cep': n_cep},
                self.cep_attrs, True)
        else:
            cep = self.db.cepcaches.find_one({'cep': n_cep})

        if cep:
            self.__dict__.update(cep)
            self.found = True

        return cep

    def json(self):
        data = self.__dict__.copy()
        invalids = filter(lambda key: key.startswith('_'), data)
        for key in invalids:
            data.pop(key)

        if not self.found:
            data = data['cep_attrs']

        return json.dumps(data)

    def __repr__(self):
        return "<CepCache: %s>" % self.cep
