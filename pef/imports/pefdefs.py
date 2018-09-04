# Definitions for pef.py

# exploitable functions
exploitableFunctions = ["system(", "exec(", "popen(", "pcntl_exec(",
                        "eval(", "preg_replace(", "create_function(", "include(", "require(", "passthru(",
                        "shell_exec(", "popen(", "proc_open(",
                        "pcntl_exec(", "asset(", "extract(", "parse_str(", "putenv(", "ini_set(",
                        "mail(", "header(", "unserialize("]

# dangerous global(s)
globalVars = ["$_POST", "$_GET", "$_COOKIE", "$_REQUEST", "$_SERVER"]

# dangerous patterns - LFI/RFI
fileInclude = ["include($_GET", "require($_GET",
               "include_once($_GET", "require_once($_GET",
               "include($_REQUEST", "require($_REQUEST", "include_once($_REQUEST", "require_once($_REQUEST"]

# reflected properties which might leads to eg. XSS
reflectedProperties = ["$_SERVER[\"PHP_SELF\"]",
                       "$_SERVER[\"SERVER_ADDR\"]",
                       "$_SERVER[\"SERVER_NAME\"]",
                       "$_SERVER[\"REMOTE_ADDR\"]",
                       "$_SERVER[\"REMOTE_HOST\"]",
                       "$_SERVER[\"REQUEST_URI\"]",
                       "$_SERVER[\"HTTP_USER_AGENT\"]"]
