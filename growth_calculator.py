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
        для добычи и дельта времени, определенной в "self.dt"
        """

        # Calculate the rate of population change
        dx_dt = x * (self.b1 - self.a12*y - self.a13*z)

        # Calculate the prey population change
        return dx_dt * self.dt

    def dy(self, x, y, z):
        """
        Рассчитывает изменение размера популяции хищников с помощью
        Уравнения Лотки-Вольтерра для хищников и дельта времени, определенной в "self.dt"
        """

        # Calculate the rate of population change
        dy_dt = y * (-self.b2 + self.a21*x - self.a23*z)

        # Calculate the predator population change
        return dy_dt * self.dt

    def dz(self, x, y, z):
        """
        Рассчитывает изменение размера популяции хищников с помощью
        Уравнения Лотки-Вольтерра для хищников и дельта времени, определенной в "self.dt"
        """

        # Calculate the rate of population change
        dz_dt = z * (-self.b3 + self.a31*x + self.a32*y)

        # Calculate the predator population change
        return dz_dt * self.dt

    def calculate(self):
        """
        Calculates the predator/prey population growth for the given parameters
        (Defined in the __init__ docstring). Returns the following dictionary:

        {'predator': [predator population history as a list],
         'prey': [prey population history as a list]}
        """
        predator_history = []
        prey_history = []
        superpredator_history = []

        for i in range(self.iterations):
            xk_1 = self.dx(self.prey, self.predators, self.superpredators)
            yk_1 = self.dy(self.prey, self.predators, self.superpredators)
            zk_1 = self.dz(self.prey, self.predators, self.superpredators)

            #xk_2 = self.dx(self.prey + xk_1, self.predators + yk_1, self.superpredators + zk_1)
            #yk_2 = self.dy(self.prey + xk_1, self.predators + yk_1, self.superpredators + zk_1)
            #zk_2 = self.dz(self.prey + xk_1, self.predators + yk_1, self.superpredators + zk_1)

            ##self.prey = self.prey + (xk_1 + xk_2) / 2
            #self.predators = self.predators + (yk_1 + yk_2) / 2
            #self.superpredators = self.superpredators + (zk_1 + zk_2) / 2

            xk_2 = self.dx(self.prey + xk_1/2, self.predators + yk_1, self.superpredators + zk_1)
            yk_2 = self.dy(self.prey + xk_1/2, self.predators + yk_1, self.superpredators + zk_1)
            zk_2 = self.dz(self.prey + xk_1, self.predators + yk_1, self.superpredators + zk_1)

            predator_history.append(self.predators)
            prey_history.append(self.prey)
            superpredator_history.append(self.superpredators)

        return {
            'predator': predator_history,
            'prey': prey_history,
            'superpredator': superpredator_history
        }
