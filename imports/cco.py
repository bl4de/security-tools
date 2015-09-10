# Color Console Output module


class _PefOutput:
    def __init__(self):
        pass

    Black = '\33[30m'
    Red = '\33[31m'
    Green = '\33[32m'
    Yellow = '\33[33m'
    Blue = '\33[34m'
    Magenta = '\33[35m'
    Cyan = '\33[36m'
    White = '\33[37m'
    _endline = '\33[0m'

    efMsgFound = "exploitable function call"
    efMsgGlobalFound = "global variable explicit call"
    fiMsgFound = "file include pattern found; potential LFI/RFI detected"
