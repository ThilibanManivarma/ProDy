# -*- coding: utf-8 -*-
"""This module defines classes for handling residues."""

from .subset import AtomSubset
from .atom import Atom

__all__ = ['Residue']

class Residue(AtomSubset):

    """Instances of this class point to atoms with same residue numbers (and
    insertion codes) and are generated by :class:`.HierView` class.
    Following built-in functions are customized for this class:

    * :func:`len` returns the number of atoms in the instance.
    * :func:`iter` yields :class:`.Atom` instances.

    Indexing :class:`Residue` instances by *atom name* (:func:`str`), e.g.
    ``"CA"`` returns an :class:`.Atom` instance."""

    __slots__ = ['_ag', '_indices', '_hv', '_acsi', '_selstr']

    def __init__(self, ag, indices, hv, acsi=None, **kwargs):

        AtomSubset.__init__(self, ag, indices, acsi, **kwargs)
        self._hv = hv


    def __repr__(self):

        n_csets = self._ag.numCoordsets()
        chain = self.getChid()
        if chain is None:
            chain = ''
        else:
            chain = ' from Chain {0}'.format(self.getChid())

        if n_csets == 1:
            return ('<Residue: {0} {1}{2}{3} from {4} ({5} atoms)>'
                    ).format(self.getResname(), self.getResnum(),
                     self.getIcode() or '', chain, self._ag.getTitle(),
                     len(self))
        elif n_csets > 1:
            return ('<Residue: {0} {1}{2}{3} from {4} '
                    '({5} atoms; active #{6} of {7} coordsets)>').format(
                    self.getResname(), self.getResnum(), self.getIcode() or '',
                    chain, self._ag.getTitle(), len(self), self.getACSIndex(),
                    n_csets)
        else:
            return ('<Residue: {0} {1}{2}{3} from {4} ({5} atoms; '
                    'no coordinates)>').format(self.getResname(),
                    self.getResnum(), self.getIcode() or '', chain,
                    self._ag.getTitle(), len(self))

    def __str__(self):

        return '{0} {1}{2}'.format(self.getResname(), self.getResnum(),
                                         self.getIcode() or '')

    def getAtom(self, name):
        """Return atom with given *name*, ``None`` if not found.  Assumes that
        atom names in the residue are unique.  If more than one atoms with the
        given *name* exists, the one with the smaller index will be returned.
        """

        acsi = self.getACSIndex()
        if isinstance(name, str):
            nz = (self.getNames() == name).nonzero()[0]
            if len(nz) > 0:
                return Atom(self._ag, self._indices[nz[0]], acsi)

    __getitem__ = getAtom

    def getChain(self):
        """Return the chain that the residue belongs to."""

        chid = self.getChid()
        if chid is not None:
            return self._hv.getChain(chid)

    def getResnum(self):
        """Return residue number."""

        return self._ag._getResnums()[self._indices[0]]

    def setResnum(self, number):
        """Set residue number."""

        self.setResnums(number)

    def getResname(self):
        """Return residue name."""

        data = self._ag._getResnames()
        if data is not None:
            return data[self._indices[0]]

    def setResname(self, name):
        """Set residue name."""

        self.setResnames(name)

    def getIcode(self):
        """Return residue insertion code."""

        data = self._ag._getIcodes()
        if data is not None:
            return data[self._indices[0]]

    def setIcode(self, icode):
        """Set residue insertion code."""

        self.setIcodes(icode)

    def getResindex(self):
        """Return residue index."""

        return self._ag._getResindices()[self._indices[0]]

    def getChid(self):
        """Return chain identifier."""

        chids = self._ag._getChids()
        if chids is not None:
            return chids[self._indices[0]]

    def getSegname(self):
        """Return segment name."""

        segnames = self._ag._getSegnames()
        if segnames is not None:
            return segnames[self._indices[0]]

    def getSegment(self):
        """Return segment of the residue."""

        segname = self.getSegname()
        if segname is not None:
            return self._hv.getSegment(segname)

    def getSelstr(self):
        """Return selection string that will select this residue."""

        icode = self.getIcode() or ''
        chain = self.getChain()
        if chain is None:
            if self._selstr:
                return 'resnum {0}{1} and ({1})'.format(
                            self.getResnum(), icode, self._selstr)
            else:
                return 'resnum {0}{1}'.format(self.getResnum(), icode)
        else:
            return 'resnum {0}{1} and ({2})'.format(
                                self.getResnum(), icode, chain.getSelstr())

    def getPrev(self):
        """Return preceding residue in the atom group."""

        nextIndex = self.getResindex()-1
        if nextIndex < 0:
            return None
        return self._hv._getResidue(nextIndex)

    def getNext(self):
        """Return following residue in the atom group."""

        return self._hv._getResidue(self.getResindex()+1)
