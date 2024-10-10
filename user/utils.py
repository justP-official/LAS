from user.models import User


def verify_owner(owner: User, current_user: User) -> bool:
    '''
    Функция для проверки текущего пользователя на права доступа к записи в БД.

    Параметры:
    ----------
    owner - владелец записи в БД.

    current_user - текущий пользователь, которого необходимо проверить.
    '''
    return owner.pk == current_user.pk
