from src.core.type import Code, ErrorType

EXCEPTION_CODE_MAP: dict[type[Exception], Code] = {
    ValueError: Code.BAD_REQUEST,
    KeyError: Code.NOT_FOUND,
    TypeError: Code.UNPROCESSABLE_ENTITY,
    FileNotFoundError: Code.NOT_FOUND,
    NotImplementedError: Code.NOT_IMPLEMENTED,
}

EXCEPTION_ERROR_TYPE_MAP: dict[type[Exception], ErrorType] = {
    ValueError: ErrorType.INVALID_REQUEST,
    KeyError: ErrorType.DOES_NOT_EXIST,
    TypeError: ErrorType.TYPE_ERROR,
    FileNotFoundError: ErrorType.FILE_NOT_FOUND,
    NotImplementedError: ErrorType.NOT_IMPLEMENTED,
}

