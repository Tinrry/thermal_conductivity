import numpy as np
import matplotlib.pyplot as plt

# 这个算法好像有点问题哦，不能正确预测参数。y = ax + b
def Gibbs_sampling(x, y, iters, init, hyper_param):
    """
    Gibbs sampling for linear regression
    :param x: independent variable
    :param y: dependent variable
    :param iters: number of iterations
    :param init: initial values of w1, w2 and sigma_n_2, 在这个样例里面，w1是截距，w2是斜率，sigma_n_2是残差方差
    :param hyper_param: hyper parameters of mu1, s1, mu2, s2, a and b
    :return: posteriori samples of w1, w2 and s
    """
    # 需要测试一下, 与百科的结果对比。
    w1 = init['w1']
    w2 = init['w2']
    sigma_n_2 = init['sigma_n_2']
    w1_mu = hyper_param['w1_mu']
    w1_sigma = hyper_param['w1_sigma']
    w2_mu = hyper_param['w2_mu']
    w2_sigma = hyper_param['w2_sigma']
    a = hyper_param['a']
    b = hyper_param['b']
    posteriori = {'w1': np.zeros(iters), 'w2': np.zeros(iters), 'sigma_n_2': np.zeros(iters)}
    for i in range(iters):
        # sample w1
        s1_hat = 1 / (len(x) / sigma_n_2 + 1 / w1_sigma)          # 残差方差，var1, w1的方差
        mu1_hat = s1_hat * (sum(y - w2 * x) / sigma_n_2) + (sigma_n_2 * w1_mu) # / (sigma_n_2 + w1_sigma * len(x))     # w1的均值
        w1 = np.random.normal(mu1_hat, np.sqrt(s1_hat))         # 给定均值为mu1_hat, 方差为s1_hat的正态先验
        # sample w2
        s2_hat = 1 / (sum(x ** 2) / sigma_n_2 + 1 / w2_sigma)     # 
        mu2_hat = s2_hat * (sum((y - w1) * x) / sigma_n_2) + (sigma_n_2 * w2_mu) # / (sigma_n_2 + w2_sigma * sum(x ** 2))
        w2 = np.random.normal(mu2_hat, np.sqrt(s2_hat))
        # sample sigma_n_2
        a_hat = a + len(x) / 2
        b_hat = b + 0.5 * sum((y - w1 - w2 * x) ** 2)
        sigma_n_2 = 1 / np.random.gamma(a_hat, 1 / b_hat)
        posteriori['w1'][i] = w1
        posteriori['w2'][i] = w2
        posteriori['sigma_n_2'][i] = sigma_n_2
    return posteriori


np.random.seed(0)

# 自变量
x = np.random.uniform(low=0, high=5, size=5)
# 因变量， y = 2x - 1 + e, e~N(0, 0.5)le
# y = np.random.normal(loc=2*x-1, scale=0.5)
y = 2 * x - 1

iters = 100000
init_data = np.random.normal(loc=0.0, scale=1.0, size=(3,))     # 生成正态分布的随机数
init = {'w1': init_data[0], 'w2': init_data[1], 'sigma_n_2': init_data[2]}
hyper_param = {'w1_mu': 0, 'w1_sigma': 1, 'w2_mu': 0, 'w2_sigma':1, 'a': 2, 'b': 1}
history = Gibbs_sampling(x, y, iters, init, hyper_param)
print(history['w1'].mean(), history['w2'].mean(), history['sigma_n_2'].mean())
# plt.plot(history['w1'], label='w1')
# plt.plot(history['w2'], label='w2')
# plt.plot(history['sigma_n_2'], label='sigma_n_2')
# plt.legend()
# plt.show()
print(f'iter-{iters}: w1 截距：{history["w1"][-1]}, w2 斜率：{history["w2"][-1]}, sigma_n_2 残差方差：{history["sigma_n_2"][-1]}')
# print(f'iter-{iters}: w1 截距：{history['w1'][-1]}, w2 斜率：{history['w2'][-1]}')