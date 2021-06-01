import numpy as np
np.seterr(all='raise')

class GrowthCalculator(object):
    def __init__(self):
        # Lotka-Volterra equation coefficients
        #для травоядных
        self.b1 = 1.0 #рождаемость
        self.a11 = 0.1 #смерть от старости
        self.a12 = 0.1 #смерть от хищников
        self.a13 = 0.1  # смерть от хищников
        #для хищников
        self.b2 = 1.0 #смерть хищников без травоядных
        self.a21 = 0.075 #репродукция хищников за каждого съеденного
        self.a22 = 0.5 #смертность от старости
        self.a31 = 0.5  # смертность от старости
        #для суперхищников
        self.b3 = 1.0  #смерть суперхищников без травоядных и хищников
        self.b4 = 1.0  #смерть суперхищников без травоядных и хищников

        # Other parameters
        self.dt = 0.02
        self.iterations = 1000
        self.predators = 5
        self.prey3 = 5
        self.prey1 = 10
        self.prey2 = 10

    def dx1(self, x1, x2, x3, y):
        """
        Рассчитывает изменение размера популяции жертвы 2 с помощью уравнения Лотки-Вольтерры
        для добычи
        """

        # Рассчитать скорость изменения численности травоядных
        dx1_dt = x1 * (self.b1 - self.a11*y)
        return dx1_dt

    def dx2(self, x1, x2, x3, y):
        """
        Рассчитывает изменение размера популяции жертвы 1  с помощью уравнения Лотки-Вольтерры
        для добычи
        """

        # Рассчитать скорость изменения численности травоядных
        dx2_dt = x2 * (self.b2 - self.a12*y)
        return dx2_dt

    def dx3(self, x1, x2, x3, y):
        """
        Рассчитывает изменение размера популяции хищников 1 с помощью
        Уравнения Лотки-Вольтерра для хищников
        """

        # Calculate the rate of population change
        dx3_dt = x3 * (self.b3 - self.a13*y)

        # Calculate the predator population change
        return dx3_dt

    def dy(self, x1, x2, x3, y):
        """
        Рассчитывает изменение размера популяции хищников 2 с помощью
        Уравнения Лотки-Вольтерра для хищников
        """

        # Calculate the rate of population change
        dy_dt = y * (-self.b4 + self.a21*x1 + self.a22*x2 + self.a23*x3)

        # Calculate the predator population change
        return dy_dt

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
        prey3_history = []
        prey2_history = []
        predator_history = []

        y0 = np.array([self.prey1, self.prey2, self.prey3, self.predators], dtype='double')
        tspan = np.array([0.0, self.dt * self.iterations], dtype='double')

        try:
            t, y = self.rk4(self.derivetives, tspan, y0, self.iterations)
            prey1_history = y[:, 0]
            prey2_history = y[:, 1]
            prey3_history = y[:, 2]
            predator_history = y[:, 3]

            # print('t = ', t)
            # print(predator_history)
            # res = [dict([(ti, yi)]) for ti, yi in zip(t, prey2_history)]
            # print(json.dumps(res, indent=2))
        except (RuntimeError, OverflowError, FloatingPointError) as ex:
            print("Error", ex)

        return {
            'prey1': prey1_history,
            'prey2': prey2_history,
            'prey3': prey3_history,
            'predator': predator_history
        }

    def derivetives(self, t, rf):

        x1 = rf[0]
        x2 = rf[1]
        x3 = rf[2]
        y = rf[3]

        dx1dt = self.dx1(x1, x2, x3, y)
        dx2dt = self.dx2(x1, x2, x3, y)
        dx3dt = self.dx3(x1, x2, x3, y)
        dydt = self.dy(x1, x2, x3, y)
        drfdt = np.array([dx1dt, dx2dt, dx3dt, dydt], dtype='double')
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
