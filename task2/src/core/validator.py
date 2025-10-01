"""
Набор исключений и простая валидация аргументов + утилита error_proxy.
"""

from typing import Callable, Any
import functools

""" Исключение, возникающее при некорректных аргументах """
class argument_exception(Exception):
    pass


""" Исключение, возникающее при ошибке бизнес-операции """
class operation_exception(Exception):
    pass


"""
Утилита для оборачивания вызовов, перенаправляющая исключения
в operation_exception с возможностью логирования/обработки
"""
class error_proxy:
    @staticmethod
    def wrap(rethrow: Exception = operation_exception) -> Callable:
        """
        Декоратор-обёртка, который перекладывает любые Exception в указанный тип
        Args:
            rethrow: класс исключения, который будет выброшен вместо оригинала
        Returns:
            декоратор
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except argument_exception:
                    raise
                except Exception as ex:
                    raise rethrow(str(ex)) from ex
            return wrapper
        return decorator


"""
Набор статических проверок аргументов. Возвращает True при успешной проверке
или выбрасывает argument_exception при ошибке.
"""
class validator:
    @staticmethod
    def validate(value: Any, expected_type: type, max_length: int = None) -> bool:
        """
        Проверка наличия, типа и максимальной длины строковых представлений
        Args:
            value: проверяемое значение
            expected_type: ожидаемый тип (например str или int)
            max_length: максимальная длина строкового представления (по необходимости)
        Raises:
            argument_exception: при некорректном значении
        """
        if value is None:
            raise argument_exception("Аргумент не должен быть None")

        if not isinstance(value, expected_type):
            raise argument_exception(
                f"Ожидается тип {expected_type.__name__}, получен {type(value).__name__}"
            )

        if isinstance(value, str):
            if len(value.strip()) == 0:
                raise argument_exception("Строковый аргумент не должен быть пустым")
            if max_length is not None and len(value.strip()) > max_length:
                raise argument_exception("Строковый аргумент превышает допустимую длину")

        return True
