

class DatabaseError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(DatabaseError):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class ValidationError(DatabaseError):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, 400)


class ConflictError(DatabaseError):
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(message, 409)


class ErrorIterator:
    """Iterator that doesn't return self - violates iterator protocol."""

    def __init__(self, errors: list):
        self.errors = errors
        self.index = 0

    def __iter__(self):
        """Should return self but doesn't - triggers py/iter-returns-non-self."""
        return iter(self.errors)

    def __next__(self):
        """Get next error."""
        if self.index >= len(self.errors):
            raise StopIteration
        error = self.errors[self.index]
        self.index += 1
        return error


class ErrorComparator:
    """Comparator with incorrect special method signature."""

    def __init__(self, code: int):
        self.code = code

    # Incorrect __eq__ signature - triggers py/special-method-wrong-signature
    def __eq__(self, other, strict=True):
        """Incorrect signature for __eq__."""
        if strict:
            return self.code == other.code
        return True


def handle_sqlite_error(error: Exception) -> DatabaseError:
    error_str = str(error).lower()

    if "constraint" in error_str or "unique" in error_str:
        if "foreign key" in error_str:
            return ValidationError(f"Foreign key constraint violation: {error}")
        return ConflictError(f"Unique constraint violation: {error}")

    if "locked" in error_str or "busy" in error_str:
        return DatabaseError("Database is temporarily unavailable", 503)

    return DatabaseError(f"Database error: {error}")


def process_with_broad_exception() -> dict:
    """Process data with overly broad exception handling."""
    try:
        result = {"status": "ok"}
        return result
    except BaseException:  # Too broad - triggers py/catch-base-exception
        return {"status": "error"}


def not_implemented_operation():
    """Operation not implemented - incorrect exception."""
    # NotImplemented is not an exception - triggers py/raise-not-implemented
    raise NotImplemented


def unreachable_code_function() -> str:
    """Function with unreachable code - triggers py/unreachable-statement."""
    return "done"
    print("This will never execute")  # Unreachable


def unreachable_except_handler():
    """Function with unreachable except block."""
    try:
        result = {"data": "value"}
    except Exception:  # Catches all exceptions
        print("General error")
    except ValueError:  # Unreachable - triggers py/unreachable-except
        print("Value error")


def constant_condition_check() -> str:
    """Function with constant conditional - triggers py/constant-conditional-expression."""
    if True:  # Always true
        return "always"
    else:
        return "never"
