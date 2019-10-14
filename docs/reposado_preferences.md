# Reposado preferences

Reposado's configuration is defined in a plist file named **preferences.plist** located in the same directory as the *repoutil* script.

Two key/values are required:

- UpdatesRootDir
   
  A string providing a path where the catalogs and update packages should be stored. Example: 
  
    /Volumes/data/reposado/html

- UpdatesMetadataDir
    
  A string providing a path where metadata used by reposado should be should be stored. Example: 
    
    /Volumes/data/reposado/metadata

If you are replicating the updates as well as the catalogs, you must also include:

- LocalCatalogURLBase
    
    This is the "root" URL for your local Software Update repo. Reposado will re-write all product URLs in the update catalogs to use this root URL. For example, a LocalCatalogURLBase of "http://su.myorg.com" will result in a Snow Leopard update catalog URLs like:

    http://su.myorg.com/content/catalogs/others/index-leopard-snowleopard.merged-1.sucatalog

If LocalCatalogURLBase is undefined, only Apple catalogs will be replicated and the URLs will not be re-written.  The actual Software Update packages will not be downloaded. This allows you to have custom catalogs for Apple Software Update, but clients will still download the actual update packages from Apple's servers. If Reposado is configured this way, you will not be able to offer deprecated updates to clients.

Note: if you are serving your softwareupdate repo on a non-standard port (standard ports are 80 for http and 443 for https) the alternate port is part of the LocalCatalogURLBase. An example is "http://su.myorg.com:8088"

*repoutil --config* will allow you to quickly and easily edit the above three values (UpdatesRootDir, UpdatesMetadataDir, LocalCatalogURLBase).


## Optional keys


The following keys are optional and may be defined in preferences.plist for special configurations:

- AdditionalCurlOptions
    
    This is an array of strings that will be used as part of a configuration file passed to curl. A common use for this is to configure HTTP proxy information if needed for your site. Example:
    
      <key>AdditionalCurlOptions</key>
      <array>
          <string>proxy = "web-proxy.yourcompany.com:8080"</string>
      </array>

  See the curl documentation for available options and formatting.

- AppleCatalogURLs

  This is an array of strings that specify the Apple SUS catalog URLs to replicate. If this is undefined, it defaults to:

      <key>AppleCatalogURLs</key>
      <array>
          <string>http://swscan.apple.com/content/catalogs/index.sucatalog</string>
          <string>http://swscan.apple.com/content/catalogs/index-1.sucatalog</string>
          <string>http://swscan.apple.com/content/catalogs/others/index-leopard.merged-1.sucatalog</string>
          <string>http://swscan.apple.com/content/catalogs/others/index-leopard-snowleopard.merged-1.sucatalog</string>
          <string>http://swscan.apple.com/content/catalogs/others/index-lion-snowleopard-leopard.merged-1.sucatalog</string>
          <string>http://swscan.apple.com/content/catalogs/others/index-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog</string>
          <string>https://swscan.apple.com/content/catalogs/others/index-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog</string>
          <string>https://swscan.apple.com/content/catalogs/others/index-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog</string>
          <string>https://swscan.apple.com/content/catalogs/others/index-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog</string>
          <string>https://swscan.apple.com/content/catalogs/others/index-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog</string>
          <string>https://swscan.apple.com/content/catalogs/others/index-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog</string>
          <string>https://swscan.apple.com/content/catalogs/others/index-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog</string>
          <string>https://swscan.apple.com/content/catalogs/others/index-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog</string>
      </array>

  As of the last update to this document, this is the current set of available Apple Software Update catalogs.

- PreferredLocalizations
    
  A list of preferred language localizations for software update descriptions. Defaults to:
    
      <key>PreferredLocalizations</key>
      <array>
          <string>English</string>
          <string>en</string>
      </array>

- CurlPath
    Path to the curl binary tool. Defaults to:

      <key>CurlPath</key>
      <string>/usr/bin/curl</string>


- RepoSyncLogFile
    
  Path to a log file for *repo_sync* output.
  
  Example:
    
      <key>RepoSyncLogFile</key>
      <string>/var/log/reposado_sync.log</string>
    
  Defaults to no log file.

- HumanReadableSizes

  Enable human-readable file sizes in download messages e.g. KB, MB.

  Example:

      <key>HumanReadableSizes</key>
      <true/>

  Defaults to displaying size in bytes.


## Example preferences.plist

  <?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
  <plist version="1.0">
  <dict>
      <key>LocalCatalogURLBase</key>
      <string>http://su.myorg.com</string>
      <key>UpdatesRootDir</key>
      <string>/Volumes/data/reposado/html</string>
      <key>UpdatesMetadataDir</key>
      <string>/Volumes/data/reposado/metadata</string>
  </dict>
  </plist>
