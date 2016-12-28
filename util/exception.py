# -*- coding: utf-8 -*-


class AsmException(Exception):
    """Base Asm Exception
    """
    message = "An unknown exception occurred."

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs
        if not message:
            try:
                message = self.message % kwargs
            except Exception:
                message = self.message
        self.msg = message
        super(AsmException, self).__init__(message)


class DasmException(Exception):
    """Base Dasm Exception
    """
    message = "An unknown exception occurred."

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs
        if not message:
            try:
                message = self.message % kwargs
            except Exception:
                message = self.message
        self.msg = message
        super(DasmException, self).__init__(message)