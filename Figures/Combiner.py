from Figures.Group import Group


class Combiner:
    """
    Класс объединения объектов
    """
    @staticmethod
    def combine(figures, obj=None):
        if obj is None:
            obj = Group()
        for e in figures:
            obj.add_figure(e)
        return obj
