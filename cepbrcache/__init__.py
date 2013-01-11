"""
TODO:
 * Cache it with pylibmc, maybe is better let user choice what lib
 * Support user configuration for memcached host and mongodb host, if wanted
 * Write tests
 ."
"""

import re
from cepbr import CEP
from pymongo import MongoClient

try:
    _str = basestring
except:
    _str = str


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

    def __init__(self, cep, **kw):
        self.found = False
        self.db = MongoClient()
        # create or get collection cepcaches
        self._db = self.db.ceps

        if isinstance(cep, dict):
            if 'cep' not in cep:
                raise ValueError('Cant find cep in without key cep in dict')

            self.cep_attrs = cep
            self.cep = normalize_cep(cep['cep'])
        else:
            self.cep = normalize_cep(cep)
            self.cep_attrs = kw

        self.get_cep()

    def get_cep(self):
        n_cep = normalize_cep(self.cep)

        if self.cep_attrs:
            cep = self._db.cepcaches.find_and_modify({'cep': n_cep}, self.cep_attrs, True)
        else:
            cep = self._db.cepcaches.find_one({'cep': n_cep})

        if cep:
            self.__dict__.update(cep)
            self.found = True

        return cep

    def __repr__(self):
        return "<CepCache: %s>" % self.cep
