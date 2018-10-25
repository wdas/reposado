# Configuring clients to use your Reposado server

If you've never used the Software Update Service on Mac OS X Server, you may be unfamiliar with configuring Mac OS X clients to use a Software Update Server other than Apple's "main" server.

This setting may be controlled by setting the value of CatalogURL in /Library/Preferences/com.apple.SoftwareUpdate.plist. This is commonly done using the command-line 'defaults' tool:

    sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate CatalogURL <catalog_url>

where \<catalog_url> is the URL to the catalog file.

This preference can also be managed via configuration profile, which in turn can be deployed via MDM.

In recent versions of macOS you may also use `sudo softwareupdate --set-catalog <catalog_url>` and for the versions that support it, that might be a "better" method than using `defaults write`.

You can use URL rewriting on your web server to simplify client configuration. See [URL_rewrites.md](./URL_rewrites.md) for more on this.


## Tiger Clients

Tiger clients should use a CatalogURL of the form:

    http://su.yourorg.com/content/catalogs/index.sucatalog

This will offer the same updates as if the client was pointed directly at Apple's servers. If you are using branch catalogs to filter available updates, or to offer deprecated updates, the CatalogURL will take the form of:

    http://su.yourorg.com/content/catalogs/index_<branchname>.sucatalog

where \<branchname> is the name of one of the branch catalogs you've created.


## Leopard Clients

Leopard clients should use a CatalogURL of the form:

    http://su.yourorg.com/content/catalogs/others/index-leopard.merged-1.sucatalog

Branch CatalogURLs take the form of:

    http://su.yourorg.com/content/catalogs/others/index-leopard.merged-1_<branchname>.sucatalog


## Snow Leopard Clients

Snow Leopard clients should use a CatalogURL of the form:

    http://su.yourorg.com/content/catalogs/others/index-leopard-snowleopard.merged-1.sucatalog

Branch CatalogURLs take the form of:

    http://su.yourorg.com/content/catalogs/others/index-leopard-snowleopard.merged-1_<branchname>.sucatalog


## Lion Clients

Lion clients should use a CatalogURL of the form:

    http://su.yourorg.com/content/catalogs/others/index-lion-snowleopard-leopard.merged-1.sucatalog

Branch CatalogURLs take the form of:

    http://su.yourorg.com/content/catalogs/others/index-lion-snowleopard-leopard.merged-1_<branchname>.sucatalog


## Mountain Lion Clients

Mountain Lion clients should use a CatalogURL of the form:

    http://su.yourorg.com/content/catalogs/others/index-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog

Branch CatalogURLs take the form of:

    http://su.yourorg.com/content/catalogs/others/index-mountainlion-lion-snowleopard-leopard.merged-1_<branchname>.sucatalog


## Mavericks Clients

Mavericks clients should use a CatalogURL of the form:

    http://su.yourorg.com/content/catalogs/others/index-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog

Branch CatalogURLs take the form of:

    http://su.yourorg.com/content/catalogs/others/index-10.9-mountainlion-lion-snowleopard-leopard.merged-1_<branchname>.sucatalog


## Yosemite Clients

Yosemite clients should use a CatalogURL of the form:

    http://su.yourorg.com/content/catalogs/others/index-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog

Branch CatalogURLs take the form of:

    http://su.yourorg.com/content/catalogs/others/index-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1_<branchname>.sucatalog


## El Capitan Clients

El Capitan clients should use a CatalogURL of the form:

    http://su.yourorg.com/content/catalogs/others/index-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog

Branch CatalogURLs take the form of:

    http://su.yourorg.com/content/catalogs/others/index-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1_<branchname>.sucatalog


## Sierra Clients

Sierra clients should use a CatalogURL of the form:

    http://su.yourorg.com/content/catalogs/others/index-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog

Branch CatalogURLs take the form of:

    http://su.yourorg.com/content/catalogs/others/index-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1_<branchname>.sucatalog


## High Sierra Clients

High Sierra clients should use a CatalogURL of the form:

    http://su.yourorg.com/content/catalogs/others/index-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog

Branch CatalogURLs take the form of:

    http://su.yourorg.com/content/catalogs/others/index-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1_<branchname>.sucatalog


## Mojave Clients

Testing with the beta releases indicates that Mojave's `softwareupdate` requires the use of https. It also does Extended Validation of TLS certs by default. To disable this, you can set a preference in the com.apple.SoftwareUpdate preferences domain:

`sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate SUDisableEVCheck -bool YES`  
(Or use a configuration profile to manage this preference.)

Mojave clients should use a CatalogURL of the form:

    https://su.yourorg.com/content/catalogs/others/index-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog

Branch CatalogURLs take the form of:

    https://su.yourorg.com/content/catalogs/others/index-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1_<branchname>.sucatalog
    
(More importantly, this means the softwareupdate catalog and products must be served via https -- if you are replicating products locally, this means the LocalCatalogURLBase must also be an https URL.)
