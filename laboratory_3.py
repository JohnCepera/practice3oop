from typing import Union, Any, Iterator

class Point3d:
    """Класс, представляющий точку в трехмерном пространстве."""
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x: float = float(x)
        self.y: float = float(y)
        self.z: float = float(z)

    def __str__(self) -> str:
        return f"Point3d({round(self.x, 2)}, {round(self.y, 2)}, {round(self.z, 2)})"

    def __repr__(self) -> str:
        return f"Point3d(x={round(self.x, 2)}, y={round(self.y, 2)}, z={round(self.z, 2)})"


class Vector3d:
    """Класс, представляющий вектор в трехмерном пространстве."""
    def __init__(self, x: float, y: float, z: float) -> None:
        self._x: float = float(x)
        self._y: float = float(y)
        self._z: float = float(z)

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = float(value)

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = float(value)

    @property
    def z(self) -> float:
        return self._z

    @z.setter
    def z(self, value: float) -> None:
        self._z = float(value)

    def __str__(self) -> str:
        return f"({round(self.x, 2)}, {round(self.y, 2)}, {round(self.z, 2)})"

    def __repr__(self) -> str:
        return f"Vector3d(x={round(self.x, 2)}, y={round(self.y, 2)}, z={round(self.z, 2)})"

    @classmethod
    def from_points(cls, start: Point3d, end: Point3d) -> 'Vector3d':
        """Фабричный метод создания вектора из двух точек (начала и конца)."""
        return cls(end.x - start.x, end.y - start.y, end.z - start.z)

    def magnitude(self) -> float:
        """Вычисление точной длины вектора."""
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def __len__(self) -> int:
        """
        Магический метод взятия длины. 
        В Python __len__ обязан возвращать целое число (int), 
        поэтому возвращается округленная длина. Пользуйтесь .magnitude() для точного значения.
        """
        return int(round(self.magnitude()))

    # Операции сравнения по длине вектора (и покомпонентно для равенства)
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Vector3d):
            return False
        return abs(self.x - other.x) < 1e-9 and abs(self.y - other.y) < 1e-9 and abs(self.z - other.z) < 1e-9

    def __lt__(self, other: 'Vector3d') -> bool:
        if not isinstance(other, Vector3d):
            return NotImplemented
        return self.magnitude() < other.magnitude()

    def __gt__(self, other: 'Vector3d') -> bool:
        if not isinstance(other, Vector3d):
            return NotImplemented
        return self.magnitude() > other.magnitude()

    # Вспомогательный метод для приведения типов (число в вектор)
    def _to_vector(self, other: Union['Vector3d', int, float]) -> 'Vector3d':
        if isinstance(other, Vector3d):
            return other
        elif isinstance(other, (int, float)):
            return Vector3d(other, other, other)
        return NotImplemented

    # Арифметические операции (+, -, *, /)
    def __add__(self, other: Union['Vector3d', int, float]) -> 'Vector3d':
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        return Vector3d(self.x + v.x, self.y + v.y, self.z + v.z)

    def __radd__(self, other: Union['Vector3d', int, float]) -> 'Vector3d':
        return self.__add__(other)

    def __sub__(self, other: Union['Vector3d', int, float]) -> 'Vector3d':
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        return Vector3d(self.x - v.x, self.y - v.y, self.z - v.z)

    def __rsub__(self, other: Union['Vector3d', int, float]) -> 'Vector3d':
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        return Vector3d(v.x - self.x, v.y - self.y, v.z - self.z)

    def __mul__(self, other: Union['Vector3d', int, float]) -> 'Vector3d':
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        return Vector3d(self.x * v.x, self.y * v.y, self.z * v.z)

    def __rmul__(self, other: Union['Vector3d', int, float]) -> 'Vector3d':
        return self.__mul__(other)

    def __truediv__(self, other: Union['Vector3d', int, float]) -> 'Vector3d':
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        if v.x == 0 or v.y == 0 or v.z == 0:
            raise ZeroDivisionError("Деление на ноль компоненты вектора.")
        return Vector3d(self.x / v.x, self.y / v.y, self.z / v.z)

    def __rtruediv__(self, other: Union['Vector3d', int, float]) -> 'Vector3d':
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        if self.x == 0 or self.y == 0 or self.z == 0:
            raise ZeroDivisionError("Деление на ноль компоненты вектора.")
        return Vector3d(v.x / self.x, v.y / self.y, v.z / self.z)

    # Инкрементальные операции (+=, -=, *=, /=) без создания нового объекта
    def __iadd__(self, other: Union['Vector3d', int, float]) -> 'Vector3d':
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        self.x += v.x
        self.y += v.y
        self.z += v.z
        return self

    def __isub__(self, other: Union['Vector3d', int, float]) -> 'Vector3d':
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        self.x -= v.x
        self.y -= v.y
        self.z -= v.z
        return self

    def __imul__(self, other: Union['Vector3d', int, float]) -> 'Vector3d':
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        self.x *= v.x
        self.y *= v.y
        self.z *= v.z
        return self

    def __itruediv__(self, other: Union['Vector3d', int, float]) -> 'Vector3d':
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        if v.x == 0 or v.y == 0 or v.z == 0:
            raise ZeroDivisionError("Деление на ноль компоненты вектора.")
        self.x /= v.x
        self.y /= v.y
        self.z /= v.z
        return self

    # Векторное произведение (@)
    def __matmul__(self, other: 'Vector3d') -> 'Vector3d':
        if not isinstance(other, Vector3d):
            return NotImplemented
        cx = self.y * other.z - self.z * other.y
        cy = self.z * other.x - self.x * other.z
        cz = self.x * other.y - self.y * other.x
        return Vector3d(cx, cy, cz)

    # Статические методы для проверки коллинеарности и компланарности
    @staticmethod
    def is_collinear(a: 'Vector3d', b: 'Vector3d') -> bool:
        """Проверка векторов на коллинеарность через векторное произведение (должно быть равно нулю)."""
        cross = a @ b
        return abs(cross.x) < 1e-9 and abs(cross.y) < 1e-9 and abs(cross.z) < 1e-9

    @staticmethod
    def is_complanar(a: 'Vector3d', b: 'Vector3d', c: 'Vector3d') -> bool:
        """Проверка векторов на компланарность через смешанное произведение (должно быть равно нулю)."""
        # Смешанное произведение: a * (b x c) -> скалярное произведение a и (b @ c)
        cross_bc = b @ c
        mixed_prod = a.x * cross_bc.x + a.y * cross_bc.y + a.z * cross_bc.z
        return abs(mixed_prod) < 1e-9

    # Доступ по индексу и имени компоненты
    def __getitem__(self, item: Union[int, str]) -> float:
        if item == 0 or item == 'x':
            return self.x
        elif item == 1 or item == 'y':
            return self.y
        elif item == 2 or item == 'z':
            return self.z
        else:
            raise KeyError("Индекс должен быть 0, 1, 2 или 'x', 'y', 'z'")

    # Перебор по компонентам (for)
    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y
        yield self.z


# Демонстрация работы программы
if __name__ == "__main__":
    print("--- Демонстрация лабораторной работы ---")
    
    # 1. Создание точек и инициализация вектора
    p_start = Point3d(1, 2, 3)
    p_end = Point3d(4, 6, 8)
    print(f"Точка начала: {p_start}, Точка конца: {p_end}")
    
    # 2. Фабричный метод from_points
    v1 = Vector3d.from_points(p_start, p_end)
    print(f"Вектор v1 из точек (from_points): {v1.__repr__()}")
    
    # 3. Проверка магических методов __str__ и __repr__
    v2 = Vector3d(3.1415, 4.567, 5.0)
    print(f"Магический метод __str__ для v2: {v2}")
    print(f"Магический метод __repr__ для v2: {v2.__repr__()}")
    
    # 4. Операции сравнения (==, >, <) по длине
    v3 = Vector3d(3, 4, 5)
    v4 = Vector3d(3, 4, 5)
    v5 = Vector3d(1, 1, 1)
    print(f"v3 == v4: {v3 == v4}")
    print(f"v3 > v5: {v3 > v5}")
    print(f"v5 < v3: {v5 < v3}")
    
    # 5. Арифметические операции с векторами и числами (слева и справа)
    a = Vector3d(3, 4, 5)
    print(f"Исходный вектор a: {a}")
    print(f"a + 3: {a + 3}")
    print(f"3 + a: {3 + a}")
    print(f"a - 1: {a - 1}")
    print(f"a * 2: {a * 2}")
    print(f"a / 2: {a / 2}")
    
    # 6. Инкрементальные операции (+=, -=, *=, /=) без создания нового объекта
    print(f"id(a) до операций: {id(a)}")
    a += 2
    print(f"a после 'a += 2': {a}, id(a): {id(a)}")
    a *= 2
    print(f"a после 'a *= 2': {a}, id(a): {id(a)}")
    
    # 7. Векторное произведение (@)
    v_a = Vector3d(1, 0, 0)
    v_b = Vector3d(0, 1, 0)
    print(f"Векторное произведение {v_a} @ {v_b} = {v_a @ v_b}")
    
    # 8. Проверка на коллинеарность и компланарность
    v_c = Vector3d(2, 0, 0)
    v_d = Vector3d(0, 0, 1)
    print(f"Коллинеарны ли {v_a} и {v_c}? {Vector3d.is_collinear(v_a, v_c)}")
    print(f"Коллинеарны ли {v_a} и {v_b}? {Vector3d.is_collinear(v_a, v_b)}")
    print(f"Компланарны ли {v_a}, {v_b}, {v_d}? {Vector3d.is_complanar(v_a, v_b, v_d}")
    
    # 9. Длина вектора (__len__)
    print(f"Длина вектора {v3} (округленная до целого): {len(v3)}, точная: {v3.magnitude():.2f}")
    
    # 10. Обращение по индексу и имени компоненты
    print(f"v3[0]: {v3[0]}, v3['y']: {v3['y']}, v3['z']: {v3['z']}")






#---------------------------------------------------------------------------------------------------------------
    import math

class Point3d:
    """Класс, представляющий точку в трехмерном пространстве."""
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        return "Point3d(" + str(round(self.x, 2)) + ", " + str(round(self.y, 2)) + ", " + str(round(self.z, 2)) + ")"

    def __repr__(self):
        return "Point3d(x=" + str(round(self.x, 2)) + ", y=" + str(round(self.y, 2)) + ", z=" + str(round(self.z, 2)) + ")"


class Vector3d:
    """Класс, представляющий вектор в трехмерном пространстве."""
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        return "(" + str(round(self.x, 2)) + ", " + str(round(self.y, 2)) + ", " + str(round(self.z, 2)) + ")"

    def __repr__(self):
        return "Vector3d(x=" + str(round(self.x, 2)) + ", y=" + str(round(self.y, 2)) + ", z=" + str(round(self.z, 2)) + ")"

    @classmethod
    def from_points(cls, start, end):
        """Фабричный метод создания вектора из двух точек."""
        return cls(end.x - start.x, end.y - start.y, end.z - start.z)

    def magnitude(self):
        """Вычисление точной математической длины вектора."""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __len__(self):
        """
        Магический метод взятия длины. 
        Возвращает округленную длину, так как __len__ обязан возвращать int.
        """
        return int(round(self.magnitude()))

    # Операции сравнения
    def __eq__(self, other):
        if not isinstance(other, Vector3d):
            return False
        return abs(self.x - other.x) < 1e-9 and abs(self.y - other.y) < 1e-9 and abs(self.z - other.z) < 1e-9

    def __lt__(self, other):
        if not isinstance(other, Vector3d):
            return NotImplemented
        return self.magnitude() < other.magnitude()

    def __gt__(self, other):
        if not isinstance(other, Vector3d):
            return NotImplemented
        return self.magnitude() > other.magnitude()

    # Вспомогательный метод преобразования чисел в квази-вектор для удобства расчетов
    def _to_vector(self, other):
        if isinstance(other, Vector3d):
            return other
        elif isinstance(other, (int, float)):
            return Vector3d(other, other, other)
        return NotImplemented

    # Арифметические операции (+, -, *, /)
    def __add__(self, other):
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        return Vector3d(self.x + v.x, self.y + v.y, self.z + v.z)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        return Vector3d(self.x - v.x, self.y - v.y, self.z - v.z)

    def __rsub__(self, other):
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        return Vector3d(v.x - self.x, v.y - self.y, v.z - self.z)

    def __mul__(self, other):
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        return Vector3d(self.x * v.x, self.y * v.y, self.z * v.z)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        if v.x == 0 or v.y == 0 or v.z == 0:
            raise ZeroDivisionError("Деление на ноль компоненты вектора.")
        return Vector3d(self.x / v.x, self.y / v.y, self.z / v.z)

    def __rtruediv__(self, other):
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        if self.x == 0 or self.y == 0 or self.z == 0:
            raise ZeroDivisionError("Деление на ноль компоненты вектора.")
        return Vector3d(v.x / self.x, v.y / self.y, v.z / self.z)

    # Инкрементальные арифметические операции (+=, -=, *=, /=)
    def __iadd__(self, other):
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        self.x += v.x
        self.y += v.y
        self.z += v.z
        return self

    def __isub__(self, other):
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        self.x -= v.x
        self.y -= v.y
        self.z -= v.z
        return self

    def __imul__(self, other):
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        self.x *= v.x
        self.y *= v.y
        self.z *= v.z
        return self

    def __itruediv__(self, other):
        v = self._to_vector(other)
        if v is NotImplemented: return NotImplemented
        if v.x == 0 or v.y == 0 or v.z == 0:
            raise ZeroDivisionError("Деление на ноль компоненты вектора.")
        self.x /= v.x
        self.y /= v.y
        self.z /= v.z
        return self

    # Векторное произведение (@)
    def __matmul__(self, other):
        if not isinstance(other, Vector3d):
            return NotImplemented
        cx = self.y * other.z - self.z * other.y
        cy = self.z * other.x - self.x * other.z
        cz = self.x * other.y - self.y * other.x
        return Vector3d(cx, cy, cz)

    # Геометрические проверки (статические методы)
    @staticmethod
    def is_collinear(a, b):
        cross = a @ b
        return abs(cross.x) < 1e-9 and abs(cross.y) < 1e-9 and abs(cross.z) < 1e-9

    @staticmethod
    def is_complanar(a, b, c):
        cross_bc = b @ c
        mixed_prod = a.x * cross_bc.x + a.y * cross_bc.y + a.z * cross_bc.z
        return abs(mixed_prod) < 1e-9

    # Доступ по индексу и названию
    def __getitem__(self, item):
        if item == 0 or item == 'x':
            return self.x
        elif item == 1 or item == 'y':
            return self.y
        elif item == 2 or item == 'z':
            return self.z
        else:
            raise KeyError("Индекс должен быть 0, 1, 2 или 'x', 'y', 'z'")

    # Поддержка цикла for
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z


# =====================================================================
# ДЕМОНСТРАЦИЯ РАБОТЫ ВСЕХ ПУНКТОВ ЗАДАНИЯ
# =====================================================================
if __name__ == "__main__":
    print("--- 1. Создание векторов и магические методы __str__ и __repr__ ---")
    v1 = Vector3d(3.14159, 4.2345, 5.6789)
    print("Вывод __str__ :", str(v1))
    print("Вывод __repr__:", repr(v1))
    print()

    print("--- 2. Фабричный метод from_points ---")
    p_start = Point3d(1, 1, 1)
    p_end = Point3d(4, 5, 6)
    v_from_p = Vector3d.from_points(p_start, p_end)
    print("Вектор из точек", p_start, "и", p_end, "равен:", v_from_p)
    print()

    print("--- 3. Операции сравнения (==, >, <) ---")
    va = Vector3d(1, 2, 3)
    vb = Vector3d(1, 2, 3)
    vc = Vector3d(4, 5, 6)
    print("va == vb:", va == vb)
    print("va < vc :", va < vc)
    print("vc > va :", vc > va)
    print()

    print("--- 4. Арифметические операции (+, -, *, /) с векторами и числами ---")
    a = Vector3d(3, 4, 5)
    print("Исходный вектор a:", a)
    print("a + 3 :", a + 3)
    print("3 + a :", 3 + a)
    print("a - 1 :", a - 1)
    print("10 - a:", 10 - a)
    print("a * 2 :", a * 2)
    print("a / 2 :", a / 2)
    print()

    print("--- 5. Инкрементальные операции (+=, -=, *=, /=) без создания нового объекта ---")
    v_inc = Vector3d(1, 2, 3)
    old_id = id(v_inc)
    print("Вектор до += :", v_inc, f"(ID: {old_id})")
    v_inc += 2
    new_id = id(v_inc)
    print("Вектор после +=:", v_inc, f"(ID: {new_id})")
    print("ID совпадает?", old_id == new_id)
    print()

    print("--- 6. Векторное произведение (@) ---")
    v_x = Vector3d(1, 0, 0)
    v_y = Vector3d(0, 1, 0)
    v_z = v_x @ v_y
    print(f"Векторное произведение {v_x} @ {v_y} = {v_z}")
    print()

    print("--- 7. Проверка на коллинеарность и компланарность ---")
    vec1 = Vector3d(1, 2, 3)
    vec2 = Vector3d(2, 4, 6)  # Коллинеарен vec1
    vec3 = Vector3d(1, 0, 1)
    print("vec1 и vec2 коллинеарны?", Vector3d.is_collinear(vec1, vec2))
    print("vec1 и vec3 коллинеарны?", Vector3d.is_collinear(vec1, vec3))
    
    # Компланарность (три вектора в одной плоскости)
    v_comp1 = Vector3d(1, 0, 0)
    v_comp2 = Vector3d(0, 1, 0)
    v_comp3 = Vector3d(1, 1, 0) # Лежит в той же плоскости XY
    print("v_comp1, v_comp2, v_comp3 компланарны?", Vector3d.is_complanar(v_comp1, v_comp2, v_comp3))
    print()

    print("--- 8. Взятие длины вектора через len() ---")
    v_len = Vector3d(3, 4, 0) # Точная длина = 5
    print("Точная длина через .magnitude():", v_len.magnitude())
    print("Округленная длина через len()   :", len(v_len))
    print()

    print("--- 9. Обращение по индексу и имени компоненты ---")
    v_idx = Vector3d(10.5, 20.7, 30.9)
    print("vector[0]   :", v_idx[0])
    print("vector['y'] :", v_idx['y'])
    print()

    print("--- 10. Перебор по компонентам вектора (цикл for) ---")
    v_for = Vector3d(7, 8, 9)
    print("Компоненты вектора в цикле:")
    for component in v_for:
        print("->", component)

    # 11. Перебор по компонентам при помощи for
    print("Перебор компонент v3 в цикле for:")
    for comp in v3:
        print(f"  Компонента: {comp}")
