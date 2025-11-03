import os


def get_abs_path(*args):
    """
    Строит абсолютный путь к файлу относительно текущего скрипта.
    Можно передать любое количество частей пути.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(base_dir, *args))


if __name__ == '__main__':
    print(get_abs_path())
