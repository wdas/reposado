# repo_sync

*repo_sync* downloads software update catalogs from Apple's servers and (if configured) also downloads software update packages to be served from your web server.


## Options

	--recheck

Normally, once downloaded, software update packages are not checked for changes against Apple's servers. If you'd like to reverify all downloaded packages (at the cost of increased execution time and additional Internet bandwidth usage), include the --recheck option when calling *repo_sync*.

	--log PATH_TO_LOGFILE

Specify a log file to redirect all output to.


# repoutil

*repoutil* is a tool for getting info about available updates, managing branch catalogs, and configuring Reposado.


## Options


### CONFIGURING REPOSADO
	
	repoutil --configure

Configure key preferences for Reposado. Note this command does not allow you to edit all available Reposado preferences. See reposado_preferences.txt for more information.


### LISTING AVAILABLE PRODUCTS (UPDATES)
	
	repoutil --products [--sort <sort_key>] [--reverse]
	repoutil --updates [--sort <sort_key>] [--reverse]
                        
List available updates. You may optionally sort by date, title, or id, and optionally reverse the sort order. The default sort order is by post date, so that newest updates are listed last. 
Example:

	repoutil --products
	061-1688        Final Cut Express            2.0.3      2005-04-12 [] 
	061-1704        iMovie HD Update             5.0.2      2005-04-14 [] 
	061-1702        iDVD Update                  5.0.1      2005-04-14 [] 
	[...]
	zzz041-0453     Security Update 2011-002     1.0        2011-04-14 [] 
	zzz041-0654     Security Update 2011-002     1.0        2011-04-14 [] 
	zzz041-0656     Security Update 2011-002     1.0        2011-04-14 [] 
	041-0560        Safari                       5.0.5      2011-04-14 ['testing'] 
	zzzz041-0565    Safari                       5.0.5      2011-04-14 ['testing'] 
	zzzz041-0531    iTunes                       10.2.2     2011-04-18 ['testing'] 
	zzzz041-0532    iTunes                       10.2.2     2011-04-18 ['testing']


### LISTING DEPRECATED UPDATES
	
	repoutil --deprecated
                        
List deprecated updates. These are updates that are no longer available from Apple. 
They may have been withdrawn, or have been superseded by newer versions. Example:
<to be generated>


### LISTING AVAILABLE BRANCH CATALOGS
	
	repoutil --branches
                      
List available branch catalogs. Example:

	repoutil --branches
	release
	testing


### CREATING A NEW BRANCH CATALOG
	
	repoutil --new-branch BRANCH_NAME

Creates a new empty branch named BRANCH_NAME. Example:

	repoutil --new-branch testing


### DELETING A BRANCH CATALOG
	
	repoutil --delete-branch BRANCH_NAME

Deletes the branch named BRANCH_NAME.


### COPYING ALL PRODUCTS FROM ONE BRANCH TO ANOTHER
	
	repoutil --copy-branch SOURCE_BRANCH DEST_BRANCH

Copies all items from SOURCE_BRANCH to DEST_BRANCH, completely replacing the contents of DEST_BRANCH with the contents of SOURCE_BRANCH. If DEST_BRANCH does not exist, it will be created.


### LISTING PRODUCTS IN A BRANCH CATALOG
	
	repoutil --list-branch BRANCH_NAME [--sort <sort_key>] [--reverse]
	repoutil --list-catalog BRANCH_NAME [--sort <sort_key>] [--reverse]

List updates in branch BRANCH_NAME. You may optionally sort these.

	repoutil--list-branch testing 
	zzzz041-0565    Safari                       5.0.5      2011-04-14 ['testing'] 
	041-0560        Safari                       5.0.5      2011-04-14 ['testing'] 
	zzzz041-0532    iTunes                       10.2.2     2011-04-18 ['testing'] 
	zzzz041-0531    iTunes                       10.2.2     2011-04-18 ['testing'] 


### GETTING DETAILED INFO ON A PRODUCT
	
	repoutil --product-info PRODUCT_ID
	repoutil --info PRODUCT_ID
                        
Prints detailed info on a specific update. Example:

	repoutil --info 041-0560
	Product:   041-0560
	Title:     Safari
	Version:   5.0.5
	Size:      47.1 MB
	Post Date: 2011-04-14 17:13:16
	AppleCatalogs:
	    http://swscan.apple.com/content/catalogs/index.sucatalog
	    http://swscan.apple.com/content/catalogs/others/index-leopard.merged-1.sucatalog
	    http://swscan.apple.com/content/catalogs/others/index-leopard-snowleopard.merged-1.sucatalog
	Branches:
	           testing
	HTML Description:
	<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
	<html>
	<head>
	  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	  <meta http-equiv="Content-Style-Type" content="text/css">
	  <title></title>
	  <style type="text/css">
	        body { font: 11.0px "Lucida Grande"; }
	        p { margin-left: 0.0px; margin-top: 0.0px; }
	  </style>
	</head>
	<body>
	    <p>This update is recommended for all Safari users and includes the latest security updates.</p>
	
	    <p>For information on the security content of this update, please visit this website: <a href = 'http://support.apple.com/kb/HT1222'>http://support.apple.com/kb/HT1222</a>.</p>
	</p>
	</body>
	</html>


### ADDING PRODUCTS TO A BRANCH CATALOG
	
	repoutil --add-product PRODUCT_ID [PRODUCT_ID ...] BRANCH_NAME
	repoutil --add-update=PRODUCT_ID [PRODUCT_ID ...] BRANCH_NAME
	repoutil --add=PRODUCT_ID [PRODUCT_ID ...] BRANCH_NAME
                        
Add one or more PRODUCT_IDs to catalog branch BRANCH_NAME.
You may add all cached products, including deprecated products to a branch catalog by specifying 'all':

	repoutil --add-product all BRANCH_NAME


### REMOVING PRODUCTS FROM A BRANCH CATALOG
	
	repoutil --remove-product=PRODUCT_ID [PRODUCT_ID ...] BRANCH_NAME
	                        
Remove one or more PRODUCT_IDs from catalog branch BRANCH_NAME.


### PURGING PRODUCTS ENTIRELY
	
	repoutil --purge-product <product_id> [<product_id ...]
 
Purge a product from the local database and and local disk storage.
You can purge all deprecated products that are not in any branch catalogs by specifying the special pseudo-product-id "all-deprecated":

	repoutil --purge-product all-deprecated

By default, *repoutil --purge-product* will print a warning and skip any products that are not deprecated or are in one or more branches.
To override the warning and purge these products anyway, add '--force':

	repoutil --purge-product <product_id> --force

Note: if you purge a deprecated product, it is deleted forever and cannot be redownloaded from Apple.
