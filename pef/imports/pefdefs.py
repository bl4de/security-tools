# Definitions for pef.py

# exploitable functions
exploitableFunctions = ["system(", "exec(", "popen(", "pcntl_exec(",
                        "eval(", "preg_replace(", "create_function(", "include(", "require(", "passthru(",
                        "shell_exec(", "popen(", "proc_open(",
                        "pcntl_exec(", "asset(", "extract(", "parse_str(", "putenv(", "ini_set(",
                        "mail(", "header(", "unserialize("]

# other keywords points to critical features, credentials, configs etc.
keywords = [
    "api",
    "api_key",
    "api_secret_key",
    "secret_key",
    "secret",
    "PRIVATE_KEY",
    "private_key",
    "token",
    "CSRF",
    "Arrays.equals",
    "HMAC",
    "random(",
    "mt_rand(",
    "rand(",
    "hashlib",
    "hashed",
    "md5",
    "sha1",
    "sha-1",
    "sha2",
    "sha-2",
    "salt",
    "bcrypt",
    "admin",
    "preg_replace('/.*/e',",
    "include(",
    "include_once(",
    "require(",
    "require_once(",
    "posix_mkfifo(",
    "posix_getlogin(",
    "posix_ttyname(",
    "getenv(",
    "get_current_user(",
    "proc_get_status(",
    "get_cfg_var(",
    "disk_free_space(",
    "disk_total_space(",
    "parse_str(",
    "putenv(",
    "ini_set(",
    "mail(",
    "header",
    "chmod",
    "chown",
    "shell=True",
    "pickle.loads",
    "yaml.load"
]
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
