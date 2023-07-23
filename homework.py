

class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories
                 ) -> None:
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
        self.training_type = training_type

    def get_message(self):
        """Функция получения сообщения:
        функция вызывается, как метод к переменной info,
        чтобы вывести данное сообщение с указанием лишь трех
        знаков после запятой"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""

    training_type = None
    LEN_STEP = 0.65
    M_IN_KM = 1000  # Константа для перевода метров в киллометры.
    CONVERT_HOURS_TO_MINUTES = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / (self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.training_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.training_type = 'Running'

    def get_spent_calories(self):
        """Спецификация функции базового класса
        для получения количества затраченных калорий на тренировку
        'Running'."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * super().get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * (self.duration * self.CONVERT_HOURS_TO_MINUTES))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WEIGHT_MULTIPLIER_1 = 0.035
    WEIGHT_MULTIPLIER_2 = 0.029
    TRANSFER_KMH_TO_MS = 0.278  # Перевод км/ч в м/с.
    TRANSGER_M_TO_S = 100  # Константа для перевода сантиметров в метры.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.training_type = 'SportsWalking'

    def get_spent_calories(self):
        """Спецификация функции базового класса
        для получения количества затраченных калорий на тренировку
        'Sports Walking'."""
        return ((self.WEIGHT_MULTIPLIER_1 * self.weight
                 + ((super().get_mean_speed() * self.TRANSFER_KMH_TO_MS)**2
                    / (self.height / self.TRANSGER_M_TO_S))
                 * self.WEIGHT_MULTIPLIER_2 * self.weight)
                * (self.duration * self.CONVERT_HOURS_TO_MINUTES))


class Swimming(Training):
    """Тренировка: плавание."""

    AVERAGE_SPEED_SHIFT = 1.1
    SPEED_MULTIPLIER = 2
    LEN_STEP = 1.38  # Изменение константы базового класса - длинна шага.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.training_type = 'Swimming'

    def get_mean_speed(self) -> float:
        """Спецификация функции базового класса
        для получения скорости при тренировке
        'Swimming'."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / (self.duration))

    def get_spent_calories(self):
        """Спецификация функции базового класса
        для получения количества затраченных калорий на тренировку
        'Swimming'."""
        return ((self.get_mean_speed() + self.AVERAGE_SPEED_SHIFT)
                * self.SPEED_MULTIPLIER
                * self.weight * (self.duration))


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_of_trainings = {'SWM': Swimming,
                         'RUN': Running,
                         'WLK': SportsWalking
                         }
    return dict_of_trainings[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
