class beautyConsole:
    """This class defines properties and methods to manipulate console output"""
    # Black       0;30     Dark Gray     1;30
    # Blue        0;34     Light Blue    1;34
    # Green       0;32     Light Green   1;32
    # Cyan        0;36     Light Cyan    1;36
    # Red         0;31     Light Red     1;31
    # Purple      0;35     Light Purple  1;35
    # Brown       0;33     Yellow        1;33
    # Light Gray  0;37     White         1;37

    colors = {
        "black": '\33[30m',
        "white": '\33[37m',
        "red": '\33[31m',
        "green": '\33[32m',
        "yellow": '\33[33m',
        "blue": '\33[34m',
        "magenta": '\33[35m',
        "cyan": '\33[36m',
        "grey": '\33[90m',
        "lightgrey": '\33[37m',
        "lightblue": '\33[94'
    }

    characters = {
        "endline": '\33[0m'
    }

    def __init__(self):
        return None

    @staticmethod
    def getColor(color_name):
        """returns color identified by color_name or white as default value"""
        if color_name in beautyConsole.colors:
            return beautyConsole.colors[color_name]
        return beautyConsole.colors["white"]

    @staticmethod
    def getSpecialChar(char_name):
        """returns special character identified by char_name"""
        if char_name in beautyConsole.characters:
            return beautyConsole.characters[char_name]
        return ""

    efMsgFound = "exploitable function call"
    eKeyWordFound = "keyword with possibly critical meaning in code"
    efMsgGlobalFound = "global variable explicit call"
    fiMsgFound = "file include pattern found; potential LFI/RFI detected"
    eReflFound = "reflected property found; check for XSS"
