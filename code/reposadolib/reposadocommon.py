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
pysuscommon.py

Created by Greg Neagle on 2011-03-03.
"""

import sys
import os
import imp
import plistlib
import time
import urlparse
import warnings
from xml.parsers.expat import ExpatError

def get_main_dir():
    '''Returns the directory name of the script or the directory name of the exe if py2exe was used
    Code from http://www.py2exe.org/index.cgi/HowToDetermineIfRunningFromExe
    '''
    if (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__")):
        return os.path.dirname(sys.executable)
    return os.path.dirname(sys.argv[0])

def prefsFilePath():
    '''Returns path to our preferences file.'''
    return os.path.join(get_main_dir(), 'preferences.plist')


def pref(prefname):
    '''Returns a preference.'''
    default_prefs = {
        'AppleCatalogURLs':                    ['http://swscan.apple.com/content/catalogs/index.sucatalog',
'http://swscan.apple.com/content/catalogs/index-1.sucatalog',
'http://swscan.apple.com/content/catalogs/others/index-leopard.merged-1.sucatalog',
'http://swscan.apple.com/content/catalogs/others/index-leopard-snowleopard.merged-1.sucatalog',
'http://swscan.apple.com/content/catalogs/others/index-lion-snowleopard-leopard.merged-1.sucatalog'],
        'PreferredLocalizations': ['English', 'en'],
        'CurlPath': '/usr/bin/curl'
    }
    try:
        prefs = plistlib.readPlist(prefsFilePath())
    except (IOError, ExpatError):
        prefs = default_prefs
    if prefname in prefs:
        return prefs[prefname]
    elif prefname in default_prefs:
        return default_prefs[prefname]
    else:
        return None
        
        
def validPreferences():
    '''Validates our preferences to make sure needed values are defined
    and paths exist. Returns boolean.'''
    prefs_valid = True
    for pref_name in ['UpdatesRootDir',  'UpdatesMetadataDir']:
        preference = pref(pref_name)
        if not preference:
            print_stderr('ERROR: %s is not defined in %s.' %
                            (pref_name, prefsFilePath()))
            prefs_valid = False
        elif not os.path.exists(preference):
             print_stderr('WARNING: %s "%s" does not exist.'
                          ' Will attempt to create it.' %
                          (pref_name, preference))
    return prefs_valid


def configure_prefs():
    """Configures prefs for use"""   
    _prefs = {}
    keysAndPrompts = [
        ('UpdatesRootDir', 
         'Path to store replicated catalogs and updates'),
        ('UpdatesMetadataDir', 
         'Path to store Reposado metadata'),
        ('LocalCatalogURLBase', 
         'Base URL for your local Software Update Service\n(Example: http://su.your.org -- leave empty if you are not replicating updates)'),
        ]
    if not os.path.exists(pref('CurlPath')):
        keysAndPrompts.append(
        ('CurlPath', 'Path to curl tool (Example: /usr/bin/curl)'))

    for (key, prompt) in keysAndPrompts:
        newvalue = raw_input('%15s [%s]: ' % (prompt, pref(key)))
        _prefs[key] = newvalue or pref(key) or ''

    prefspath = prefsFilePath()
    # retrieve current preferences
    try:
        prefs = plistlib.readPlist(prefspath)
    except (IOError, ExpatError):
        prefs = {}
    # merge edited preferences
    for key in _prefs.keys():
        prefs[key] = _prefs[key]
    # write preferences to our file
    try:
        plistlib.writePlist(prefs, prefspath)
    except (IOError, ExpatError):
        print_stderr('Could not save configuration to %s', prefspath)
    else:
        # check to make sure they're valid
        unused_value = validPreferences()


def str_to_ascii(s):
    """Given str (unicode, latin-1, or not) return ascii.

    Args:
      s: str, likely in Unicode-16BE, UTF-8, or Latin-1 charset
    Returns:
      str, ascii form, no >7bit chars
    """
    try:
        return unicode(s).encode('ascii', 'ignore')
    except UnicodeDecodeError:
        return s.decode('ascii', 'ignore')


def concat_message(msg, *args):
    """Concatenates a string with any additional arguments; drops unicode."""
    msg = str_to_ascii(msg)
    if args:
        args = [str_to_ascii(arg) for arg in args]
        try:
            msg = msg % tuple(args)
        except TypeError:
            warnings.warn(
                'String format does not match concat args: %s' % (
                str(sys.exc_info())))
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
            print >> fileobj, time.strftime(formatstr), msg.encode('UTF-8')
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
        print output
        sys.stdout.flush()


def print_stderr(msg, *args):
    """
    Prints message and args to stderr.
    """
    output = concat_message(msg, *args)
    if LOGFILE:
        log(output)
    else:
        print >> sys.stderr, concat_message(msg, *args)


def writeDataToPlist(data, filename):
    '''Writes a dict or list to a plist in our metadata dir'''
    metadata_dir = pref('UpdatesMetadataDir')
    if not os.path.exists(metadata_dir):
        try:
            os.makedirs(metadata_dir)
        except OSError, errmsg:
            print_stderr(
                'Could not create missing %s because %s', 
                metadata_dir, errmsg)
    try:
        plistlib.writePlist(data, 
            os.path.join(metadata_dir, filename))
    except (IOError, OSError), errmsg:
        print_stderr(
            'Could not write %s because %s', filename, errmsg)
        
        
def getDataFromPlist(filename):
    '''Reads data from a plist in our metadata dir'''
    metadata_dir = pref('UpdatesMetadataDir')
    try:
        return plistlib.readPlist(
            os.path.join(metadata_dir, filename))
    except (IOError, ExpatError):
        return {}


def getDownloadStatus():
    '''Reads download status info from disk'''
    return getDataFromPlist('DownloadStatus.plist')


def writeDownloadStatus(download_status_list):
    '''Writes download status info to disk'''
    writeDataToPlist(download_status_list, 'DownloadStatus.plist')


def getCatalogBranches():
    '''Reads catalog branches info from disk'''
    return getDataFromPlist('CatalogBranches.plist')


def writeCatalogBranches(catalog_branches):
    '''Writes catalog branches info to disk'''
    writeDataToPlist(catalog_branches, 'CatalogBranches.plist')


def getProductInfo():
    '''Reads Software Update product info from disk'''
    return getDataFromPlist('ProductInfo.plist')
    
    
def writeProductInfo(product_info_dict):
    '''Writes Software Update product info to disk'''
    writeDataToPlist(product_info_dict, 'ProductInfo.plist')
        
        
def getFilenameFromURL(url):
    '''Gets the filename from a URL'''
    (unused_scheme, unused_netloc,
        path, unused_query, unused_fragment) = urlparse.urlsplit(url)
    return os.path.basename(path)


def getLocalPathNameFromURL(url, root_dir=None):
    '''Derives the appropriate local path name based on the URL'''
    if root_dir == None:
        root_dir = pref('UpdatesRootDir')
    (unused_scheme, unused_netloc,
        path, unused_query, unused_fragment) = urlparse.urlsplit(url)
    relative_path = path.lstrip('/')
    return os.path.join(root_dir, relative_path)
    

def rewriteOneURL(full_url):
    '''Rewrites a single URL to point to our local replica'''
    our_base_url = pref('LocalCatalogURLBase')
    if not full_url.startswith(our_base_url):
        # only rewrite the URL if needed
        (unused_scheme, unused_netloc,
         path, unused_query, unused_fragment) = urlparse.urlsplit(full_url)
        return our_base_url + path
    else:
        return full_url
        

def rewriteURLsForProduct(product):
    '''Rewrites the URLs for a product'''
    if 'ServerMetadataURL' in product:
        product['ServerMetadataURL'] = rewriteOneURL(
            product['ServerMetadataURL'])
    for package in product.get('Packages', []):
        if 'URL' in package:
            package['URL'] = rewriteOneURL(package['URL'])
        if 'MetadataURL' in package:
            package['MetadataURL'] = rewriteOneURL(
                package['MetadataURL'])
    distributions = product['Distributions']
    for dist_lang in distributions.keys():
        distributions[dist_lang] = rewriteOneURL(
            distributions[dist_lang])


def rewriteURLs(catalog):
    '''Rewrites all the URLs in the given catalog to point to our local
    replica'''
    if pref('LocalCatalogURLBase') == None:
        return
    if 'Products' in catalog:
        product_keys = list(catalog['Products'].keys())
        for product_key in product_keys:
            product = catalog['Products'][product_key]
            rewriteURLsForProduct(product)


def writeAllBranchCatalogs():
    '''Writes out all branch catalogs. Used when we edit branches.'''
    for catalog_URL in pref('AppleCatalogURLs'):
        localcatalogpath = getLocalPathNameFromURL(catalog_URL)
        writeBranchCatalogs(localcatalogpath)


def writeBranchCatalogs(localcatalogpath):
    '''Writes our branch catalogs'''
    catalog = plistlib.readPlist(localcatalogpath)
    downloaded_products = catalog['Products']
    product_info = getProductInfo()
    
    localcatalogname = os.path.basename(localcatalogpath)
    # now strip the '.sucatalog' bit from the name
    # so we can use it to construct our branch catalog names
    if localcatalogpath.endswith('.sucatalog'):
        localcatalogpath = localcatalogpath[0:-10]

    # now write filtered catalogs (branches)
    catalog_branches = getCatalogBranches()
    for branch in catalog_branches.keys():
        branchcatalogpath = localcatalogpath + '_' + branch + '.sucatalog'
        print_stdout('Building %s...' % os.path.basename(branchcatalogpath))
        catalog['Products'] = {}
        for product_key in catalog_branches[branch]:
            if product_key in downloaded_products.keys():
                # add the product to the Products dict
                # for this catalog
                catalog['Products'][product_key] = \
                    downloaded_products[product_key]
            elif pref('LocalCatalogURLBase') and product_key in product_info:
                # Product has probably been deprecated by Apple, 
                # so we're using cached product info
                # First check to see if this product was ever in this
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
                                 product_key, title, version, branch)
                            rewriteURLsForProduct(catalog_entry)
                            catalog['Products'][product_key] = catalog_entry
                            continue
            else:
                if pref('LocalCatalogURLBase') :
                    print_stderr(
                        'WARNING: Product %s not added to branch %s of %s. '
                        'It is not in the corresponding Apple catalogs '
                        'and is not in the ProductInfo cache.', 
                        product_key, branch, localcatalogname)
                else:
                    print_stderr(
                        'WARNING: Product %s not added to branch %s of %s. '
                        'It is not in the corresponding Apple catalog.',
                        product_key, branch, localcatalogname)

        plistlib.writePlist(catalog, branchcatalogpath)


def writeAllLocalCatalogs():
    '''Writes out all local and branch catalogs. Used when we purge products.'''
    for catalog_URL in pref('AppleCatalogURLs'):
        localcatalogpath = getLocalPathNameFromURL(catalog_URL) + '.apple'
        if os.path.exists(localcatalogpath):
            writeLocalCatalogs(localcatalogpath)


def writeLocalCatalogs(applecatalogpath):
    '''Writes our local catalogs based on the Apple catalog'''
    catalog = plistlib.readPlist(applecatalogpath)
    # rewrite the URLs within the catalog to point to the items on our
    # local server instead of Apple's
    rewriteURLs(catalog)
    # remove the '.apple' from the end of the localcatalogpath
    if applecatalogpath.endswith('.apple'):
        localcatalogpath = applecatalogpath[0:-6]
    else:
        localcatalogpath = applecatalogpath
    
    print_stdout('Building %s...' % os.path.basename(localcatalogpath))
    downloaded_products_list = getDownloadStatus()

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
    plistlib.writePlist(catalog, localcatalogpath)

    # now write filtered catalogs (branches) based on this catalog
    writeBranchCatalogs(localcatalogpath)

LOGFILE = None
def main():
    '''Placeholder'''
    pass


if __name__ == '__main__':
    main()

