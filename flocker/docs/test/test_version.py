# Copyright Hybrid Logic Ltd.  See LICENSE file for details.

"""
Test for :module:`flocker.docs.version`.
"""


from twisted.trial.unittest import SynchronousTestCase

from .._version import (
    parse_version, FlockerVersion,
    get_doc_version, is_release,
)


class ParseVersionTests(SynchronousTestCase):
    """
    Test for :function:`parse_version`.
    """
    def assertParsedVersion(self, version, **expected_parts):
        """
        Assert that :function:`parse_version` returns ``expected_parts``.
        The release is expected to be `0.3.2`.
        """
        parts = {
            'major': '0',
            'minor': '3',
            'micro': '2',
        }
        parts.update(expected_parts)
        self.assertEqual(parse_version(version), FlockerVersion(**parts))

    def test_release(self):
        """
        When the version is from a release, the documentation version is left
        unchanged.
        """
        self.assertParsedVersion('0.3.2')

    def test_development_vesion(self):
        """
        When the version is from a development version, the documentation
        version is left unchanged.
        """
        self.assertParsedVersion('0.3.2-1-gf661a6a',
                                 commit_count='1',
                                 commit_hash='f661a6a')

    def test_dirty(self):
        """
        When the version is dirty, the documentation version is left unchanged.
        """
        self.assertParsedVersion('0.3.2-1-gf661a6a-dirty',
                                 commit_count='1',
                                 commit_hash='f661a6a',
                                 dirty='-dirty')

    def test_doc(self):
        """
        When the documentation version is from a documentation release, the
        trailing '+doc.X' is stripped.
        """
        self.assertParsedVersion('0.3.2+doc.11',
                                 documentation_revision='11')

    def test_doc_dirty(self):
        """
        When the version is from a documentation release but is dirty, the
        documentation version is left unchanged.
        """
        self.assertParsedVersion('0.3.2+doc.11-dirty',
                                 documentation_revision='11',
                                 dirty='-dirty')


class GetDocVersionTests(SynchronousTestCase):
    """
    Test for :function:`get_doc_version`.
    """

    def test_release(self):
        """
        When the version is from a release, the documentation version is left
        unchanged.
        """
        self.assertEqual(get_doc_version('0.3.2'), '0.3.2')

    def test_development_vesion(self):
        """
        When the version is from a development version, the documentation
        version is left unchanged.
        """
        self.assertEqual(get_doc_version('0.3.2-1-gf661a6a'),
                         '0.3.2-1-gf661a6a')

    def test_dirty(self):
        """
        When the version is dirty, the documentation version is left unchanged.
        """
        self.assertEqual(get_doc_version('0.3.2-1-gf661a6a-dirty'),
                         '0.3.2-1-gf661a6a-dirty')

    def test_doc(self):
        """
        When the documentation version is from a documentation release, the
        trailing '+doc.X' is stripped.
        """
        self.assertEqual(get_doc_version('0.3.2+doc.11'), '0.3.2')

    def test_doc_dirty(self):
        """
        When the version is from a documentation release but is dirty, the
        documentation version is left unchanged.
        """
        self.assertEqual(get_doc_version('0.3.2+doc.0-dirty'),
                         '0.3.2+doc.0-dirty')


class IsReleaseTests(SynchronousTestCase):
    """
    Test for :function:`is_release`.
    """

    def test_release(self):
        """
        When the version is from a release, it is a release.
        """
        self.assertTrue(is_release('0.3.2'))

    def test_development_vesion(self):
        """
        When the version is from a development version, it isn't a release.
        """
        self.assertFalse(is_release('0.3.2-1-gf661a6a'))

    def test_dirty(self):
        """
        When the version is dirty, it isn't a release.
        """
        self.assertFalse(is_release('0.3.2-1-gf661a6a-dirty'))

    def test_doc(self):
        """
        When the documentation version is from a documentation release, it is a
        release.  """
        self.assertTrue(is_release('0.3.2+doc.11'))

    def test_doc_dirty(self):
        """
        When the version is from a documentation release but is dirty, it isn't
        a release.
        """
        self.assertFalse(is_release('0.3.2+doc.0-dirty'))
