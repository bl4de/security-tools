# Reference(S) for pef.py

# doc dipslayed:
# 1st element - description
# 2nd element - syntax
# 3rd element - possible vulnerability classes
exploitableFunctionsDesc = {
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
    "system()": [
        "Allows to execute system command passed as an argument",
        "system ( string $command [, int &$return_var ] ) : string",
        "RCE",
        "high"
    ],
    "fopen()": [
        "Opens file or URL",
        "fopen ( string $filename , string $mode [, bool $use_include_path = FALSE [, resource $context ]] ) : resource",
        "Local File Include; Remote File Include",
        "high"
    ]
}
