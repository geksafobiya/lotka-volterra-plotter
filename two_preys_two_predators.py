import numpy as np
np.seterr(all='raise')

class GrowthCalculator(object):
    def __init__(self):
        # Lotka-Volterra equation coefficients
        #для травоядных
        self.b1 = 1.0 #рождаемость
        self.a11 = 0.1 #смерть от старости
        self.a12 = 0.1 #смерть от хищников

        #для хищников
        self.b2 = 1.0 #смерть хищников без травоядных
        self.a21 = 0.075 #репродукция хищников за каждого съеденного
        self.a22 = 0.5 #смертность от старости

        #для суперхищников
        self.b3 = 1.0  #смерть суперхищников без травоядных и хищников
        self.a31 = 0.075  # репродукция суперхищников за каждого съеденного травоядного
        self.a32 = 0.5  # репродукция суперхищников за каждого съеденного хищника

        self.b4 = 1.0  #смерть суперхищников без травоядных и хищников
        self.a41 = 0.075  # репродукция суперхищников за каждого съеденного травоядного
        self.a42 = 0.5  # репродукция суперхищников за каждого съеденного хищника

        # Other parameters
        self.dt = 0.02
        self.iterations = 1000
        self.predators1 = 5
        self.predators2 = 5
        self.prey1 = 10
        self.prey2 = 10

    def dx1(self, x1, x2, y1, y2):
        """
        Рассчитывает изменение размера популяции жертвы 2 с помощью уравнения Лотки-Вольтерры
        для добычи
        """

        # Рассчитать скорость изменения численности травоядных
        dx1_dt = x1 * (self.b1 - self.a11*y1 - self.a12*y2)
        return dx1_dt

    def dx2(self, x1, x2, y1, y2):
        """
        Рассчитывает изменение размера популяции жертвы 1  с помощью уравнения Лотки-Вольтерры
        для добычи
        """

        # Рассчитать скорость изменения численности травоядных
        dx2_dt = x2 * (self.b2 - self.a21*y1 - self.a22*y2)
        return dx2_dt

    def dy1(self, x1, x2, y1, y2):
        """
        Рассчитывает изменение размера популяции хищников 2 с помощью
        Уравнения Лотки-Вольтерра для хищников
        """

        # Calculate the rate of population change
        dy1_dt = y1 * (-self.b3 + self.a31*x1 + self.a32*x2)

        # Calculate the predator population change
        return dy1_dt

    def dy2(self, x1, x2, y1, y2):
        """
        Рассчитывает изменение размера популяции хищников 1 с помощью
        Уравнения Лотки-Вольтерра для хищников
        """

        # Calculate the rate of population change
        dy2_dt = y2 * (-self.b4 + self.a41*x1 + self.a42*x2)

        # Calculate the predator population change
        return dy2_dt

    def calculate(self):
        import json
        """
        Рассчитывает прирост популяции хищников / жертв / суперхищников для заданных параметров.
        (Определено в строке документации __init__). Возвращает следующий словарь:

        {'predator': [predator population history as a list],
         'prey': [prey population history as a list],
         'superpredator: [superpredator population history as a list]'}
        """
        prey1_history = []
        predator1_history = []
        prey2_history = []
        predator2_history = []

        y0 = np.array([self.prey1, self.predators1, self.prey2, self.predators2], dtype='double')
        tspan = np.array([0.0, self.dt * self.iterations], dtype='double')

        try:
            t, y = self.rk4(self.derivetives, tspan, y0, self.iterations)
            prey1_history = y[:, 0]
            predator1_history = y[:, 1]
            prey2_history = y[:, 2]
            predator2_history = y[:, 3]

            # print('t = ', t)
            # print(predator_history)
            # res = [dict([(ti, yi)]) for ti, yi in zip(t, prey2_history)]
            # print(json.dumps(res, indent=2))
        except (RuntimeError, OverflowError, FloatingPointError) as ex:
            print("Error", ex)

        return {
            'prey1': prey1_history,
            'prey2': prey2_history,
            'predator1': predator1_history,
            'predator2': predator2_history
        }

    def derivetives(self, t, rf):

        x1 = rf[0]
        y1 = rf[1]
        x2 = rf[2]
        y2 = rf[3]

        dx1dt = self.dx1(x1, x2, y1, y2)
        dy1dt = self.dy1(x1, x2, y1, y2)
        dx2dt = self.dx2(x1, x2, y1, y2)
        dy2dt = self.dy2(x1, x2, y1, y2)
        drfdt = np.array([dx1dt, dy1dt, dx2dt, dy2dt], dtype='double')
        return drfdt


    def rk4(self, dydt, tspan, y0, n):
        # RK4 approximates the solution to an ODE using the RK4 method.
        #  Input:
        #    function dydt: points to a function that evaluates the right
        #                   hand side of the ODE.
        #    real tspan[2]: contains the initial and final times.
        #    real y0[m]: an array containing the initial condition.
        #    integer n: the number of steps to take.

        #  Output:
        #    real t[n+1], y[n+1,m]: the times and solution values.
        #

        if np.ndim(y0) == 0:
            m = 1
        else:
            m = len(y0)

        tfirst = tspan[0]
        tlast = tspan[1]
        dt = (tlast - tfirst) / n
        t = np.zeros(n + 1)
        y = np.zeros([n + 1, m])
        y[0, :] = y0

        for i in range(0, n):
            f1 = dydt(t[i], y[i, :])
            f2 = dydt(t[i] + dt / 2.0, y[i, :] + dt * f1 / 2.0)
            f3 = dydt(t[i] + dt / 2.0, y[i, :] + dt * f2 / 2.0)
            f4 = dydt(t[i] + dt, y[i, :] + dt * f3)

            t[i + 1] = t[i] + dt
            y[i + 1, :] = y[i, :] + dt * (f1 + 2.0 * f2 + 2.0 * f3 + f4) / 6.0

        return t, y
