**INTRODUCTION**

Reposado is a set of tools written in Python that replicate the key functionality of Mac OS X Server's Software Update Service.

**LICENSE**

Reposado is licensed under the new BSD license.

**DISCUSSION GROUP**

Discussion for users and developers of Reposado is [here.](http://groups.google.com/group/reposado)

**FEATURES AND CAPABILITIES**

Reposado, together with Python, the "curl" binary tool and a web server such as Apache 2, enables you to host a local Apple Software Update Server on any hardware and OS of your choice.

Reposado contains a tool (repo_sync) to download Software Update catalogs and (optionally) update packages from Apple's servers, enabling you to host them from a local web server.

Additionally, Reposado provides a command-line tool (repoutil) that enables you to create any arbitrary number of "branches" of the Apple catalogs. These branches can contain any subset of the available updates. For example, one could create "testing" and "release" branches, and then set some clients to use the "testing" branch catalog to test newly-released updates. You would set most of your clients to use the "release" branch catalog, which would contain updates that had been through the testing process.

If you configure Reposado to also download the actual updates as well as the catalogs, you can continue to offer updates that have been superseded by more recent updates. For example, if you are currently offering the 10.6.7 updates to your clients, and Apple releases a 10.6.8 update, you can continue to offer the (deprecated) 10.6.7 update until you are ready to release the newer update to your clients. You can even offer the 10.6.7 update to your "release" clients while offering the 10.6.8 update to your "testing" clients. Offering "deprecated" Apple Software Updates is a feature that is difficult with Apple's tools.

**LIMITATIONS AND DEPENDENCIES**

Apple's Software Update Service does a few things. Primarily, it replicates software updates from Apple's servers, downloading them to a local machine. Secondly, it functions as a web server to actually serve these updates to client machines. Reposado does not duplicate the web server portion of Apple's Software Update Service. Instead you may use any existing web server you wish.

Reposado also currently relies on the command-line "curl" binary to download updates from Apple's servers. curl is available on OS X, RedHat Linux, and many other OSes, including Win32 and Win64 versions. See [http://curl.haxx.se](http://curl.haxx.se) for more information.

**MORE INFO**

More information and basic documentation is available here: https://github.com/wdas/reposado/tree/master/docs