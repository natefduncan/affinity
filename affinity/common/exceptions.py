class TokenMissing(Exception):
    pass

class RequestTypeNotAllowed(Exception):
    pass

class RequestFailed(Exception):
    pass

class RequiredPayloadFieldMissing(Exception):
    pass

class RequiredQueryParamMissing(Exception):
    pass
