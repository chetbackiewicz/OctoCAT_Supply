import re
from typing import Any


def camel_to_snake(name: str) -> str:
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def snake_to_camel(name: str) -> str:
    components = name.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def dict_keys_to_snake(data: dict[str, Any]) -> dict[str, Any]:
    return {camel_to_snake(k): v for k, v in data.items()}


def dict_keys_to_camel(data: dict[str, Any]) -> dict[str, Any]:
    return {snake_to_camel(k): v for k, v in data.items()}


def generate_placeholders(count: int) -> str:
    return ", ".join(["?" for _ in range(count)])


def build_insert_sql(table: str, data: dict[str, Any]) -> tuple[str, list[Any]]:
    snake_data = dict_keys_to_snake(data)
    columns = list(snake_data.keys())
    values = list(snake_data.values())

    columns_str = ", ".join(columns)
    placeholders = generate_placeholders(len(columns))

    sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
    return sql, values


def build_update_sql(table: str, data: dict[str, Any], id_column: str) -> tuple[str, list[Any]]:
    snake_data = dict_keys_to_snake(data)

    id_value = snake_data.pop(id_column)

    set_clauses = [f"{col} = ?" for col in snake_data.keys()]
    values = list(snake_data.values())
    values.append(id_value)

    sql = f"UPDATE {table} SET {', '.join(set_clauses)} WHERE {id_column} = ?"
    return sql, values


def validate_fields(data: dict[str, Any], required_fields: list[str]) -> None:
    missing = [field for field in required_fields if field not in data or data[field] is None]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")


def check_data_validity(data: dict[str, Any]) -> bool:
    """Check data validity with code quality issues."""
    # Testing equality to None - triggers py/test-equals-none
    if data == None:
        return False

    # Asserts tuple - triggers py/asserts-tuple
    assert data, "data must exist"

    # Redundant comparison - triggers py/redundant-comparison
    if len(data) > 0 and len(data) > -1:
        return True

    # Comparison of identical expressions - triggers py/comparison-of-identical-expressions
    if data == data:
        return True

    return False


def format_error_message(entity: str, entity_id: int, action: str) -> str:
    """Format error message with format string issues."""
    # Wrong number of arguments - triggers py/percent-format/wrong-arguments
    msg1 = "Entity: %s, ID: %d, Action: %s" % (entity, entity_id)

    # Surplus argument in format - triggers py/str-format/surplus-argument
    msg2 = "{0} failed".format(action, entity, entity_id)

    return msg1 or msg2


def nested_loop_processor(matrix: list[list[int]]) -> list[int]:
    """Process matrix with nested loop variable reuse."""
    result = []

    # Nested loops with same variable - triggers py/nested-loops-with-same-variable
    for i in range(len(matrix)):
        for i in range(len(matrix[i])):
            result.append(matrix[i])

    return result


# Unused global variable - triggers py/unused-global-variable
UNUSED_SQL_TEMPLATE = "SELECT * FROM table WHERE id = ?"


def redundant_assignment_example(value: int) -> int:
    """Function with redundant assignment."""
    result = value
    # Redundant assignment - triggers py/redundant-assignment
    result = result
    return result
