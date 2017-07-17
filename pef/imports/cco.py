class ConsoleOutputBeautifier:
    """This class defines properties and methods to manipulate console output"""
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
        if color_name in ConsoleOutputBeautifier.colors:
            return ConsoleOutputBeautifier.colors[color_name]
        return ConsoleOutputBeautifier.colors["white"]

    @staticmethod
    def getSpecialChar(char_name):
        """returns special character identified by char_name"""
        if char_name in ConsoleOutputBeautifier.characters:
            return ConsoleOutputBeautifier.characters[char_name]
        return ""


    efMsgFound = "exploitable function call"
    efMsgGlobalFound = "global variable explicit call"
    fiMsgFound = "file include pattern found; potential LFI/RFI detected"
    eReflFound = "reflected property found; check for XSS"
