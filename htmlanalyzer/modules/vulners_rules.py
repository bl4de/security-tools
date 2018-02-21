RULES = {
    "3DM, html": {
        "alias": "3ware",
        "regex": "<title>3ware 3DM([\\d\\.]+)?",
        "type": "software"
    },
    "3ware, headers": {
        "alias": "3ware",
        "regex": "Server:\\s*3ware\\/?([\\d\\.]+)?",
        "type": "software"
    },
    "AMPcms, headers": {
        "alias": "AMP CMS",
        "regex": "X-AMP-Version:\\s*([\\d.]+)",
        "type": "software"
    },
    "AOLserver, headers": {
        "alias": "cpe:/a:aol:aolserver",
        "regex": "Server:\\s*AOLserver/?([\\d.]+)?",
        "type": "cpe"
    },
    "ATEN, headers": {
        "alias": "ATEN",
        "regex": "Server:\\s*ATEN HTTP Server(?:\\(?V?([\\d\\.]+)\\)?)?",
        "type": "software"
    },
    "Adminer, html": {
        "alias": "Adminer",
        "regex": "Adminer</a> <span class=\"version\">([\\d.]+)</span>",
        "type": "software"
    },
    "Adminer, html tag": {
        "alias": "Adminer",
        "regex": "onclick=\"bodyClick\\(event\\);\" onload=\"verifyVersion\\('([\\d.]+)'\\);\">",
        "type": "software"
    },
    "Akka HTTP, headers": {
        "alias": "Akka HTTP",
        "regex": "Server:\\s*akka-http(?:/([\\d.]+))?",
        "type": "software"
    },
    "Allegro RomPager, headers": {
        "alias": "cpe:/a:allegrosoft:rompager",
        "regex": "Server:\\s*Allegro-Software-RomPager(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "Angular Material, script": {
        "alias": "Angular Material",
        "regex": "/([\\d.]+(?:\\-?rc[.\\d]*)*)/angular-material(?:\\.min)?\\.js",
        "type": "software"
    },
    "AngularJS, script": {
        "alias": "Angular",
        "regex": "/([\\d.]+(?:\\-?rc[.\\d]*)*)/angular(?:\\.min)?\\.js",
        "type": "software"
    },
    "Apache, headers": {
        "alias": "httpd",
        "regex": "Server:\\s*(?:Apache(?:$|/([\\d.]+)|[^/-])|(?:^|\b)HTTPD)",
        "type": "software"
    },
    "Apache Tomcat, headers": {
        "alias": "cpe:/a:apache:tomcat",
        "regex": "X-Powered-By:\\s*\bTomcat\b(?:-([\\d.]+))?",
        "type": "cpe"
    },
    "Apache Traffic Server, headers": {
        "alias": "cpe:/a:apache:traffic_server",
        "regex": "Server:\\s*ATS/?([\\d.]+)?",
        "type": "cpe"
    },
    "Artifactory, html": {
        "alias": "cpe:/a:jfrog:artifactory",
        "regex": "<span class=\"version\">Artifactory(?: Pro)?(?: Power Pack)?(?: ([\\d.]+))?",
        "type": "cpe"
    },
    "Artifactory Web Server, headers": {
        "alias": "cpe:/a:jfrog:artifactory",
        "regex": "Server:\\s*Artifactory(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "Atlassian Confluence, html": {
        "alias": "cpe:/a:atlassian:confluence",
        "regex": "Powered by <a href=[^>]+atlassian\\.com/software/confluence(?:[^>]+>Atlassian Confluence</a> ([\\d.]+))?",
        "type": "cpe"
    },
    "Atlassian FishEye, html": {
        "alias": "cpe:/a:atlassian:fisheye",
        "regex": "<title>(?:Log in to )?FishEye (?:and Crucible )?([\\d.]+)?</title>",
        "type": "cpe"
    },
    "Banshee, html": {
        "alias": "cpe:/a:banshee-project:banshee",
        "regex": "Built upon the <a href=\"[^>]+banshee-php\\.org/\">[a-z]+</a>(?:v([\\d.]+))?",
        "type": "cpe"
    },
    "BaseHTTP, headers": {
        "alias": "BaseHTTP",
        "regex": "Server:\\s*BaseHTTP\\/?([\\d\\.]+)?",
        "type": "software"
    },
    "Canon HTTP Server, headers": {
        "alias": "Canon HTTP Server",
        "regex": "Server:\\s*CANON HTTP Server(?:/([\\d.]+))?",
        "type": "software"
    },
    "Catwalk, headers": {
        "alias": "Catwalk Server",
        "regex": "Server:\\s*Catwalk\\/?([\\d\\.]+)?",
        "type": "software"
    },
    "CenteHTTPd, headers": {
        "alias": "CenteHTTPd",
        "regex": "Server:\\s*CenteHTTPd(?:/([\\d.]+))?",
        "type": "software"
    },
    "Chamilo, headers": {
        "alias": "cpe:/a:chamilo:chamilo_lms",
        "regex": "X-Powered-By:\\s*Chamilo ([\\d.]+)",
        "type": "cpe"
    },
    "Chamilo, html": {
        "alias": "cpe:/a:chamilo:chamilo_lms",
        "regex": "\">Chamilo ([\\d.]+)</a>",
        "type": "cpe"
    },
    "Chart.js, script": {
        "alias": "Chart.js",
        "regex": "chartjs\\.org/dist/([\\d.]+(?:-[^/]+)?|master|latest)/Chart.*\\.js",
        "type": "software"
    },
    "Chart.js, cloudflare script": {
        "alias": "Chart.js",
        "regex": "cdnjs\\.cloudflare\\.com/ajax/libs/Chart\\.js/([\\d.]+(?:-[^/]+)?)/Chart.*\\.js",
        "type": "software"
    },
    "Chart.js, jsdelivr script": {
        "alias": "Chart.js",
        "regex": "cdn\\.jsdelivr\\.net/npm/chart\\.js@([\\d.]+(?:-[^/]+)?|latest)/dist/Chart.*\\.js",
        "type": "software"
    },
    "Chart.js, jsdelivr latest script": {
        "alias": "Chart.js",
        "regex": "cdn\\.jsdelivr\\.net/gh/chartjs/Chart\\.js@([\\d.]+(?:-[^/]+)?|latest)/dist/Chart.*\\.js",
        "type": "software"
    },
    "Cherokee, headers": {
        "alias": "cpe:/a:cherokee-project:cherokee",
        "regex": "Server:\\s*Cherokee/([\\d.]+)",
        "type": "cpe"
    },
    "CherryPy, headers": {
        "alias": "cpe:/a:cherrypy:cherrypy",
        "regex": "Server:\\s*CherryPy\\/?([\\d\\.]+)?",
        "type": "cpe"
    },
    "CompaqHTTPServer, headers": {
        "alias": "cpe:/a:compaq:compaqhttpserver",
        "regex": "Server:\\s*CompaqHTTPServer\\/?([\\d\\.]+)?",
        "type": "cpe"
    },
    "Coppermine, html": {
        "alias": "cpe:/a:coppermine-gallery:coppermine_photo_gallery",
        "regex": "<!--Coppermine Photo Gallery ([\\d.]+)",
        "type": "cpe"
    },
    "CouchDB, headers": {
        "alias": "cpe:/a:apache:couchdb",
        "regex": "Server:\\s*CouchDB/([\\d.]+)",
        "type": "cpe"
    },
    "CppCMS, headers": {
        "alias": "CppCMS",
        "regex": "X-Powered-By:\\s*CppCMS/([\\d.]+)",
        "type": "software"
    },
    "Dancer, headers": {
        "alias": "cpe:/a:dancer:dancer",
        "regex": "Server:\\s*Perl Dancer ([\\d.]+)|X-Powered-By:\\s*Perl Dancer ([\\d.]+)",
        "type": "cpe"
    },
    "Danneo CMS, headers": {
        "alias": "cpe:/a:danneo:cms",
        "regex": "X-Powered-By:\\s*CMS Danneo ([\\d.]+)",
        "type": "cpe"
    },
    "Decorum, headers": {
        "alias": "Decorum",
        "regex": "Server:\\s*DECORUM(?:/([\\d.]+))?",
        "type": "software"
    },
    "DirectAdmin, headers": {
        "alias": "cpe:/a:directadmin:directadmin",
        "regex": "Server:\\s*DirectAdmin Daemon v([\\d.]+)",
        "type": "cpe"
    },
    "Django, html": {
        "alias": "cpe:/a:djangoproject:django",
        "regex": "(?:powered by <a[^>]+>Django ?([\\d.]+)?|<input[^>]*name=[\"']csrfmiddlewaretoken[\"'][^>]*>)",
        "type": "cpe"
    },
    "Dojo, script": {
        "alias": "cpe:/a:dojotoolkit:dojo",
        "regex": "([\\d.]+)/dojo/dojo(?:\\.xd)?\\.js",
        "type": "cpe"
    },
    "Doxygen, html": {
        "alias": "Doxygen",
        "regex": "(?:<!-- Generated by Doxygen ([\\d.]+)|<link[^>]+doxygen\\.css)",
        "type": "software"
    },
    "Drupal, headers": {
        "alias": "Drupal",
        "regex": "X-Generator:\\s*Drupal(?:\\s([\\d.]+))?",
        "type": "software"
    },
    "ESERV-10, headers": {
        "alias": "eserv",
        "regex": "Server:\\s*ESERV-10(?:/([\\d.]+))?",
        "type": "software"
    },
    "EmbedThis Appweb, headers": {
        "alias": "cpe:/a:embedthis:appweb",
        "regex": "Server:\\s*Mbedthis-Appweb(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "Embedthis-http, headers": {
        "alias": "cpe:/a:embedthis:appweb",
        "regex": "Server:\\s*Embedthis-http(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "FancyBox, script": {
        "alias": "jQuery FancyBox",
        "regex": "jquery\\.fancybox(?:\\.pack|\\.min)?\\.js(?:\\?v=([\\d.]+))?$",
        "type": "software"
    },
    "FlashCom, headers": {
        "alias": "cpe:/a:macromedia:flash_communication_server",
        "regex": "Server:\\s*FlashCom/?([\\d\\.]+)?",
        "type": "cpe"
    },
    "Flask, headers": {
        "alias": "Werkzeug",
        "regex": "Server:\\s*Werkzeug/?([\\d\\.]+)?",
        "type": "software"
    },
    "FlexCMP, headers": {
        "alias": "FlexCMP",
        "regex": "X-Powered-By:\\s*FlexCMP.+\\[v\\. ([\\d.]+)",
        "type": "software"
    },
    "FlexCMP, html": {
        "alias": "FlexCMP",
        "regex": "<!--[^>]+FlexCMP[^>v]+v\\. ([\\d.]+)",
        "type": "software"
    },
    "FreeBSD, headers": {
        "alias": "cpe:/o:freebsd:freebsd",
        "regex": "Server:\\s*FreeBSD(?: ([\\d.]+))?",
        "type": "cpe"
    },
    "Fusion Ads, script": {
        "alias": "Fusion Ads",
        "regex": "^[^\\/]*//[ac]dn\\.fusionads\\.net/(?:api/([\\d.]+)/)?",
        "type": "software"
    },
    "GitPHP, html": {
        "alias": "GitPHP",
        "regex": "<!-- gitphp web interface ([\\d.]+)",
        "type": "software"
    },
    "GlassFish, headers": {
        "alias": "cpe:/a:oracle:glassfish_server",
        "regex": "Server:\\s*GlassFish(?: Server)?(?: Open Source Edition)?(?: ?/?([\\d.]+))?",
        "type": "cpe"
    },
    "Google Maps, script": {
        "alias": "Google Maps Api",
        "regex": "(?:maps\\.google\\.com/maps\\?file=api(?:&v=([\\d.]+))?|maps\\.google\\.com/maps/api/staticmap)",
        "type": "software"
    },
    "Google PageSpeed, headers": {
        "alias": "cpe:/a:google:mod_pagespeed",
        "regex": "X-Mod-Pagespeed:\\s*([\\d.]+)",
        "type": "cpe"
    },
    "Grandstream, headers": {
        "alias": "cpe:/o:grandstream:gxv_device_firmware",
        "regex": "Server:\\s*Grandstream\\/?([\\d\\.]+)?",
        "type": "cpe"
    },
    "HERE, script": {
        "alias": "HERE Maps JS API",
        "regex": "https?://js\\.cit\\.api\\.here\\.com/se/([\\d.]+)\\/",
        "type": "software"
    },
    "HHVM, headers": {
        "alias": "cpe:/a:facebook:hhvm",
        "regex": "X-Powered-By:\\s*HHVM/?([\\d.]+)?",
        "type": "cpe"
    },
    "HP ChaiServer, headers": {
        "alias": "HP ChaiServer",
        "regex": "Server:\\s*HP-Chai(?:Server|SOE)(?:/([\\d.]+))?",
        "type": "software"
    },
    "HP Compact Server, headers": {
        "alias": "HP Compact Server",
        "regex": "Server:\\s*HP_Compact_Server(?:/([\\d.]+))?",
        "type": "software"
    },
    "HP iLO, headers": {
        "alias": "cpe:/o:hp:integrated_lights-out",
        "regex": "Server:\\s*HP-iLO-Server(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "HTTP-Server, headers": {
        "alias": "example.com HTTP-Server",
        "regex": "Server:\\s*(?:^|[^-])\bHTTP-Server(?: ?/?V?([\\d.]+))?",
        "type": "software"
    },
    "Handlebars, script": {
        "alias": "Handlebars js",
        "regex": "handlebars(?:\\.runtime)?(?:-v([\\d.]+?))?(?:\\.min)?\\.js",
        "type": "software"
    },
    "Happy ICS Server, headers": {
        "alias": "Happy ICS",
        "regex": "Server:\\s*Happy ICS Server(?:/([\\d.]+))?",
        "type": "software"
    },
    "Hiawatha, headers": {
        "alias": "Hiawatha",
        "regex": "Server:\\s*Hiawatha v([\\d.]+)",
        "type": "software"
    },
    "Highlight.js, script": {
        "alias": "Highlight.js",
        "regex": "/highlight\\.js/[\\d.]+?/highlight\\.min\\.js",
        "type": "software"
    },
    "Hogan.js, script": {
        "alias": "Hogan.js",
        "regex": "([\\d.]+)/hogan(?:\\.min)?\\.js",
        "type": "software"
    },
    "IBM HTTP Server, headers": {
        "alias": "IBM HTTP Server",
        "regex": "Server:\\s*IBM_HTTP_Server(?:/([\\d.]+))?",
        "type": "software"
    },
    "IBM Tivoli Storage Manager, headers": {
        "alias": "cpe:/a:ibm:tivoli_storage_manager",
        "regex": "Server:\\s*TSM_HTTP(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "IIS, headers": {
        "alias": "cpe:/a:microsoft:iis",
        "regex": "Server:\\s*IIS(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "Indico, html": {
        "alias": "CERN Indico",
        "regex": "Powered by\\s+(?:CERN )?<a href=\"http://(?:cdsware\\.cern\\.ch/indico/|indico-software\\.org|cern\\.ch/indico)\">(?:CDS )?Indico( [\\d\\.]+)?",
        "type": "software"
    },
    "Indy, headers": {
        "alias": "Indy",
        "regex": "Server:\\s*Indy(?:/([\\d.]+))?",
        "type": "software"
    },
    "Intel Active Management Technology, headers": {
        "alias": "cpe:/o:intel:active_management_technology_firmware",
        "regex": "Server:\\s*Intel\\(R\\) Active Management Technology(?: ([\\d.]+))?",
        "type": "cpe"
    },
    "Invenio, html": {
        "alias": "CDS Invenio",
        "regex": "(?:Powered by|System)\\s+(?:CERN )?<a (?:class=\"footer\" )?href=\"http://(?:cdsware\\.cern\\.ch(?:/invenio)?|invenio-software\\.org|cern\\.ch/invenio)(?:/)?\">(?:CDS )?Invenio</a>\\s*v?([\\d\\.]+)?",
        "type": "software"
    },
    "JBoss Application Server, headers": {
        "alias": "cpe:/a:redhat:jboss_community_application_server",
        "regex": "X-Powered-By:\\s*JBoss(?:-([\\d.]+))?",
        "type": "cpe"
    },
    "JBoss Web, headers": {
        "alias": "cpe:/a:redhat:jboss_enterprise_web_server",
        "regex": "X-Powered-By:\\s*JBossWeb(?:-([\\d.]+))?",
        "type": "cpe"
    },
    "JC-HTTPD, headers": {
        "alias": "JC-HTTPD",
        "regex": "Server:\\s*JC-HTTPD(?:/([\\d.]+))?",
        "type": "software"
    },
    "Java Servlet, headers": {
        "alias": "Java Servlet",
        "regex": "X-Powered-By:\\s*Servlet(?:.([\\d.]+))?",
        "type": "software"
    },
    "JavaServer Faces, headers": {
        "alias": "cpe:/a:oracle:mojarra",
        "regex": "X-Powered-By:\\s*JSF(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "JavaServer Pages, headers": {
        "alias": "JavaServer Pages",
        "regex": "X-Powered-By:\\s*JSP(?:/([\\d.]+))?",
        "type": "software"
    },
    "Jenkins, headers": {
        "alias": "cpe:/a:jenkins:jenkins",
        "regex": "X-Jenkins:\\s*([\\d\\.]+)",
        "type": "cpe"
    },
    "Joomla, headers": {
        "alias": "joomla",
        "regex": "X-Content-Encoded-By:\\s*Joomla! ([\\d.]+)",
        "type": "software"
    },
    "KS_HTTP, headers": {
        "alias": "KS HTTP",
        "regex": "Server:\\s*KS_HTTP\\/?([\\d\\.]+)?",
        "type": "software"
    },
    "Kibana, headers": {
        "alias": "cpe:/a:elasticsearch:kibana",
        "regex": "kbn-version:\\s*^([\\d.]+)$",
        "type": "cpe"
    },
    "KineticJS, script": {
        "alias": "KineticJS",
        "regex": "kinetic(?:-v?([\\d.]+))?(?:\\.min)?\\.js",
        "type": "software"
    },
    "Kohana, headers": {
        "alias": "Kohana",
        "regex": "X-Powered-By:\\s*Kohana Framework ([\\d.]+)",
        "type": "software"
    },
    "Koken, script": {
        "alias": "Koken",
        "regex": "koken(?:\\.js\\?([\\d.]+)|/storage)",
        "type": "software"
    },
    "LabVIEW, headers": {
        "alias": "cpe:/a:ni:labview",
        "regex": "Server:\\s*LabVIEW(?:/([\\d\\.]+))?",
        "type": "cpe"
    },
    "Liferay, headers": {
        "alias": "cpe:/a:liferay:liferay_portal",
        "regex": "Liferay-Portal:\\s*[a-z\\s]+([\\d.]+)",
        "type": "cpe"
    },
    "LinkSmart, script": {
        "alias": "LinkSmart",
        "regex": "^https?://cdn\\.linksmart\\.com/linksmart_([\\d.]+?)(?:\\.min)?\\.js",
        "type": "software"
    },
    "Logitech Media Server, headers": {
        "alias": "Logitech Media Server",
        "regex": "Server:\\s*Logitech Media Server(?: \\(([\\d\\.]+))?",
        "type": "software"
    },
    "Lua, headers": {
        "alias": "cpe:/a:lua:lua",
        "regex": "X-Powered-By:\\s*\bLua(?: ([\\d.]+))?",
        "type": "cpe"
    },
    "MediaTomb, headers": {
        "alias": "MediaTomb",
        "regex": "Server:\\s*MediaTomb(?:/([\\d.]+))?",
        "type": "software"
    },
    "Microsoft HTTPAPI, headers": {
        "alias": "Microsoft HTTPAPI",
        "regex": "Server:\\s*Microsoft-HTTPAPI(?:/([\\d.]+))?",
        "type": "software"
    },
    "MiniServ, headers": {
        "alias": "MiniServ",
        "regex": "Server:\\s*MiniServ\\/?([\\d\\.]+)?",
        "type": "software"
    },
    "MochiWeb, headers": {
        "alias": "cpe:/a:mochiweb_project:mochiweb",
        "regex": "Server:\\s*MochiWeb(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "Monkey HTTP Server, headers": {
        "alias": "cpe:/a:monkey-project:monkey_http_daemon",
        "regex": "Server:\\s*Monkey/?([\\d.]+)?",
        "type": "cpe"
    },
    "Motion-httpd, headers": {
        "alias": "Motion-httpd",
        "regex": "Server:\\s*Motion-httpd(?:/([\\d.]+))?",
        "type": "software"
    },
    "Moxa, headers": {
        "alias": "cpe:/h:moxa",
        "regex": "Server:\\s*MoxaHttp(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "Nginx, headers": {
        "alias": "cpe:/a:nginx:nginx",
        "regex": "Server:\\s*nginx(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "OpenResty, headers": {
        "alias": "OpenResty",
        "regex": "Server:\\s*openresty(?:/([\\d.]+))?",
        "type": "software"
    },
    "OpenSSL, headers": {
        "alias": "OpenSSL",
        "regex": "Server:\\s*OpenSSL(?:/([\\d.]+[a-z]?))?",
        "type": "software"
    },
    "Oracle Commerce, headers": {
        "alias": "cpe:/a:oracle:commerce_platform",
        "regex": "X-ATG-Version:\\s*(?:ATGPlatform/([\\d.]+))?",
        "type": "cpe"
    },
    "Oracle HTTP Server, headers": {
        "alias": "cpe:/a:oracle:http_server",
        "regex": "Server:\\s*Oracle-HTTP-Server(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "Outlook Web App, html": {
        "alias": "OWA",
        "regex": "<link\\s[^>]*href=\"[^\"]*?([\\d.]+)/themes/resources/owafont\\.css",
        "type": "software"
    },
    "PHP": {
        "regex": "PHP/([\\d.]+)",
        "alias": "cpe:/a:php:php",
        "type": "cpe"
    },
    "PHP, headers": {
        "alias": "cpe:/a:php:php",
        "regex": "Server:\\s*php/?([\\d.]+)?|X-Powered-By:\\s*php/?([\\d.]+)?",
        "type": "cpe"
    },
    "PerfSONAR-PS, headers": {
        "alias": "PerfSONAR PS",
        "regex": "User-agent:\\s*perfSONAR-PS/?([\\d\\.]+)?",
        "type": "software"
    },
    "Perl, headers": {
        "alias": "Perl",
        "regex": "Server:\\s*\bPerl\b(?: ?/?v?([\\d.]+))?",
        "type": "software"
    },
    "Petrojs, script": {
        "alias": "Petrojs",
        "regex": "(?:/([\\d.]+)/)?petrojs(?:\\.min)?\\.js",
        "type": "software"
    },
    "Python, headers": {
        "alias": "Python",
        "regex": "Server:\\s*(?:^|\\s)Python(?:/([\\d.]+))?",
        "type": "software"
    },
    "RAID HTTPServer, headers": {
        "alias": "RAID HTTPServer",
        "regex": "Server:\\s*RAID HTTPServer(?:/([\\d.]+))?",
        "type": "software"
    },
    "Rapid Logic, headers": {
        "alias": "Rapid Logic",
        "regex": "Server:\\s*Rapid Logic(?:/([\\d.]+))?",
        "type": "software"
    },
    "React, script": {
        "alias": "React",
        "regex": "/([\\d.]+)/react(?:\\.min)?\\.js",
        "type": "software"
    },
    "Ruby on Rails, headers": {
        "alias": "cpe:/a:rubyonrails:ruby_on_rails",
        "regex": "X-Powered-By:\\s*(?:mod_rails|mod_rack|Phusion[\\._ ]Passenger)(?: \\(mod_rails/mod_rack\\))?(?: ?/?([\\d\\.]+))?",
        "type": "cpe"
    },
    "SUSE, headers": {
        "alias": "cpe:/o:suse:linux_enterprise_server",
        "regex": "Server:\\s*SUSE(?:/?\\s?-?([\\d.]+))?|X-Powered-By:\\s*SUSE(?:/?\\s?-?([\\d.]+))?",
        "type": "cpe"
    },
    "Schneider Web Server, headers": {
        "alias": "Schneider Web Server",
        "regex": "Server:\\s*Schneider-WEB(?:/V?([\\d.]+))?",
        "type": "software"
    },
    "Sentinel Keys Server, headers": {
        "alias": "Sentinel Keys Server",
        "regex": "Server:\\s*SentinelKeysServer\\/?([\\d\\.]+)?",
        "type": "software"
    },
    "Sentinel Protection Server, headers": {
        "alias": "Sentinel Protection Server",
        "regex": "Server:\\s*SentinelProtectionServer\\/?([\\d\\.]+)?",
        "type": "software"
    },
    "Shapecss, script": {
        "alias": "Shapecss",
        "regex": "/([\\d.]+)/shapecss(?:\\.min)?\\.js",
        "type": "software"
    },
    "Shopware, html": {
        "alias": "Shopware",
        "regex": "<title>Shopware ([\\d\\.]+) [^<]+",
        "type": "software"
    },
    "SimpleHTTP, headers": {
        "alias": "SimpleHTTP",
        "regex": "Server:\\s*SimpleHTTP(?:/([\\d.]+))?",
        "type": "software"
    },
    "SonarQubes, html": {
        "alias": "SonarQubes",
        "regex": "<link href=\"/css/sonar\\.css?v=([\\d.]+)",
        "type": "software"
    },
    "SonarQubes, script": {
        "alias": "SonarQubes",
        "regex": "^/js/bundles/sonar\\.js?v=([\\d.]+)$",
        "type": "software"
    },
    "Splunk, html": {
        "alias": "cpe:/a:splunk:splunk",
        "regex": "<p class=\"footer\">&copy; [-\\d]+ Splunk Inc\\.(?: Splunk ([\\d\\.]+(?: build [\\d\\.]*\\d)?))?[^<]*</p>",
        "type": "cpe"
    },
    "SunOS, headers": {
        "alias": "cpe:/o:sun:sunos",
        "regex": "Server:\\s*SunOS( [\\d\\.]+)?|Servlet-engine:\\s*SunOS( [\\d\\.]+)?",
        "type": "cpe"
    },
    "TeamCity, html": {
        "alias": "cpe:/a:jetbrains:teamcity",
        "regex": "<span class=\"versionTag\"><span class=\"vWord\">Version</span> ([\\d\\.]+)",
        "type": "cpe"
    },
    "TornadoServer, headers": {
        "alias": "cpe:/a:tornadoweb:tornado",
        "regex": "Server:\\s*TornadoServer(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "Trac, html": {
        "alias": "cpe:/a:edgewall_software:trac",
        "regex": "Powered by <a href=\"[^\"]*\"><strong>Trac(?:[ /]([\\d.]+))?",
        "type": "cpe"
    },
    "TwistedWeb, headers": {
        "alias": "cpe:/a:twistedmatrix:twistedweb",
        "regex": "Server:\\s*TwistedWeb(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "Vue.js, script": {
        "alias": "Vue.js",
        "regex": "/([\\d.]+)/vue(?:\\.min)?\\.js",
        "type": "software"
    },
    "W3 Total Cache, headers": {
        "alias": "cpe:/a:w3edge:total_cache",
        "regex": "X-Powered-By:\\s*W3 Total Cache(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "WP Rocket, headers": {
        "alias": "WP Rocket",
        "regex": "X-Powered-By:\\s*WP Rocket(?:/([\\d.]+))?",
        "type": "software"
    },
    "Webs, headers": {
        "alias": "Webs",
        "regex": "Server:\\s*Webs\\.com/?([\\d\\.]+)?",
        "type": "software"
    },
    "Winstone Servlet Container, headers": {
        "alias": "cpe:/a:jenkins:jenkins",
        "regex": "Server:\\s*Winstone Servlet (?:Container|Engine) v?([\\d.]+)?|X-Powered-By:\\s*Winstone(?:.([\\d.]+))?",
        "type": "cpe"
    },
    "Wowza Media Server, html": {
        "alias": "Wowza Streaming Engine",
        "regex": "<title>Wowza Media Server \\d+ ((?:\\w+ Edition )?\\d+\\.[\\d\\.]+(?: build\\d+)?)?",
        "type": "software"
    },
    "XAMPP, html": {
        "alias": "cpe:/a:apache_friends:xampp",
        "regex": "<title>XAMPP(?: Version ([\\d\\.]+))?</title>",
        "type": "cpe"
    },
    "Xregex, script": {
        "alias": "Xregex",
        "regex": "/([\\d.]+)/xregex(?:\\.min)?\\.js",
        "type": "software"
    },
    "Xitami, headers": {
        "alias": "cpe:/a:imatix:xitami",
        "regex": "Server:\\s*Xitami(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "YUI Doc, html": {
        "alias": "YUI Doc",
        "regex": "(?:<html[^>]* yuilibrary\\.com/rdf/[\\d.]+/yui\\.rdf|<body[^>]+class=\"yui3-skin-sam)",
        "type": "software"
    },
    "Yaws, headers": {
        "alias": "cpe:/a:yaws:yaws",
        "regex": "Server:\\s*Yaws(?: ([\\d.]+))?",
        "type": "cpe"
    },
    "cPanel, headers": {
        "alias": "cpe:/a:cpanel:cpanel",
        "regex": "Server:\\s*cpsrvd/([\\d.]+)",
        "type": "cpe"
    },
    "debut, headers": {
        "alias": "debut",
        "regex": "Server:\\s*debut\\/?([\\d\\.]+)?",
        "type": "software"
    },
    "eDevice SmartStack, headers": {
        "alias": "eDevice SmartStack",
        "regex": "Server:\\s*eDevice SmartStack(?: ?/?([\\d.]+))?",
        "type": "software"
    },
    "eHTTP, headers": {
        "alias": "eHTTP",
        "regex": "Server:\\s*\beHTTP(?: v?([\\d\\.]+))?",
        "type": "software"
    },
    "gitlist, html": {
        "alias": "gitlist",
        "regex": "<p>Powered by <a[^>]+>GitList ([\\d.]+)",
        "type": "software"
    },
    "gitweb, html": {
        "alias": "gitweb",
        "regex": "<!-- git web interface version ([\\d.]+)?",
        "type": "software"
    },
    "gunicorn, headers": {
        "alias": "gunicorn",
        "regex": "Server:\\s*gunicorn(?:/([\\d.]+))?",
        "type": "software"
    },
    "jQuery, script": {
        "alias": "cpe:/a:jquery:jquery",
        "regex": "/([\\d.]+)/jquery(?:\\.min)?\\.js",
        "type": "software"
    },
    "jQuery Mobile, script": {
        "alias": "jQuery Mobile",
        "regex": "jquery\\.mobile(?:-([\\d.]+rc\\d))?.*\\.js(?:\\?ver=([\\d.]+))??\\1:\\2",
        "type": "software"
    },
    "jQuery UI, script": {
        "alias": "cpe:/a:jqueryui:jquery_ui",
        "regex": "([\\d.]+)/jquery-ui(?:\\.min)?\\.js",
        "type": "cpe"
    },
    "libwww-perl-daemon, headers": {
        "alias": "libwww-perl-daemon",
        "regex": "Server:\\s*libwww-perl-daemon(?:/([\\d\\.]+))?",
        "type": "software"
    },
    "lighttpd, headers": {
        "alias": "cpe:/a:lighttpd:lighttpd",
        "regex": "Server:\\s*lighttpd(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "mini_httpd, headers": {
        "alias": "cpe:/a:acme:mini_httpd",
        "regex": "Server:\\s*mini_httpd(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "mod_auth_pam, headers": {
        "alias": "mod_auth_pam",
        "regex": "Server:\\s*mod_auth_pam(?:/([\\d\\.]+))?",
        "type": "software"
    },
    "mod_dav, headers": {
        "alias": "mod_dav",
        "regex": "Server:\\s*\b(?:mod_)?DAV\b(?:/([\\d.]+))?",
        "type": "software"
    },
    "mod_fastcgi, headers": {
        "alias": "mod_fastcgi",
        "regex": "Server:\\s*mod_fastcgi(?:/([\\d.]+))?",
        "type": "software"
    },
    "mod_jk, headers": {
        "alias": "mod_jk",
        "regex": "Server:\\s*mod_jk(?:/([\\d\\.]+))?",
        "type": "software"
    },
    "mod_perl, headers": {
        "alias": "cpe:/a:apache:mod_perl",
        "regex": "Server:\\s*mod_perl(?:/([\\d\\.]+))?",
        "type": "cpe"
    },
    "mod_python, headers": {
        "alias": "cpe:/a:apache:mod_python",
        "regex": "Server:\\s*mod_python(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "mod_rack, headers": {
        "alias": "cpe:/a:apache:mod_rack",
        "regex": "Server:\\s*mod_rack(?:/([\\d.]+))?|X-Powered-By:\\s*mod_rack(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "mod_rails, headers": {
        "alias": "cpe:/a:apache:mod_rails",
        "regex": "Server:\\s*mod_rails(?:/([\\d.]+))?|X-Powered-By:\\s*mod_rails(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "mod_ssl, headers": {
        "alias": "cpe:/a:modssl:mod_ssl",
        "regex": "Server:\\s*mod_ssl(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "mod_wsgi, headers": {
        "alias": "cpe:/a:modwsgi:mod_wsgi",
        "regex": "Server:\\s*mod_wsgi(?:/([\\d.]+))?|X-Powered-By:\\s*mod_wsgi(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "phpMyAdmin, html": {
        "alias": "cpe:/a:phpmyadmin:phpmyadmin",
        "regex": "(?: \\| phpMyAdmin ([\\d.]+)<\\/title>|PMA_sendHeaderLocation\\(|<link [^>]*href=\"[^\"]*phpmyadmin\\.css\\.php)",
        "type": "cpe"
    },
    "thttpd, headers": {
        "alias": "cpe:/a:acme_labs:thttpd",
        "regex": "Server:\\s*\bthttpd(?:/([\\d.]+))?",
        "type": "cpe"
    },
    "uKnowva, headers": {
        "alias": "uKnowva",
        "regex": "X-Content-Encoded-By:\\s*uKnowva ([\\d.]+)",
        "type": "software"
    },
    "wpCache, headers": {
        "alias": "wpCache",
        "regex": "X-Powered-By:\\s*wpCache(?:/([\\d.]+))?",
        "type": "software"
    },
    "Phusion Passenger": {
        "regex": "Phusion Passenger(?: \\([a-zA-Z_/]+\\))? ([\\d.]+)",
        "alias": "cpe:/a:phusion:passenger",
        "type": "cpe"
    },
    "IBM WebSphere Application Server": {
        "regex": "WebSphere Application Server/([\\d.]+)",
        "alias": "WebSphere",
        "type": "software"
    },
    "jQuery UI Core": {
        "regex": "jQuery UI Core ([\\d.]+)",
        "alias": "jquery-ui",
        "type": "software"
    },
    "Undertow": {
        "regex": "X-Powered-By: Undertow/([\\d.]+)",
        "alias": "cpe:/a:redhat:undertow",
        "type": "cpe"
    },
    "Google Web Toolkit (GWT)": {
        "regex": "\\$gwt_version\\s?=\\s?\"([\\d.]+)\"",
        "alias": "cpe:/a:google:web_toolkit",
        "type": "cpe"
    },
    "CKEditor": {
        "regex": "CKEDITOR.*version:\"([\\d.]+)\"",
        "alias": "cpe:/a:ckeditor:ckeditor",
        "type": "cpe"
    },
    "IBM TeaLeaf": {
        "regex": "X-TeaLeaf-UIEventCapture-Version: ([\\d.]+)",
        "alias": "cpe:/a:ibm:tealeaf_consumer_experience",
        "type": "cpe"
    },
    "Oracle Java": {
        "regex": "Oracle Corporation ([\\d\\._])+",
        "alias": "Oracle Java",
        "type": "software"
    },
    "Handlebars.js": {
        "regex": "Handlebars\\.VERSION\\s*=\\s*[\"']([\\w.]+)[\"']",
        "alias": "Handlebars",
        "type": "software"
    },
    "Microsoft IIS": {
        "regex": "Microsoft-IIS/([\\d.]+)",
        "alias": "cpe:/a:microsoft:iis",
        "type": "cpe"
    },
    "Apache Cocoon": {
        "regex": "X-Cocoon-Version: ([\\d.]+)",
        "alias": "cpe:/a:apache:cocoon",
        "type": "cpe"
    },
    "ASP.Net MVC Framework": {
        "regex": "X-AspNetMvc-Version: ([\\d.]+)",
        "alias": "cpe:/a:microsoft:asp.net",
        "type": "cpe"
    },
    "Microsoft .Net Framework": {
        "regex": "Microsoft \\.NET Framework ([\\d.]+)",
        "alias": "cpe:/a:microsoft:.net_framework",
        "type": "cpe"
    },
    "Microsoft SharePoint": {
        "regex": "MicrosoftSharePointTeamServices: ([\\d.]+)",
        "alias": "cpe:/a:microsoft:sharepoint",
        "type": "cpe"
    },
    "WildFly": {
        "regex": "Server: WildFly/([\\d.]+)",
        "alias": "cpe:/a:redhat:jboss_wildfly_application_server",
        "type": "cpe"
    },
    "JBoss Enterprise Application Platform": {
        "regex": "JBoss-EAP/([\\d.]+)",
        "alias": "cpe:/a:redhat:jboss_enterprise_application_platform",
        "type": "cpe"
    },
    "Oracle iPlanet": {
        "regex": "Sun-Java-System-Web-Server/([\\d.]+.*)",
        "alias": "cpe:/a:oracle:iplanet_web_server",
        "type": "cpe"
    },
    "Igor Sysoev nginx": {
        "regex": "nginx/([\\d.]+)",
        "alias": "cpe:/a:igor_sysoev:nginx",
        "type": "cpe"
    },
    "OpenCms": {
        "regex": "OpenCms/([\\d.]+)",
        "alias": "cpe:/a:alkacon:opencms",
        "type": "cpe"
    },
    "Ember": {
        "regex": "Ember\\.VERSION\\s*=\\s*[\"']([\\w.]+)[\"']",
        "alias": "cpe:/a:emberjs:ember.js",
        "type": "cpe"
    },
    "Tornado Server": {
        "regex": "TornadoServer/([\\d.]+)",
        "alias": "cpe:/a:tornadoweb:tornado",
        "type": "cpe"
    },
    "Nexpose": {
        "regex": "NSC/([\\d.]+) \\(JVM\\)",
        "alias": "cpe:/a:rapid7:nexpose",
        "type": "cpe"
    },
    "Outlook Web Access": {
        "regex": "X-OWA-Version: ([\\d.]+)",
        "alias": "cpe:/a:microsoft:outlook_web_access",
        "type": "cpe"
    },
    "Java Server Faces": {
        "regex": "JSF/([\\d.]+)",
        "alias": "cpe:/a:oracle:mojarra",
        "type": "cpe"
    },
    "Ruby": {
        "regex": "Ruby/([\\d.]+(?:/\\d{4}-\\d{2}-\\d{2})?)",
        "alias": "Ruby",
        "type": "software"
    },
    "Oracle OpenSSO": {
        "regex": "Oracle OpenSSO ([\\d.]+.*)",
        "alias": "cpe:/a:oracle:opensso",
        "type": "cpe"
    },
    "Joomla!": {
        "regex": "Joomla! ([\\d.]+)",
        "alias": "Joomla",
        "type": "software"
    },
    "Apache Coyote (Tomcat)": {
        "regex": "Apache-Coyote/([\\d.]+)",
        "alias": "cpe:/a:apache:tomcat",
        "type": "cpe"
    },
    "Jetty": {
        "regex": "Jetty\\([v\\d.]+\\)",
        "alias": "cpe:/a:mortbay:jetty",
        "type": "cpe"
    },
    "Oracle-Application-Server": {
        "regex": "Oracle-Application-Server-([\\d.]+.*)",
        "alias": "cpe:/a:oracle:application_server",
        "type": "cpe"
    },
    "ASP.Net": {
        "regex": "X-AspNet-Version: ([\\d.]+)",
        "alias": "cpe:/a:microsoft:asp.net",
        "type": "cpe"
    },
    "Microsoft CRM": {
        "regex": "var APPLICATION_FULL_VERSION = '([\\d.]+)';",
        "alias": "cpe:/a:microsoft:business_solutions_crm",
        "type": "cpe"
    },
    "JBoss": {
        "regex": "JBPAPP_([\\d_]+(?:GA)?)",
        "alias": "cpe:/a:redhat:jboss",
        "type": "cpe"
    },
    "jQuery JavaScript Library": {
        "regex": "jQuery JavaScript Library v([\\d.]+)",
        "alias": "jquery",
        "type": "software"
    },
    "Wordpress": {
        "regex": "name=\"generator\" content=\"WordPress ([\\d.]+)\"",
        "alias": "wordpress",
        "type": "software"
    },
    "Java": {
        "regex": "java\\/([\\d\\.\\_]+)",
        "alias": "cpe:/a:oracle:jre",
        "type": "cpe"
    },
    "GlassFish Server": {
        "regex": "GlassFish Server Open Source Edition ([\\d\\.]+)",
        "alias": "cpe:/a:oracle:glassfish_server",
        "type": "cpe"
    },
    "Oracle Weblogic": {
        "regex": "WebLogic (:?Server )?([\\d\\.]+)",
        "alias": "cpe:/a:oracle:weblogic_server",
        "type": "cpe"
    },
    "Oracle Application Server Containers for J2EE 10g": {
        "regex": "Oracle Application Server Containers for J2EE 10g \\(([\\d\\.]+)\\)",
        "alias": "cpe:/a:oracle:application_server",
        "type": "cpe"
    },
    "Oracle Application Server 10g": {
        "regex": "Oracle.Application.Server.10g\\/([\\d\\.]+)",
        "alias": "cpe:/a:oracle:application_server",
        "type": "cpe"
    },
    "Oracle Application Server": {
        "regex": "Oracle Application Server\\/([\\d\\.]+)",
        "alias": "cpe:/a:oracle:application_server",
        "type": "cpe"
    },
    "Oracle9iA": {
        "regex": "Oracle9iAS\\/([\\d\\.]+)",
        "alias": "cpe:/a:oracle:application_server",
        "type": "cpe"
    }
}