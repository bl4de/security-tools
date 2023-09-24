# Reference(S) for pef.py

# doc dipslayed:
# 1st element - description
# 2nd element - syntax
# 3rd element - possible vulnerability classes
exploitableFunctionsDesc = {
    "`": [
        "Allows to execute system command",
        "`$command`",
        "RCE",
        "critical",
        "sink"
    ],
    "system()": [
        "Allows to execute system command passed as an argument",
        "system ( string $command [, int &$return_var ] ) : string",
        "RCE",
        "critical",
        "sink"
    ],
    "exec()": [
        "exec - Execute an external program",
        "exec ( string $command [, array &$output [, int &$return_var ]] ) : string",
        "RCE",
        "critical",
        "sink"
    ],
    "call_user_func_array()": [
        "Call a callback with an array of parameters",
        "call_user_func_array ( callable $callback , array $param_arr ) : mixed",
        "RCE",
        "high",
        "sink"
    ],
    "parse_url()": [
        "parse_url — Parse a URL and return its components",
        "parse_url(string $url, int $component = -1): mixed",
        "SSRF, Filter Bypass",
        "medium",
        "sink"
    ],
    "parse_str()": [
        "when parse_str(arg, [target]) parses URL-like string, it sets variables in current scope WITHOUT initializing it",
        "parse_str ( string $encoded_string [, array &$result ] ) : void"
        "Code Injection",
        "high",
        "sink"
    ],
    "eval()": [
        "Evaluate a string as PHP code",
        "eval ( string $code ) : mixed",
        "RCE",
        "critical",
        "sink"
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
        "medium",
        "sink"
    ],
    "passthru()": [
        "Execute an external program and display raw output",
        "passthru ( string $command [, int &$return_var ] ) : void",
        "RCE",
        "critical",
        "sink"
    ],
    "shell_exec()": [
        "Execute command via shell and return the complete output as a string. This function is identical to the backtick operator.",
        "shell_exec ( string $cmd ) : string",
        "RCE",
        "critical",
        "sink"
    ],
    "popen()": [
        "Opens process file pointer. Opens a pipe to a process executed by forking the command given by command.",
        "popen ( string $command , string $mode ) : resource",
        "Code Injection",
        "medium",
        "sink"
    ],
    "proc_open()": [
        "Execute a command and open file pointers for input/output. proc_open() is similar to popen() but provides a much greater degree of control over the program execution.",
        "proc_open ( string $cmd , array $descriptorspec , array &$pipes [, string $cwd = NULL [, array $env = NULL [, array $other_options = NULL ]]] ) : resource",
        "Code Injection",
        "medium",
        "sink"
    ],
    "pcntl_exec()": [
        "Executes the program with the given arguments.",
        "pcntl_exec ( string $path [, array $args [, array $envs ]] ) : void",
        "RCE",
        "critical",
        "sink"
    ],
    "extract()": [
        "Import variables into the current symbol table from an array",
        "extract ( array &$array [, int $flags = EXTR_OVERWRITE [, string $prefix = NULL ]] ) : int",
        "Code Injection",
        "high",
        "sink"
    ],
    "ini_set()": [
        "Sets the value of the given configuration option. The configuration option will keep this new value during the script's execution, and will be restored at the script's ending.",
        "ini_set ( string $varname , string $newvalue ) : string",
        "PHP Interpreter behavior change; application settings overwrite",
        "low"
    ],
    "mail()": [
        "Sends an email.",
        "mail ( string $to , string $subject , string $message [, mixed $additional_headers [, string $additional_parameters ]] ) : bool",
        "Arbitrary mail sending",
        "low",
        "sink"
    ],
    "echo": [
        "Outputs all parameters. No additional newline is appended.",
        "echo ( string $arg1 [, string $... ] ) : void",
        "XSS, HTML Injection, Content Injection etc.",
        "low"
    ],
    "unserialize()": [
        "unserialize() takes a single serialized variable and converts it back into a PHP value.",
        "unserialize ( string $str [, array $options ] ) : mixed",
        "Code Injection, RCE (in certain conditions)",
        "high",
        "sink"
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
        "medium",
        "sink"
    ],
    "ereg_replace()": [
        "This function scans string for matches to pattern, then replaces the matched text with replacement (DEPRECATED in PHP 5.3.0, and REMOVED in PHP 7.0.0.)",
        "ereg_replace ( string $pattern , string $replacement , string $string ) : string",
        "Code Injection",
        "low",
        "sink"
    ],
    "eregi_replace()": [
        "This function is identical to ereg_replace() except that this ignores case distinction when matching alphabetic characters. (DEPRECATED in PHP 5.3.0, and REMOVED in PHP 7.0.0)",
        "eregi_replace ( string $pattern , string $replacement , string $string ) : string",
        "Code Injection",
        "low",
        "sink"
    ],
    "mb_ereg_replace()": [
        "Scans string for matches to pattern, then replaces the matched text with replacement. Never use the e modifier when working on untrusted input. No automatic escaping will happen (as known from preg_replace()).",
        "mb_ereg_replace ( string $pattern , string $replacement , string $string [, string $option = \"msr\" ] ) : string",
        "Code Injection",
        "low",
        "sink"
    ],
    "mb_eregi_replace()": [
        "Scans string for matches to pattern, then replaces the matched text with replacement. Never use the e modifier when working on untrusted input. No automatic escaping will happen (as known from preg_replace()).",
        "mb_eregi_replace ( string $pattern , string $replace , string $string [, string $option = \"msri\" ] ) : string",
        "Code Injection",
        "low",
        "sink"
    ],
    "virtual()": [
        "Perform an Apache sub-request (calls url passed as an argument). This function is supported when PHP is installed as an Apache module or by the NSAPI server module",
        "virtual ( string $filename ) : bool",
        "Local File Include, Remote File Include",
        "low",
        "sink"
    ],
    "readfile()": [
        "Reads a file and writes it to the output buffer.",
        "readfile ( string $filename [, bool $use_include_path = FALSE [, resource $context ]] ) : int",
        "Code Injection, LFI, RFI",
        "high",
        "source"
    ],
    "file_get_contents()": [
        "This function is similar to file(), except that file_get_contents() returns the file in a string, starting at the specified offset up to maxlen bytes. On failure, file_get_contents() will return FALSE.",
        "file_get_contents ( string $filename [, bool $use_include_path = FALSE [, resource $context [, int $offset = 0 [, int $maxlen ]]]] ) : string",
        "Code Injection, LFI, RFI",
        "high",
        "source"
    ],
    "show_source()": [
        "(Alias for highlight_file()) Prints out or returns a syntax highlighted version of the code contained in filename using the colors defined in the built-in syntax highlighter for PHP.",
        "show_source ( string $filename [, bool $return = FALSE ] ) : mixed",
        "Information Disclosure",
        "low",
        "source"
    ],
    "highlight_file()": [
        "Prints out or returns a syntax highlighted version of the code contained in filename using the colors defined in the built-in syntax highlighter for PHP.",
        "highlight_file ( string $filename [, bool $return = FALSE ] ) : mixed",
        "Information Disclosure",
        "low",
        "source"
    ],
    "fopen()": [
        "fopen() binds a named resource, specified by filename, to a stream.",
        "fopen ( string $filename , string $mode [, bool $use_include_path = FALSE [, resource $context ]] ) : resource",
        "Code Injection, LFI, RFI",
        "low",
        "source"
    ],
    "file()": [
        "Reads an entire file into an array.",
        "ile ( string $filename [, int $flags = 0 [, resource $context ]] ) : array",
        "Code Injection, LFI, RFI",
        "low",
        "source"
    ],
    "fpassthru()": [
        "Reads to EOF on the given file pointer from the current position and writes the results to the output buffer.",
        "fpassthru ( resource $handle ) : int",
        "Code Injection, LFI, RFI, RCE (depending on the context)",
        "low",
        "sink"
    ],
    "fsockopen()": [
        "Initiates a socket connection to the resource specified by hostname.",
        "fsockopen ( string $hostname [, int $port = -1 [, int &$errno [, string &$errstr [, float $timeout = ini_get(\"default_socket_timeout\") ]]]] ) : resource",
        "RCE (depends on context)",
        "low",
        "sink"
    ],
    "gzopen()": [
        "Opens a gzip (.gz) file for reading or writing.",
        "gzopen ( string $filename , string $mode [, int $use_include_path = 0 ] ) : resource",
        "Code Injection, LFI (depends on context)",
        "low",
        "sink"
    ],
    "gzread()": [
        "gzread() reads up to length bytes from the given gz-file pointer. Reading stops when length (uncompressed) bytes have been read or EOF is reached, whichever comes first.",
        "gzread ( resource $zp , int $length ) : string",
        "Code Injection, LFI",
        "low",
        "sink"
    ],
    "gzfile()": [
        "Read entire gz-file into an array. This function is identical to readgzfile(), except that it returns the file in an array.",
        "gzfile ( string $filename [, int $use_include_path = 0 ] ) : array",
        "Code Injection, LFI",
        "low",
        "sink"
    ],
    "gzpassthru()": [
        "Output all remaining data on a gz-file pointer. Reads to EOF on the given gz-file pointer from the current position and writes the (uncompressed) results to standard output.",
        "gzpassthru ( resource $zp ) : int",
        "Code Injection, LFI",
        "low",
        "sink"
    ],
    "readgzfile()": [
        "Output a gz-file. Reads a file, decompresses it and writes it to standard output.",
        "readgzfile ( string $filename [, int $use_include_path = 0 ] ) : int",
        "Code Injection, LFI, RCE",
        "medium",
        "sink"
    ],
    "mssql_query()": [
        "Send MS SQL query to the currently active database on the server that's associated with the specified link identifier. This function was REMOVED in PHP 7.0.0.",
        "mssql_query ( string $query [, resource $link_identifier [, int $batch_size = 0 ]] ) : mixed",
        "SQL Injection",
        "high"
    ],
    "odbc_exec()": [
        "Sends an SQL statement to the database server.",
        "odbc_exec ( resource $connection_id , string $query_string [, int $flags ] ) : resource",
        "SQL Injection",
        "high",
        "sink"
    ],
    "sqlsrv_query()": [
        "Prepares and executes a query",
        "sqlsrv_query ( resource $conn , string $sql [, array $params [, array $options ]] ) : mixed",
        "SQL Injection",
        "medium",
        "sink"
    ],
    "PDO::query()": [
        "PDO::query() executes an SQL statement in a single function call, returning the result set (if any) returned by the statement as a PDOStatement object.",
        "public PDO::query ( string $statement , int $PDO::FETCH_CLASS , string $classname , array $ctorargs ) : PDOStatement",
        "SQL Injection",
        "medium",
        "sink"
    ],
    "move_uploaded_file()": [
        "This function checks to ensure that the file designated by filename is a valid upload file (meaning that it was uploaded via PHP's HTTP POST upload mechanism). If the file is valid, it will be moved to the filename given by destination.",
        "move_uploaded_file ( string $filename , string $destination ) : bool",
        "File Include",
        "low",
        "sink"
    ],
    "print()": [
        "Outputs arg. print is not actually a real function (it is a language construct) so you are not required to use parentheses with its argument list.",
        "print ( string $arg ) : int",
        "XSS, Content/HTML Injection",
        "low",
        "sink"
    ],
    "printf()": [
        "Produces output according to format.",
        "printf ( string $format [, mixed $... ] ) : int",
        "XSS, Content/HTML Injection",
        "low",
        "sink"
    ],
    "ldap_search()": [
        "Performs the search for a specified filter on the directory with the scope of LDAP_SCOPE_SUBTREE. This is equivalent to searching the entire directory.",
        "ldap_search ( resource $link_identifier , string $base_dn , string $filter [, array $attributes = array() [, int $attrsonly = 0 [, int $sizelimit = -1 [, int $timelimit = -1 [, int $deref = LDAP_DEREF_NEVER [, array $serverctrls = array() ]]]]]] ) : resource",
        "unknown?",
        "low"
    ],
    "header()": [
        "Send a raw HTTP header",
        "header ( string $header [, bool $replace = TRUE [, int $http_response_code ]] ) : void",
        "Header Injection, Open Redirect",
        "low",
        "sink"
    ],
    "sqlite_query()": [
        "SQLiteDatabase::query - Executes a query against a given database and returns a result handle",
        "sqlite_query ( string $query , resource $dbhandle [, int $result_type = SQLITE_BOTH [, string &$error_msg ]] ) : resource",
        "SQL Injection",
        "medium",
        "sink"
    ],
    "pg_query()": [
        "pg_query() executes the query on the specified database connection. pg_query_params() should be preferred in most cases.",
        "pg_query ([ resource $connection ], string $query ) : resource",
        "SQL Injection",
        "medium",
        "sink"
    ],
    "mysql_query()": [
        "mysql_query() sends a unique query (multiple queries are not supported) to the currently active database on the server that's associated with the specified link_identifier.(deprecated in PHP 5.5.0, and it was removed in PHP 7.0.0)",
        "mysql_query ( string $query [, resource $link_identifier = NULL ] ) : mixed",
        "SQL Injection",
        "high",
        "sink"
    ],
    "mysqli_query()": [
        "Performs a query against the database.",
        "mysqli_query ( mysqli $link , string $query [, int $resultmode = MYSQLI_STORE_RESULT ] ) : mixed",
        "SQL Injection",
        "medium",
        "sink"
    ],
    "mysqli::query()": [
        "Performs a query against the database.",
        "mysqli::query ( string $query [, int $resultmode = MYSQLI_STORE_RESULT ] ) : mixed",
        "SQL Injection",
        "medium",
        "sink"
    ],
    "apache_setenv()": [
        "Sets the value of the Apache environment variable specified by variable.",
        "apache_setenv ( string $variable , string $value [, bool $walk_to_top = FALSE ] ) : bool",
        "ENV server variables overwrite",
        "low",
        "sink"
    ],
    "dl()": [
        "Loads a PHP extension at runtime",
        "dl ( string $library ) : bool",
        "Code Injection, RCE (in certain conditions)",
        "low",
        "sink"
    ],
    "escapeshellarg()": [
        "Escape a string to be used as a shell argument",
        "escapeshellarg ( string $arg ) : string",
        "",
        "low"
    ],
    "escapeshellcmd()": [
        "Escapes any characters in a string that might be used to trick a shell command into executing arbitrary commands",
        "escapeshellcmd ( string $command ) : string",
        "",
        "low"
    ],
    "get_cfg_var()": [
        "Gets the value of a PHP configuration option",
        "get_cfg_var ( string $option ) : mixed",
        "Information Disclosure",
        "low"
    ],
    "get_current_user()": [
        "Gets the name of the owner of the current PHP script",
        "get_current_user ( void ) : string",
        "Information Disclosure",
        "low"
    ],
    "getcwd()": [
        "Gets the current working directory",
        "getcwd ( void ) : string",
        "Information Disclosure",
        "low"
    ],
    "getenv()": [
        " Gets the value of an environment variable",
        "getenv ( string $varname [, bool $local_only = FALSE ] ) : string",
        "Information Disclosure",
        "low"
    ],
    "php_uname()": [
        "Returns information about the operating system PHP is running on",
        "php_uname ([ string $mode = \"a\" ] ) : string",
        "Information Disclosure",
        "low"
    ],
    "phpinfo()": [
        "Outputs information about PHP's configuration",
        "phpinfo ([ int $what = INFO_ALL ] ) : bool",
        "Information Disclosure",
        "medium"
    ],
    "putenv()": [
        "Adds setting to the server environment. The environment variable will only exist for the duration of the current request. At the end of the request the environment is restored to its original state.",
        "putenv ( string $setting ) : bool",
        "ENV variable create/owerwrite",
        "low",
        "sink"
    ],
    "symlink()": [
        "Creates a symbolic link to the existing target with the specified name link.",
        "symlink ( string $target , string $link ) : bool",
        "LFI (in certain conditions)",
        "low"
    ],
    "syslog()": [
        "Generate a system log message",
        "syslog ( int $priority , string $message ) : bool",
        "Log poisoning",
        "low"
    ],
    "curl_exec()": [
        "Execute the given cURL session. This function should be called after initializing a cURL session and all the options for the session are set.",
        "curl_exec ( resource $ch ) : mixed",
        "SSRF",
        "medium",
        "sink"
    ],
    "__destruct()": [
        "unserialize() checks if your class has a function with the magic name __destruct(). If so, that function is executed after unserialization",
        "__destruct ( void ) : void",
        "Object Injection; RCE via unserialize() + POP gadget chain",
        "high",
        "sink"
    ],
    "__wakeup()": [
        "serialize() checks if your class has a function with the magic name __wakeup(). If so, that function is executed prior to any serialization",
        "__wakeup ( void ) : void",
        "Object Injection; RCE via unserialize() + POP gadget chain",
        "medium",
        "sink"
    ],
    "__sleep()": [
        "serialize() checks if your class has a function with the magic name __sleep(). If so, that function is executed prior to any serialization",
        "public __sleep ( void ) : array",
        "Object Injection; RCE via unserialize() + POP gadget chain",
        "medium",
        "sink"
    ],
    "__call()": [
        "Triggered when invoking inaccessible methods in an object context",
        "public __call ( string $name , array $arguments ) : mixed",
        "Object Injection; RCE via unserialize() + POP gadget chain",
        "medium",
        "sink"
    ],
    "__callStatic()": [
        "Triggered when invoking inaccessible methods in a static context.",
        "public static __callStatic ( string $name , array $arguments ) : mixed",
        "Object Injection; RCE via unserialize() + POP gadget chain",
        "medium",
        "sink"
    ],
    "filter_var()": [
        "Filters a variable with a specified filter",
        "filter_var ( mixed $variable [, int $filter = FILTER_DEFAULT [, mixed $options ]] ) : mixed",
        "Validation bypass (in certain conditions)",
        "low"
    ],
    "file_put_contents()": [
        "Write data to a file",
        "file_put_contents ( string $filename , mixed $data [, int $flags = 0 [, resource $context ]] ) : int",
        "Arbitrary file write",
        "medium",
        "source"
    ],
    "SELECT.*FROM": [
        "SQL syntax found.",
        "This is likely a raw SQL query, which can be filled with user provided input or not implemented as prepared statement",
        "SQL Injection",
        "medium",
        "source"
    ],
    "INSERT.*INTO": [
        "SQL syntax found.",
        "This is likely a raw SQL query, which can be filled with user provided input or not implemented as prepared statement",
        "SQL Injection",
        "medium",
        "source"
    ],
    "UPDATE.*": [
        "SQL syntax found.",
        "This is likely a raw SQL query, which can be filled with user provided input or not implemented as prepared statement",
        "SQL Injection",
        "medium",
        "source"
    ],
    "DELETE.*FROM": [
        "SQL syntax found.",
        "This is likely a raw SQL query, which can be filled with user provided input or not implemented as prepared statement",
        "SQL Injection",
        "medium",
        "source"
    ],
    "$_POST": [
        "$_POST reference found",
        "",
        "",
        "critical",
        "source"
    ],
    "$_GET": [
        "$_GET reference found",
        "",
        "",
        "critical",
        "source"
    ],
    "$_REQUEST": [
        "$_REQUEST reference found",
        "",
        "",
        "critical",
        "source"
    ],
    "$_COOKIES": [
        "$_COOKIES reference found",
        "",
        "",
        "critical",
        "source"
    ]
}
