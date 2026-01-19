class DBException(Exception):
    """Excepción personalizada para errores relacionados con la base de datos."""

    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)

    def __str__(self):
        if self.original_error:
            return f"{self.message} | Error original: {self.original_error}"
        return self.message

