# Reference(S) for pef.py

# doc dipslayed:
# 1st element - description
# 2nd element - syntax
# 3rd element - possible vulnerability classes
exploitableFunctionsDesc = {
    "system()": [
        "Allows to execute system command passed as an argument",
        "system ( string $command [, int &$return_var ] ) : string",
        "RCE",
        "high"
    ],
    "exec()": [
        "exec - Execute an external program",
        "exec ( string $command [, array &$output [, int &$return_var ]] ) : string",
        "RCE",
        "high"
    ],
    "call_user_func_array()": [
        "Call a callback with an array of parameters",
        "call_user_func_array ( callable $callback , array $param_arr ) : mixed",
        "RCE",
        "high"
    ],
    "parse_str()": [
        "when parse_str(arg, [target]) parses URL-like string, it sets variables in current scope WITHOUT initializing it",
        "parse_str ( string $encoded_string [, array &$result ] ) : void"
        "Code Injection",
        "high"
    ],
    "fopen()": [
        "Opens file or URL",
        "fopen ( string $filename , string $mode [, bool $use_include_path = FALSE [, resource $context ]] ) : resource",
        "Local File Include; Remote File Include",
        "high"
    ],
    "popen()": [
        "Opens process file pointer. Opens a pipe to a process executed by forking the command given by command",
        "popen ( string $command , string $mode ) : resource",
        "RCE",
        "high"
    ],
    "pcntl_exec()": [
        "Executes specified program in current process space with the given arguments",
        "pcntl_exec ( string $path [, array $args [, array $envs ]] ) : void",
        "RCE",
        "high"
    ],
    "eval()" : [
        "Evaluate a string as PHP code",
        "eval ( string $code ) : mixed",
        "RCE",
        "high"
    ],
    "preg_replace()": [
        "Perform a regular expression search and replace. Searches subject for matches to pattern and replaces them with replacement",
        "preg_replace ( mixed $pattern , mixed $replacement , mixed $subject [, int $limit = -1 [, int &$count ]] ) : mixed",
        "RCE (in certain conditions)",
        "medium"
    ],
    "create_function()": [
        "DEPRECATED as of PHP 7.2.0 - Create an anonymous (lambda-style) function. Creates an anonymous function from the parameters passed, and returns a unique name for it.",
        "create_function ( string $args , string $code ) : string",
        "Code Injection, RCE",
        "medium"
    ],
    "include()": [
        "The include statement includes and evaluates the specified file.",
        "",
        "Code Injection, RCE",
        "high"
    ],
    "require()": [
        "The include statement includes and evaluates the specified file.",
        "",
        "Code Injection, RCE",
        "high"
    ],
    "passthru()": [
        "Execute an external program and display raw output",
        "passthru ( string $command [, int &$return_var ] ) : void",
        "RCE",
        "high"
    ],
    "shell_exec()": [
        "Execute command via shell and return the complete output as a string. This function is identical to the backtick operator.",
        "shell_exec ( string $cmd ) : string",
        "RCE",
        "high"
    ],
    "popen()": [
        "Opens process file pointer. Opens a pipe to a process executed by forking the command given by command.",
        "popen ( string $command , string $mode ) : resource",
        "Code Injection",
        "medium"
    ],
    "proc_open()": [
        "Execute a command and open file pointers for input/output. proc_open() is similar to popen() but provides a much greater degree of control over the program execution.",
        "proc_open ( string $cmd , array $descriptorspec , array &$pipes [, string $cwd = NULL [, array $env = NULL [, array $other_options = NULL ]]] ) : resource",
        "Code Injection",
        "medium"
    ],
    "pcntl_exec()": [
        "Executes the program with the given arguments.",
        "pcntl_exec ( string $path [, array $args [, array $envs ]] ) : void",
        "RCE",
        "high"
    ],
    "extract()" :[
        "Import variables into the current symbol table from an array",
        "extract ( array &$array [, int $flags = EXTR_OVERWRITE [, string $prefix = NULL ]] ) : int",
        "Code Injection",
        "medium"
    ],
    "parse_str()" :[
        "Parses encoded_string as if it were the query string passed via a URL and sets variables in the current scope (or in the array if result is provided).",
        "parse_str ( string $encoded_string [, array &$result ] ) : void",
        "Code Injection",
        "medium"
    ],
    "putenv()":[
        "Sets the value of an environment variable",
        "putenv ( string $setting ) : bool",
        "Code Injection",
        "low"
    ],
    "ini_set()": [
        "Sets the value of the given configuration option. The configuration option will keep this new value during the script's execution, and will be restored at the script's ending.",
        "ini_set ( string $varname , string $newvalue ) : string",
        "PHP Interpreter behavior change; application settings overwrite",
        "low"
    ],
    "mail()":[
        "Sends an email.",
        "mail ( string $to , string $subject , string $message [, mixed $additional_headers [, string $additional_parameters ]] ) : bool",
        "Arbitrary mail sending",
        "low"
    ],
    "echo": [
        "Outputs all parameters. No additional newline is appended.",
        "echo ( string $arg1 [, string $... ] ) : void",
        "XSS, HTML Injection, Content Injection etc.",
        "low"
    ],
    "header()" : [
        "header() is used to send a raw HTTP header.",
        "header ( string $header [, bool $replace = TRUE [, int $http_response_code ]] ) : void",
        "Header Injection (?)",
        "low"
    ],
    "unserialize()": [
        "unserialize() takes a single serialized variable and converts it back into a PHP value.",
        "unserialize ( string $str [, array $options ] ) : mixed",
        "Code Injection, RCE (in certain conditions)",
        "high"
    ],
    "assert()": [
        "assert() will check the given assertion and take appropriate action if its result is FALSE. If the assertion is given as a string it will be evaluated as PHP code by assert() - ONLY PNP <7.2.0",
        "assert ( mixed $assertion [, string $description ] ) : bool (PHP 5,7) assert ( mixed $assertion [, Throwable $exception ] ) : bool (PHP 7)",
        "RCE, Code Injection (in certain conditions)",
        "low"
    ],
    "call_user_func()": [
        "Calls the callback given by the first parameter and passes the remaining parameters as arguments.",
        "call_user_func ( callable $callback [, mixed $... ] ) : mixed",
        "Code Injection",
        "medium"
    ],
    "ereg_replace()" :[
        "This function scans string for matches to pattern, then replaces the matched text with replacement (DEPRECATED in PHP 5.3.0, and REMOVED in PHP 7.0.0.)",
        "ereg_replace ( string $pattern , string $replacement , string $string ) : string",
        "Code Injection",
        "low"
    ],
    "eregi_replace()" :[
        "This function is identical to ereg_replace() except that this ignores case distinction when matching alphabetic characters. (DEPRECATED in PHP 5.3.0, and REMOVED in PHP 7.0.0)",
        "eregi_replace ( string $pattern , string $replacement , string $string ) : string",
        "Code Injection",
        "low"
    ],
    "mb_ereg_replace()": [
        "Scans string for matches to pattern, then replaces the matched text with replacement. Never use the e modifier when working on untrusted input. No automatic escaping will happen (as known from preg_replace()).",
        "mb_ereg_replace ( string $pattern , string $replacement , string $string [, string $option = \"msr\" ] ) : string",
        "Code Injection",
        "low"
    ],
    "mb_eregi_replace()": [
        "Scans string for matches to pattern, then replaces the matched text with replacement. Never use the e modifier when working on untrusted input. No automatic escaping will happen (as known from preg_replace()).",
        "mb_eregi_replace ( string $pattern , string $replace , string $string [, string $option = \"msri\" ] ) : string",
        "Code Injection",
        "low"
    ],
    "virtual()" : [
        "Perform an Apache sub-request (calls url passed as an argument). This function is supported when PHP is installed as an Apache module or by the NSAPI server module",
        "virtual ( string $filename ) : bool",
        "Local File Include, Remote File Include",
        "low"
    ]
}
