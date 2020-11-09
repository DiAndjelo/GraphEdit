from Figures.Object import Object


class Combiner:
    @staticmethod
    def combine(figures, obj=None):
        if obj is None:
            obj = Object()
        for e in figures:
            obj.add_figure(e)
        return obj