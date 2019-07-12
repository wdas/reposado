#!/usr/bin/env python
# encoding: utf-8
#
# Copyright 2011 Disney Enterprises, Inc. All rights reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:

# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in
# the documentation and/or other materials provided with the
# distribution.

# * The names "Disney", "Walt Disney Pictures", "Walt Disney Animation
# Studios" or the names of its contributors may NOT be used to
# endorse or promote products derived from this software without
# specific prior written permission from Walt Disney Pictures.

# Disclaimer: THIS SOFTWARE IS PROVIDED BY WALT DISNEY PICTURES AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE, NONINFRINGEMENT AND TITLE ARE DISCLAIMED.
# IN NO EVENT SHALL WALT DISNEY PICTURES, THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND BASED ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

"""
reposadocommon.py

Created by Greg Neagle on 2011-03-03.
"""

from __future__ import absolute_import
from __future__ import print_function
import sys
import os
import imp
import plistlib
import time
import warnings
from xml.parsers.expat import ExpatError
from xml.dom import minidom
try:
    # Python 2
    from urlparse import urlsplit
except ImportError:
    # Python 3
    from urllib.parse import urlsplit

# wrapper for raw_input in Python 3
try:
    # Python 2
    get_input = raw_input # pylint: disable=raw_input-builtin,invalid-name
except NameError:
    # Python 3
    get_input = input # pylint: disable=input-builtin,invalid-name


def read_plist(filepath):
    '''Wrapper for the differences between Python 2 and Python 3's plistlib'''
    try:
        with open(filepath, "rb") as fileobj:
            return plistlib.load(fileobj)
    except AttributeError:
        # plistlib module doesn't have a load function (as in Python 2)
        return plistlib.readPlist(filepath)


def write_plist(data, filepath):
    '''Wrapper for the differences between Python 2 and Python 3's plistlib'''
    try:
        with open(filepath, "wb") as fileobj:
            plistlib.dump(data, fileobj)
    except AttributeError:
        # plistlib module doesn't have a dump function (as in Python 2)
        plistlib.writePlist(data, filepath)


def get_main_dir():
    '''Returns the directory name of the script or the directory name of the exe
    if py2exe was used
    Code from http://www.py2exe.org/index.cgi/HowToDetermineIfRunningFromExe
    '''
    if (hasattr(sys, "frozen") or hasattr(sys, "importers")
            or imp.is_frozen("__main__")):
        return os.path.dirname(sys.executable)
    return os.path.dirname(sys.argv[0])

def prefs_file_path():
    '''Returns path to our preferences file.'''
    return os.path.join(get_main_dir(), 'preferences.plist')


def pref(prefname):
    '''Returns a preference.'''
    default_prefs = {
        'AppleCatalogURLs': [
            ('http://swscan.apple.com/content/catalogs/'
             'index.sucatalog'),
            ('http://swscan.apple.com/content/catalogs/'
             'index-1.sucatalog'),
            ('http://swscan.apple.com/content/catalogs/others/'
             'index-leopard.merged-1.sucatalog'),
            ('http://swscan.apple.com/content/catalogs/others/'
             'index-leopard-snowleopard.merged-1.sucatalog'),
            ('http://swscan.apple.com/content/catalogs/others/'
             'index-lion-snowleopard-leopard.merged-1.sucatalog'),
            ('http://swscan.apple.com/content/catalogs/others/'
             'index-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog'),
            ('https://swscan.apple.com/content/catalogs/others/'
             'index-10.9-mountainlion-lion-snowleopard-leopard.merged-1'
             '.sucatalog'),
            ('https://swscan.apple.com/content/catalogs/others/'
             'index-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1'
             '.sucatalog'),
            ('https://swscan.apple.com/content/catalogs/others/'
             'index-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard'
             '.merged-1.sucatalog'),
            ('https://swscan.apple.com/content/catalogs/others/'
             'index-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-'
             'leopard.merged-1.sucatalog'),
            ('https://swscan.apple.com/content/catalogs/others/'
             'index-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-'
             'leopard.merged-1.sucatalog'),
            ('https://swscan.apple.com/content/catalogs/others/'
             'index-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-'
             'snowleopard-leopard.merged-1.sucatalog'),
            ('https://swscan.apple.com/content/catalogs/others/'
             'index-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-'
             'snowleopard-leopard.merged-1.sucatalog'),
        ],
        'PreferredLocalizations': ['English', 'en'],
        'CurlPath': '/usr/bin/curl'
    }
    try:
        prefs = read_plist(prefs_file_path())
    except (IOError, ExpatError):
        prefs = default_prefs
    if prefname in prefs:
        return prefs[prefname]
    elif prefname in default_prefs:
        return default_prefs[prefname]
    return None


def valid_preferences():
    '''Validates our preferences to make sure needed values are defined
    and paths exist. Returns boolean.'''
    prefs_valid = True
    for pref_name in ['UpdatesRootDir', 'UpdatesMetadataDir']:
        preference = pref(pref_name)
        if not preference:
            print_stderr(
                'ERROR: %s is not defined in %s.' % (pref_name, prefs_file_path())
            )
            prefs_valid = False
        elif not os.path.exists(preference):
            print_stderr('WARNING: %s "%s" does not exist.'
                         ' Will attempt to create it.' %
                         (pref_name, preference))
    return prefs_valid


def configure_prefs():
    """Configures prefs for use"""
    _prefs = {}
    keys_and_prompts = [
        ('UpdatesRootDir',
         'Filesystem path to store replicated catalogs and updates'),
        ('UpdatesMetadataDir',
         'Filesystem path to store Reposado metadata'),
        ('LocalCatalogURLBase',
         'Base URL for your local Software Update Service\n(Example: '
         'http://su.your.org -- leave empty if you are not replicating '
         'updates)'),
        ]
    if not os.path.exists(pref('CurlPath')):
        keys_and_prompts.append(
            ('CurlPath', 'Path to curl tool (Example: /usr/bin/curl)')
        )

    for (key, prompt) in keys_and_prompts:
        newvalue = get_input('%15s [%s]: ' % (prompt, pref(key)))
        _prefs[key] = newvalue or pref(key) or ''

    prefspath = prefs_file_path()
    # retrieve current preferences
    try:
        prefs = read_plist(prefspath)
    except (IOError, ExpatError):
        prefs = {}
    # merge edited preferences
    for key in _prefs:
        prefs[key] = _prefs[key]
    # write preferences to our file
    try:
        write_plist(prefs, prefspath)
    except (IOError, ExpatError):
        print_stderr('Could not save configuration to %s', prefspath)
    else:
        # check to make sure they're valid
        _ = valid_preferences()


def unicode_or_str(something, encoding="UTF-8"):
    '''Wrapper for unicode vs str'''
    try:
        # Python 2
        # pylint: disable=unicode-builtin
        if isinstance(something, str):
            return unicode(something, encoding)
        return unicode(something)
        # pylint: enable=unicode-builtin
    except NameError:
        # Python 3
        if isinstance(something, bytes):
            return str(something, encoding)
        return str(something)


def concat_message(msg, *args):
    """Concatenates a string with any additional arguments;
    coerces to unicode."""
    msg = unicode_or_str(msg)
    if args:
        args = [unicode_or_str(arg) for arg in args]
        try:
            msg = msg % tuple(args)
        except TypeError:
            warnings.warn(
                'String format does not match concat args: %s'
                % (str(sys.exc_info()))
            )
    return msg


def log(msg):
    """Generic logging function"""
    # date/time format string
    if not LOGFILE:
        return
    formatstr = '%b %d %H:%M:%S'
    try:
        fileobj = open(LOGFILE, mode='a', buffering=1)
        try:
            print(time.strftime(formatstr), msg, file=fileobj)
        except (OSError, IOError):
            pass
        fileobj.close()
    except (OSError, IOError):
        pass


def print_stdout(msg, *args):
    """
    Prints message and args to stdout.
    """
    output = concat_message(msg, *args)
    if LOGFILE:
        log(output)
    else:
        print(output)
        sys.stdout.flush()


def print_stderr(msg, *args):
    """
    Prints message and args to stderr.
    """
    output = concat_message(msg, *args)
    if LOGFILE:
        log(output)
    else:
        print(output, file=sys.stderr)


def human_readable(size_in_bytes):
    """Returns sizes in human-readable units."""
    # pylint: disable=round-builtin,old-division
    try:
        size_in_bytes = int(size_in_bytes)
    except ValueError:
        size_in_bytes = 0
    units = [(" KB", 10**6), (" MB", 10**9), (" GB", 10**12), (" TB", 10**15)]
    for suffix, limit in units:
        if size_in_bytes > limit:
            continue
        else:
            return str(round(size_in_bytes/float(limit/2**10), 1)) + suffix


def write_data_to_plist(data, filename):
    '''Writes a dict or list to a plist in our metadata dir'''
    metadata_dir = pref('UpdatesMetadataDir')
    if not os.path.exists(metadata_dir):
        try:
            os.makedirs(metadata_dir)
        except OSError as errmsg:
            print_stderr(
                'Could not create missing %s because %s',
                metadata_dir, errmsg)
    try:
        write_plist(
            data, os.path.join(metadata_dir, filename))
    except (IOError, OSError, TypeError) as errmsg:
        print_stderr(
            'Could not write %s because %s', filename, errmsg)


def get_data_from_plist(filename):
    '''Reads data from a plist in our metadata dir'''
    metadata_dir = pref('UpdatesMetadataDir')
    try:
        return read_plist(
            os.path.join(metadata_dir, filename))
    except (IOError, ExpatError):
        return {}


def get_download_status():
    '''Reads download status info from disk'''
    return get_data_from_plist('DownloadStatus.plist')


def write_download_status(download_status_list):
    '''Writes download status info to disk'''
    write_data_to_plist(download_status_list, 'DownloadStatus.plist')


def get_catalog_branches():
    '''Reads catalog branches info from disk'''
    return get_data_from_plist('CatalogBranches.plist')


def write_catalog_branches(catalog_branches):
    '''Writes catalog branches info to disk'''
    write_data_to_plist(catalog_branches, 'CatalogBranches.plist')


def get_product_info():
    '''Reads Software Update product info from disk'''
    return get_data_from_plist('ProductInfo.plist')


def write_product_info(product_info_dict):
    '''Writes Software Update product info to disk'''
    write_data_to_plist(product_info_dict, 'ProductInfo.plist')


def get_filename_from_url(url):
    '''Gets the filename from a URL'''
    (unused_scheme, unused_netloc,
     path, unused_query, unused_fragment) = urlsplit(url)
    return os.path.basename(path)


def get_local_pathname_from_url(url, root_dir=None):
    '''Derives the appropriate local path name based on the URL'''
    if root_dir is None:
        root_dir = pref('UpdatesRootDir')
    (unused_scheme, unused_netloc,
     path, unused_query, unused_fragment) = urlsplit(url)
    relative_path = path.lstrip('/')
    return os.path.join(root_dir, relative_path)


def rewrite_one_url(full_url):
    '''Rewrites a single URL to point to our local replica'''
    our_base_url = pref('LocalCatalogURLBase')
    if not full_url.startswith(our_base_url):
        # only rewrite the URL if needed
        (unused_scheme, unused_netloc,
         path, unused_query, unused_fragment) = urlsplit(full_url)
        return our_base_url + path
    return full_url


def rewrite_urls_for_product(product):
    '''Rewrites the URLs for a product'''
    if 'ServerMetadataURL' in product:
        product['ServerMetadataURL'] = rewrite_one_url(
            product['ServerMetadataURL'])
    for package in product.get('Packages', []):
        if 'URL' in package:
            package['URL'] = rewrite_one_url(package['URL'])
        if 'MetadataURL' in package:
            package['MetadataURL'] = rewrite_one_url(
                package['MetadataURL'])
        if 'IntegrityDataURL' in package:
            package['IntegrityDataURL'] = rewrite_one_url(
                package['IntegrityDataURL'])
        # workaround for 10.8.2 issue where client ignores local pkg
        # and prefers Apple's URL. Need to revisit as we better understand this
        # issue
        if 'Digest' in package:
            # removing the Digest causes 10.8.2 to use the replica's URL
            # instead of Apple's
            del package['Digest']
    distributions = product['Distributions']
    for dist_lang in list(distributions.keys()):
        distributions[dist_lang] = rewrite_one_url(
            distributions[dist_lang])


def rewrite_urls(catalog):
    '''Rewrites all the URLs in the given catalog to point to our local
    replica'''
    if pref('LocalCatalogURLBase') is None:
        return
    if 'Products' in catalog:
        product_keys = list(catalog['Products'].keys())
        for product_key in product_keys:
            product = catalog['Products'][product_key]
            rewrite_urls_for_product(product)


def write_all_branch_catalogs():
    '''Writes out all branch catalogs. Used when we edit branches.'''
    for catalog_url in pref('AppleCatalogURLs'):
        localcatalogpath = get_local_pathname_from_url(catalog_url)
        if os.path.exists(localcatalogpath):
            write_branch_catalogs(localcatalogpath)
        else:
            print_stderr(
                'WARNING: %s does not exist. Perhaps you need to run repo_sync?'
                % localcatalogpath)


def write_branch_catalogs(localcatalogpath):
    '''Writes our branch catalogs'''
    catalog = read_plist(localcatalogpath)
    downloaded_products = catalog['Products']
    product_info = get_product_info()

    localcatalogname = os.path.basename(localcatalogpath)
    # now strip the '.sucatalog' bit from the name
    # so we can use it to construct our branch catalog names
    if localcatalogpath.endswith('.sucatalog'):
        localcatalogpath = localcatalogpath[0:-10]

    # now write filtered catalogs (branches)
    catalog_branches = get_catalog_branches()
    for branch in catalog_branches.keys():
        branchcatalogpath = localcatalogpath + '_' + branch + '.sucatalog'
        print_stdout('Building %s...' % os.path.basename(branchcatalogpath))
        # embed branch catalog name into the catalog for troubleshooting
        # and validation
        catalog['_CatalogName'] = os.path.basename(branchcatalogpath)
        catalog['Products'] = {}
        for product_key in catalog_branches[branch]:
            if product_key in list(downloaded_products.keys()):
                # add the product to the Products dict
                # for this catalog
                catalog['Products'][product_key] = \
                    downloaded_products[product_key]
            elif pref('LocalCatalogURLBase') and product_key in product_info:
                # Product might have been deprecated by Apple,
                # so we check cached product info
                # Check to see if this product was ever in this
                # catalog
                original_catalogs = product_info[product_key].get(
                    'OriginalAppleCatalogs', [])
                for original_catalog in original_catalogs:
                    if original_catalog.endswith(localcatalogname):
                        # this item was originally in this catalog, so
                        # we can add it to the branch
                        catalog_entry = \
                            product_info[product_key].get('CatalogEntry')
                        title = product_info[product_key].get('title')
                        version = product_info[product_key].get('version')
                        if catalog_entry:
                            print_stderr(
                                'WARNING: Product %s (%s-%s) in branch %s '
                                'has been deprecated. Will use cached info '
                                'and packages.',
                                product_key, title, version, branch
                            )
                            rewrite_urls_for_product(catalog_entry)
                            catalog['Products'][product_key] = catalog_entry
                            continue
            else:
                # item is not listed in the main catalog and we don't have a
                # local cache of product info. It either was never in this
                # catalog or has been removed by Apple. In either case, we just
                # skip the item -- we can't add it to the catalog.
                pass

        write_plist(catalog, branchcatalogpath)


def write_all_local_catalogs():
    '''Writes out all local and branch catalogs. Used when we purge products.'''
    for catalog_url in pref('AppleCatalogURLs'):
        localcatalogpath = get_local_pathname_from_url(catalog_url) + '.apple'
        if os.path.exists(localcatalogpath):
            write_local_catalogs(localcatalogpath)


def write_local_catalogs(applecatalogpath):
    '''Writes our local catalogs based on the Apple catalog'''
    catalog = read_plist(applecatalogpath)
    # rewrite the URLs within the catalog to point to the items on our
    # local server instead of Apple's
    rewrite_urls(catalog)
    # remove the '.apple' from the end of the localcatalogpath
    if applecatalogpath.endswith('.apple'):
        localcatalogpath = applecatalogpath[0:-6]
    else:
        localcatalogpath = applecatalogpath

    print_stdout('Building %s...' % os.path.basename(localcatalogpath))
    catalog['_CatalogName'] = os.path.basename(localcatalogpath)
    downloaded_products_list = get_download_status()

    downloaded_products = {}
    product_keys = list(catalog['Products'].keys())
    # filter Products, removing those that haven't been downloaded
    for product_key in product_keys:
        if product_key in downloaded_products_list:
            downloaded_products[product_key] = \
                catalog['Products'][product_key]
        else:
            print_stderr('WARNING: did not add product %s to '
                         'catalog %s because it has not been downloaded.',
                         product_key, os.path.basename(applecatalogpath))
    catalog['Products'] = downloaded_products

    # write raw (unstable/development) catalog
    # with all downloaded Apple updates enabled
    write_plist(catalog, localcatalogpath)

    # now write filtered catalogs (branches) based on this catalog
    write_branch_catalogs(localcatalogpath)


def read_xml_file(filename):
    '''Return dom from XML file or None'''
    try:
        dom = minidom.parse(filename)
    except ExpatError:
        print_stderr(
            'Invalid XML in %s', filename)
        return None
    except IOError as err:
        print_stderr(
            'Error reading %s: %s', filename, err)
        return None
    return dom


def write_xml_to_file(node, path):
    '''Write XML dom node to file'''
    xml_string = node.toxml('utf-8')
    try:
        fileobject = open(path, mode='w')
        print(xml_string, file=fileobject)
        fileobject.close()
    except (OSError, IOError):
        print_stderr('Couldn\'t write XML to %s' % path)


def remove_config_data_attr(product_list):
    '''Wrapper to emulate previous behavior of remove-only only operation.'''
    check_or_remove_config_data_attr(product_list, remove_attr=True)


def check_or_remove_config_data_attr( # pylint: disable=invalid-name
        product_list, remove_attr=False, products=None, suppress_output=False):
    '''Loop through the type="config-data" attributes from the distribution
    options for a list of products. Return a list of products that have
    this attribute set or if `remove_attr` is specified then remove the
    attribute from the distribution file.

    This makes softwareupdate find and display updates like
    XProtectPlistConfigData and Gatekeeper Configuration Data, which it
    normally does not.'''
    if not products:
        products = get_product_info()
    config_data_products = set()
    for key in product_list:
        if key in products:
            if products[key].get('CatalogEntry'):
                distributions = products[key]['CatalogEntry'].get(
                    'Distributions', {})
                for lang in distributions.keys():
                    dist_path = get_local_pathname_from_url(
                        products[key]['CatalogEntry']['Distributions'][lang])
                    if not os.path.exists(dist_path):
                        continue
                    dom = read_xml_file(dist_path)
                    if dom:
                        found_config_data = False
                        option_elements = (
                            dom.getElementsByTagName('options') or [])
                        for element in option_elements:
                            if 'type' in list(element.attributes.keys()):
                                if (element.attributes['type'].value
                                        == 'config-data'):
                                    found_config_data = True
                                    config_data_products.add(key)
                                    if remove_attr:
                                        element.removeAttribute('type')
                        # done editing dom
                        if found_config_data and remove_attr:
                            try:
                                write_xml_to_file(dom, dist_path)
                            except (OSError, IOError):
                                pass
                            else:
                                if not suppress_output:
                                    print_stdout('Updated dist: %s', dist_path)
                        elif not found_config_data:
                            if not suppress_output:
                                print_stdout('No config-data in %s', dist_path)
    return list(config_data_products)

LOGFILE = None
def main():
    '''Placeholder'''
    pass


if __name__ == '__main__':
    main()
