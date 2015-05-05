__author__ = 'admin'


# exploitable functions
exploitableFunctions = [" system", " exec", " popen", " pcntl_exec",
                        " eval", " preg_replace", " create_function", " include", " require", " passthru",
                        " shell_exec", " popen", " proc_open",
                        " pcntl_exec", " asset", " extract", " parse_str", " putenv", " ini_set", " mail", " header"]

# dangerous global(s)
globalVars = ["$_POST", "$_GET", "$_COOKIE", "$_REQUEST", "$_SERVER"]

# dangerous patterns - LFI/RFI
fileInclude = ["include($_GET", "require($_GET", "include_once($_GET", "require_once($_GET"]
