import matplotlib.pyplot as plt
import os
import re
import math
from scipy.special import lambertw


"""
D/M/1 Average Age
"""
def d_m_1_average_age(mu, D):
    rho = 1/(mu*D)
    beta = -rho*lambertw((-rho**-1)*math.exp(-1/rho))

    return (1/mu)*(1/(2*rho) + 1/(1-beta))


"""
M/M/1 Average Age
"""
def m_m_1_average_age(mu, lam):
    return (1/mu)*(1 + (mu/lam) + (lam**2/(mu**2 - mu*lam)))

"""
M/U/1 Average Peak Age
"""
def m_u_1_average_peak_age(mu, lam):
    return (1/lam) + (1/mu) + (2*lam)/(3*mu*(mu-lam))

"""
D/M/1 Average Peak Age
"""
def d_m_1_average_peak_age(mu, lam, D):
    rho = 1 / (mu * D)
    beta = -rho * lambertw((-rho ** -1) * math.exp(-1 / rho))

    return (1/lam) + (1/mu) + beta/(mu*(1-beta))


"""
extracts average age, average latency, and average interarrival time

:param string directory_name:
:param int num_directories:
"""
def get_average_data(directory_name, num_directories):
    avg_age = []
    avg_peak_age = []
    avg_latency = []
    avg_inter = []

    for i in range(num_directories):
        dir_name = directory_name + str(i) + "/"

        age = []
        latency = []
        inter = []
        peak_age = []
        files = None
        try:
            files = sorted([file for file in os.listdir(dir_name) if "age" in file],
                           key=lambda x: int(''.join(re.findall(r'\d+', x))))
        except:
            print("Incorrect directory name or no age files in it")
            print(dir_name)
            return

        for file_name in files:
            with open(dir_name + file_name, "r") as f:
                line = f.read().split("\n")
                age.append(float(line[0].split(":")[1]))
                peak_age.append(float(line[1].split(":")[1]))
                latency.append(float(line[2].split(":")[1]))
                inter.append(float(line[3].split(":")[1]))

        avg_age.append(sum(age) / len(age))
        avg_peak_age.append(sum(peak_age)/len(peak_age))
        avg_latency.append(sum(latency) / len(latency))
        avg_inter.append(sum(inter) / len(inter))

    return avg_age, avg_peak_age, avg_latency, avg_inter


"""
plot the age files and plots the average age, average latency, and theoretical results

:param list x:
:param string directory_name:
:param int num_directories:
"""
def plot_age(x, directory_name, num_directories):
    avg_age, avg_peak_age, avg_latency, avg_inter = get_average_data(directory_name, num_directories)

    plt.plot(x, avg_latency, color="black", label="Latency")
    plt.plot(x, avg_inter, color="blue", label="Interarrival")
    plt.plot(x, avg_age, color="red", label="Age")

    plt.scatter(x, avg_latency, color="black")
    plt.scatter(x, avg_inter, color="blue")
    plt.scatter(x, avg_age, color="red")

    plt.legend()
    plt.xlabel("Rate [packet/second]")
    plt.ylabel("Average Age [seconds]")

    plt.show()


"""
plots average age from poisson distribution vs. periodic distribution arrival

:param list x:
:param string poisson_dir:
:param string periodic_dir:
:param int num_poisson_dir:
:param int num_periodic_dir:
"""
def plot_avg_age_distributions(X, poisson_dir, periodic_dir, num_poisson_dir, num_periodic_dir):
    avg_age_poisson, avg_peak_age, z, y = get_average_data(poisson_dir, num_poisson_dir)
    avg_age_periodic, avg_peak_age, z, y = get_average_data(periodic_dir, num_periodic_dir)

    theor_avg_age_poisson = [m_m_1_average_age(10, x) for x in X]
    theor_avg_age_periodic = [d_m_1_average_age(10, 1/x) for x in X]

    plt.plot(X, avg_age_poisson, color="blue", label="Poisson - Emulated o")
    plt.plot(X, theor_avg_age_poisson, color="blue", label="Poisson - Theoretical v")
    plt.plot(X, avg_age_periodic, color="red", label="Periodic - Emulated o")
    plt.plot(X, theor_avg_age_periodic, color="red", label="Periodic - Theoretical v")

    plt.scatter(X, avg_age_poisson, color="blue")
    plt.scatter(X, theor_avg_age_poisson, color="blue", marker='v')
    plt.scatter(X, avg_age_periodic, color="red")
    plt.scatter(X, theor_avg_age_periodic, color="red", marker='v')


    plt.legend()
    plt.xlabel("Rate [packet/second]")
    plt.ylabel("Average Age [seconds]")
    plt.show()


"""
Plots average peak age vs. average age for a poisson arrival distribution

:param list x:
:param string directory:
:param int num_directories:
"""
def plot_avg_age_vs_avg_peak_age_mm1(X, directory, num_directories):
    avg_age, avg_peak_age, y, z = get_average_data(directory, num_directories)
    theor_avg_age = [m_m_1_average_age(10, x) for x in X]
    theor_avg_peak_age = [m_u_1_average_peak_age(10, x) for x in X]

    plt.plot(X, theor_avg_age, color="blue", label="v Avg. Age - Theoretical (M/M/1)")
    plt.plot(X, avg_age, color="blue", label="o Avg. Age - Emulated")
    plt.plot(X, theor_avg_peak_age, color="red", label="v Avg. Peak Age - Theoretical (M/U/1)")
    plt.plot(X, avg_peak_age, color="red", label="o Avg. Peak Age - Emulated")

    plt.scatter(X, theor_avg_age, color="blue", marker='v')
    plt.scatter(X, avg_age, color="blue")
    plt.scatter(X, theor_avg_peak_age, color="red", marker='v')
    plt.scatter(X, avg_peak_age, color="red")

    plt.legend()
    plt.xlabel("Rate [packet/second]")
    plt.ylabel("Average Age [seconds]")
    plt.show()



"""
Plots average peak age vs. average age for a periodic arrival distribution

:param list x:
:param string directory:
:param int num_directories:
"""
def plot_avg_age_vs_avg_peak_age_dm1(X, directory, num_directories):
    avg_age, avg_peak_age, y, z = get_average_data(directory, num_directories)
    theor_avg_age = [d_m_1_average_age(10, 1/x) for x in X]
    theor_avg_peak_age = [d_m_1_average_peak_age(10, x, 1/x) for x in X]

    plt.plot(X, theor_avg_age, color="blue", label="v Avg. Age - Theoretical (D/M/1)")
    plt.plot(X, avg_age, color="blue", label="o Avg. Age - Emulated")
    plt.plot(X, theor_avg_peak_age, color="red", label="v Avg. Peak Age - Theoretical (D/M/1)")
    plt.plot(X, avg_peak_age, color="red", label="o Avg. Peak Age - Emulated")

    plt.scatter(X, theor_avg_age, color="blue", marker='v')
    plt.scatter(X, avg_age, color="blue")
    plt.scatter(X, theor_avg_peak_age, color="red", marker='v')
    plt.scatter(X, avg_peak_age, color="red")

    plt.legend()
    plt.xlabel("Rate [packet/second]")
    plt.ylabel("Average Age [seconds]")
    plt.show()



if __name__=='__main__':
    x = [.3, .5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9.5, 9.7]
    plot_age(x, "/home/jm/Desktop/CORE_Research/data/poisson/data", 13)
    plot_avg_age_distributions(x, "/home/jm/Desktop/CORE_Research/data/poisson/data", "/home/jm/Desktop/CORE_Research/data/periodic/data", 13, 13)
    plot_avg_age_vs_avg_peak_age_mm1(x, "/home/jm/Desktop/CORE_Research/data/poisson/data", 13)
    plot_avg_age_vs_avg_peak_age_dm1(x, "/home/jm/Desktop/CORE_Research/data/periodic/data", 13)