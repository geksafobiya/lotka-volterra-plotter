import numpy as np
np.seterr(all='raise')

class GrowthCalculator(object):
    def __init__(self):
        # Lotka-Volterra equation coefficients
        #для травоядных
        self.b1 = 1.0 #рождаемость
     #   self.a11 = 0.1 #смерть от старости
        self.a12 = 0.1 #смерть от хищников
        self.a13 = 0.1 #смерть от суперхищников

        #для хищников
        self.b2 = 1.0 #смерть хищников без травоядных
        self.a21 = 0.075 #репродукция хищников за каждого съеденного
     #   self.a22 = 0.5 #смертность от старости
        self.a23 = 0.3 #смертность от суперхищников

        #для суперхищников
        self.b3 = 1.0  #смерть суперхищников без травоядных и хищников
        self.a31 = 0.075  # репродукция суперхищников за каждого съеденного травоядного
        self.a32 = 0.5  # репродукция суперхищников за каждого съеденного хищника
    #    self.a33 = 0.3 #смерть от старости


        # Other parameters
        self.dt = 0.02
        self.iterations = 1000
        self.predators = 5
        self.superpredators = 4
        self.prey = 10

    def dx(self, x, y, z):
        """
        Рассчитывает изменение размера популяции жертвы с помощью уравнения Лотки-Вольтерры
        для добычи
        """

        # Рассчитать скорость изменения численности травоядных
        dx_dt = x * (self.b1 - x/3 - self.a12*y - self.a13*z)
        return dx_dt

    def dy(self, x, y, z):
        """
        Рассчитывает изменение размера популяции хищников с помощью
        Уравнения Лотки-Вольтерра для хищников
        """

        # Calculate the rate of population change
        dy_dt = y * (-self.b2 + self.a21*x)

        # Calculate the predator population change
        return dy_dt

    def dz(self, x, y, z):
        """
        Рассчитывает изменение размера популяции хищников с помощью
        Уравнения Лотки-Вольтерра для суперхищников
        """

        # Calculate the rate of population change
        dz_dt = z * (-self.b3 + self.a31*x)

        # Calculate the predator population change
        return dz_dt

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
        predator_history = []
        superpredator_history = []

        y0 = np.array([self.prey, self.predators, self.superpredators], dtype='double')
        tspan = np.array([0.0, self.dt * self.iterations], dtype='double')

        try:
            t, y = self.rk4(self.derivetives, tspan, y0, self.iterations)
            prey_history = y[:, 0]
            predator_history = y[:, 1]
            superpredator_history = y[:, 2]

            print('t = ', t)
            #print(predator_history)
            #res = [dict([(ti, yi)]) for ti, yi in zip(t, predator_history)]
            #print(json.dumps(res, indent=2))
        except (RuntimeError, OverflowError, FloatingPointError):
            print("")

        return {
            'prey': prey_history,
            'predator': predator_history,
            'superpredator': superpredator_history
        }

    def derivetives(self, t, rf):

        x = rf[0]
        y = rf[1]
        z = rf[2]

        dxdt = self.dx(x, y, z)
        dydt = self.dy(x, y, z)
        dzdt = self.dz(x, y, z)

        drfdt = np.array([dxdt, dydt, dzdt], dtype='double')
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
