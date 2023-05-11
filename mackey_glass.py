import numpy as np

class MackeyGlass:
    def __init__(self, gamma=0.1, beta_0=0.2, n=10, tau=22, p_0=0.1, change_time=None, gamma_2=None, beta_2=None, n_2=None, tau_2=None):
        print(f'{gamma}, {beta_0}, {n}, {tau}, {p_0}')
        self.gamma = gamma
        self.beta_0 = beta_0
        self.n = n
        self.tau = tau
        self.scale_factor = 1000

        self.qs = [p_0] * self.tau

        self.change_time = change_time
        self.changed = change_time is None
        print(self.changed)

        self.gamma_2 = gamma_2
        self.beta_2 = beta_2
        self.n_2 = n_2
        self.tau_2 = tau_2
        pass

    def __call__(self, t, x, dt=1e-3):
        if not self.changed and t > self.change_time:
            self.beta_0=self.beta_2
            self.gamma=self.gamma_2
            self.tau = self.tau_2
            self.n = self.n_2
            self.qs = self.qs[:self.tau]
        ### end if
        q_tau = self.qs.pop()
        dq_dt = (self.beta_0 * q_tau / ( 1 + q_tau**self.n)) - self.gamma * self.qs[0]

        q = self.qs[0] + dq_dt #* (dt*self.scale_factor) # Make 1 second equivalent to 1 day
        self.qs.insert(0, q)
        assert len(self.qs) == self.tau
        return q

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    mg = MackeyGlass(gamma=0.1, beta_0=0.2, n=10, tau=22, p_0=0.1, change_time=4000,
                     gamma_2=0.1, beta_2=0.2, n_2=10, tau_2=6)
    ts = range(3000)
    xs = [mg(t, None) for t in ts]

    plt.plot(ts, xs)
    plt.show()
