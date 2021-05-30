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
        self.a23 = 0.5  # смертность от старости
        #для суперхищников
        self.b3 = 1.0  #смерть суперхищников без травоядных и хищников
        self.b4 = 1.0  #смерть суперхищников без травоядных и хищников

        # Other parameters
        self.dt = 0.02
        self.iterations = 1000
        self.predators1 = 5
        self.predators2 = 5
        self.predators3 = 5
        self.prey = 10


    def dx(self, x, y1, y2, y3):
        """
        Рассчитывает изменение размера популяции жертвы 2 с помощью уравнения Лотки-Вольтерры
        для добычи
        """

        # Рассчитать скорость изменения численности травоядных
        dx_dt = x * (self.b1 - self.a11*y1 - self.a12*y2 - self.a13*y3)
        return dx_dt

    def dy1(self, x, y1, y2, y3):
        """
        Рассчитывает изменение размера популяции хищников 2 с помощью
        Уравнения Лотки-Вольтерра для хищников
        """

        # Calculate the rate of population change
        dy1_dt = y1 * (-self.b2 + self.a21*x)

        # Calculate the predator population change
        return dy1_dt

    def dy2(self, x, y1, y2, y3):
        """
        Рассчитывает изменение размера популяции хищников 1 с помощью
        Уравнения Лотки-Вольтерра для хищников
        """

        # Calculate the rate of population change
        dy2_dt = y2 * (-self.b3 + self.a22*x)

        # Calculate the predator population change
        return dy2_dt

    def dy3(self, x, y1, y2, y3):
        """
        Рассчитывает изменение размера популяции хищников 2 с помощью
        Уравнения Лотки-Вольтерра для хищников
        """

        # Calculate the rate of population change
        dy3_dt = y3 * (-self.b4 + self.a23*x)

        # Calculate the predator population change
        return dy3_dt

    def calculate(self):
        import json
        """
        Рассчитывает прирост популяции хищников / жертв / суперхищников для заданных параметров.
        (Определено в строке документации __init__). Возвращает следующий словарь:

        {'predator': [predator population history as a list],
         'prey': [prey population history as a list],
         'superpredator: [superpredator population history as a list]'}
        """
        prey_history = []
        predator1_history = []
        predator2_history = []
        predator3_history = []

        y0 = np.array([self.prey, self.predators1, self.predators2, self.predators3], dtype='double')
        tspan = np.array([0.0, self.dt * self.iterations], dtype='double')

        try:
            t, y = self.rk4(self.derivetives, tspan, y0, self.iterations)
            prey_history = y[:, 0]
            predator1_history = y[:, 1]
            predator2_history = y[:, 2]
            predator3_history = y[:, 3]

            # print('t = ', t)
            # print(predator_history)
            # res = [dict([(ti, yi)]) for ti, yi in zip(t, prey2_history)]
            # print(json.dumps(res, indent=2))
        except (RuntimeError, OverflowError, FloatingPointError) as ex:
            print("Error", ex)

        return {
            'prey': prey_history,
            'predator1': predator1_history,
            'predator2': predator2_history,
            'predator3': predator3_history
        }

    def derivetives(self, t, rf):

        x = rf[0]
        y1 = rf[1]
        y2 = rf[2]
        y3 = rf[3]

        dxdt = self.dx(x, y1, y2, y3)
        dy1dt = self.dy1(x, y1, y2, y3)
        dy2dt = self.dy2(x, y1, y2, y3)
        dy3dt = self.dy3(x, y1, y2, y3)
        drfdt = np.array([dxdt, dy1dt, dy2dt, dy3dt], dtype='double')
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
