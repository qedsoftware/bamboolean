class BambooleanError(Exception):
    pass


class BambooleanLexerError(BambooleanError):
    pass


class BambooleanParserError(BambooleanError):
    pass


class NoSuchVisitorException(BambooleanError):
    pass
