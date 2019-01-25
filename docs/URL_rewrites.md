# URL rewrites

## Introduction

Apple's Software Update service has the ability to offer the "correct" catalog to a client that requests simply "index.sucatalog". This ability was first added with OS X Server 10.6.6, and involved the use of Apache's mod_rewrite.

This feature is handy, as it greatly simplifies client configuration. You no longer need to take client OS version into consideration when setting the CatalogURL for the client.

Lion Server's Software Update service has a similar capability, but this is done via a CGI instead.

Since Reposado doesn't handle the web-serving part of offering Apple software updates, Reposado itself cannot provide a similar feature: instead you must configure your web server to do URL rewrites, or write your own CGI to provide this functionality.


## Apache2 mod_rewrite example

If you are using Apache2 as your webserver, you may be able to configure mod_rewrite to return the "correct" OS-specific sucatalog:

Here is an example .htaccess file you could place at the root of your Reposado repo:

	RewriteEngine On
	Options FollowSymLinks
	RewriteBase  /
	RewriteCond %{HTTP_USER_AGENT} Darwin/8
	RewriteRule ^index(.*)\.sucatalog$ content/catalogs/index$1.sucatalog [L]
	RewriteCond %{HTTP_USER_AGENT} Darwin/9
	RewriteRule ^index(.*)\.sucatalog$ content/catalogs/others/index-leopard.merged-1$1.sucatalog [L]
	RewriteCond %{HTTP_USER_AGENT} Darwin/10
	RewriteRule ^index(.*)\.sucatalog$ content/catalogs/others/index-leopard-snowleopard.merged-1$1.sucatalog [L]
	RewriteCond %{HTTP_USER_AGENT} Darwin/11
	RewriteRule ^index(.*)\.sucatalog$ content/catalogs/others/index-lion-snowleopard-leopard.merged-1$1.sucatalog [L]
	RewriteCond %{HTTP_USER_AGENT} Darwin/12
	RewriteRule ^index(.*)\.sucatalog$ content/catalogs/others/index-mountainlion-lion-snowleopard-leopard.merged-1$1.sucatalog [L]
	RewriteCond %{HTTP_USER_AGENT} Darwin/13
	RewriteRule ^index(.*)\.sucatalog$ content/catalogs/others/index-10.9-mountainlion-lion-snowleopard-leopard.merged-1$1.sucatalog [L]
	RewriteCond %{HTTP_USER_AGENT} Darwin/14
	RewriteRule ^index(.*)\.sucatalog$ content/catalogs/others/index-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1$1.sucatalog [L]
	RewriteCond %{HTTP_USER_AGENT} Darwin/15
	RewriteRule ^index(.*)\.sucatalog$ content/catalogs/others/index-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1$1.sucatalog [L]
	RewriteCond %{HTTP_USER_AGENT} Darwin/16
	RewriteRule ^index(.*)\.sucatalog$ content/catalogs/others/index-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1$1.sucatalog [L]
	RewriteCond %{HTTP_USER_AGENT} Darwin/17
	RewriteRule ^index(.*)\.sucatalog$ content/catalogs/others/index-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1$1.sucatalog [L]
	RewriteCond %{HTTP_USER_AGENT} Darwin/18
	RewriteRule ^index(.*)\.sucatalog$ content/catalogs/others/index-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1$1.sucatalog [L]


This requires Apache2 to be configured to actually pay attention to mod_rewrite rules in .htaccess files. See your Apache and mod_rewrite documentation for details.

Note that the format for these rules is specific for use in an .htaccess file. The rules would need to be changed if in the main Apache config file.


## Other web servers

Other web servers support URL rewriting; the specifics are slightly different, but the general concepts are similar.

### nginx

Heig Gregorian has contributed this example of an Nginx configuration. This is an excerpt from the 'server' section of his Nginx config:


	
	if ( $http_user_agent ~ "Darwin/8" ){
	  rewrite ^/index(.*)\.sucatalog$ /content/catalogs/index$1.sucatalog last;
	}
	if ( $http_user_agent ~ "Darwin/9" ){
	  rewrite ^/index(.*)\.sucatalog$ /content/catalogs/others/index-leopard.merged-1$1.sucatalog last;
	}
	if ( $http_user_agent ~ "Darwin/10" ){
	  rewrite ^/index(.*)\.sucatalog$ /content/catalogs/others/index-leopard-snowleopard.merged-1$1.sucatalog last;
	}
	if ( $http_user_agent ~ "Darwin/11" ){
	  rewrite ^/index(.*)\.sucatalog$ /content/catalogs/others/index-lion-snowleopard-leopard.merged-1$1.sucatalog last;
	}
	if ( $http_user_agent ~ "Darwin/12" ){
	  rewrite ^/index(.*)\.sucatalog$ /content/catalogs/others/index-mountainlion-lion-snowleopard-leopard.merged-1$1.sucatalog last;
	}
	if ( $http_user_agent ~ "Darwin/13" ){
	  rewrite ^/index(.*)\.sucatalog$ /content/catalogs/others/index-10.9-mountainlion-lion-snowleopard-leopard.merged-1$1.sucatalog last;
	}
	if ( $http_user_agent ~ "Darwin/14" ){
	  rewrite ^/index(.*)\.sucatalog$ /content/catalogs/others/index-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1$1.sucatalog last;
	}
	if ( $http_user_agent ~ "Darwin/15" ){
	  rewrite ^/index(.*)\.sucatalog$ /content/catalogs/others/index-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1$1.sucatalog last;
	}
	if ( $http_user_agent ~ "Darwin/16" ){
	  rewrite ^/index(.*)\.sucatalog$ /content/catalogs/others/index-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1$1.sucatalog last;
	}
	if ( $http_user_agent ~ "Darwin/17" ){
	  rewrite ^/index(.*)\.sucatalog$ /content/catalogs/others/index-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1$1.sucatalog last;
	}
	if ( $http_user_agent ~ "Darwin/18" ){
	  rewrite ^/index(.*)\.sucatalog$ /content/catalogs/others/index-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1$1.sucatalog last;
	}

Again, consult Nginx documentation for further information about URL rewriting.

### IIS

This was tested successfully on Microsoft IIS 7. IIS 7 does not have URL Rewrite support installed by default, but it can be added by installing a module for the specific version of IIS.

IIS does not support serving certain Apple specific extensions, so the following MIME Types will need to be added. This is example is taken from the web.config in the root of the reposado directory:

	<?xml version="1.0" encoding="UTF-8"?>
	<configuration>
    		<system.webServer>
        		<staticContent>
            			<mimeMap fileExtension="." mimeType="text/xml" />
            			<mimeMap fileExtension=".dist" mimeType="text/xml" />
           			<mimeMap fileExtension=".pkg" mimeType="application/octet-stream" />
            			<mimeMap fileExtension=".pkm" mimeType="application/octet-stream" />
            			<mimeMap fileExtension=".sucatalog" mimeType="text/xml" />
        		</staticContent>
    		</system.webServer>
	</configuration>

Here is an example web.config file located in the html directory of a reposado repository:

	<?xml version="1.0" encoding="UTF-8"?>
	<configuration>
   		<system.webServer>
        		<rewrite>
            			<rules>
                			<rule name="Darwin/16" stopProcessing="true">
                    				<match url="^index(.*)\.sucatalog$" />
                    				<conditions>
                        				<add input="{HTTP_USER_AGENT}" pattern="Darwin/16" />
                    				</conditions>
                    				<action type="Rewrite" url="content/catalogs/others/index-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1{R:1}.sucatalog" />
                			</rule>
                			<rule name="Darwin/17" stopProcessing="true">
                    				<match url="^index(.*)\.sucatalog$" />
                    				<conditions>
                        				<add input="{HTTP_USER_AGENT}" pattern="Darwin/17" />
                    				</conditions>
                    				<action type="Rewrite" url="content/catalogs/others/index-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1{R:1}.sucatalog" />
                			</rule>
                			<rule name="Darwin/18" stopProcessing="true">
                    				<match url="^index(.*)\.sucatalog$" />
                    				<conditions>
                        				<add input="{HTTP_USER_AGENT}" pattern="Darwin/18" />
                    				</conditions>
                    				<action type="Rewrite" url="content/catalogs/others/index-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1{R:1}.sucatalog" />
                			</rule>
            			</rules>
        		</rewrite>
    		</system.webServer>
	</configuration>

## Testing

Reposado can help you test your URL rewrites. When catalogs are written out to disk, a key named "_CatalogName" is added to the catalog with the base filename of the catalog. This allows you to verify that the catalog being returned is the one you expect.

For example, I want to test that I'm getting the Lion catalog:

	% curl --user-agent "Darwin/11.4.0" http://su.example.com/index_testing.sucatalog > /tmp/testing
	  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
	                                 Dload  Upload   Total   Spent    Left  Speed
	100 1024k  100 1024k    0     0  25.1M      0 --:--:-- --:--:-- --:--:-- 32.2M
	
	% tail -5 /tmp/testing
		</dict>
		<key>_CatalogName</key>
		<string>index-lion-snowleopard-leopard.merged-1_testing.sucatalog</string>
	</dict>
	</plist>

The _CatalogName is "index-lion-snowleopard-leopard.merged-1_testing.sucatalog", which is what I expect.

I can repeat the test for Snow Leopard, this time against the "release" branch:

	% curl --user-agent "Darwin/10.8.0" http://su.example.com/index_release.sucatalog > /tmp/release
	  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
	                                 Dload  Upload   Total   Spent    Left  Speed
	100  912k  100  912k    0     0  29.7M      0 --:--:-- --:--:-- --:--:-- 31.8M
	
	% tail -5 /tmp/release
		</dict>
		<key>_CatalogName</key>
		<string>index-leopard-snowleopard.merged-1_release.sucatalog</string>
	</dict>
	</plist>


## Conclusion

Adding URL rewriting to your Reposado web server configuration makes client configuration much simpler, as you no longer have to worry about which OS the client is running.
