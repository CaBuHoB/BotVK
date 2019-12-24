import numpy as np
import pandas as pd
import sympy
from sympy import Add, div, latex

x = sympy.Symbol('x')
a = sympy.Symbol('a')


def get_tables_log_exp(GF_step, p, use_latex):
    global x
    degree_of_symbol_x = np.zeros((2 ** GF_step + 1, 3), dtype=object)
    degree_of_symbol_x_latex = np.zeros((2 ** GF_step + 1, 3), dtype=object)
    degree_of_symbol_x[0][2] = '{:>0{GF}b}'.format(0, GF=GF_step)
    for i in range(1, 2 ** GF_step + 1):
        degree_of_symbol_x[i][0] = x ** (i - 1)
        degree_of_symbol_x[i][1] = degree_of_symbol_x[i - 1][0] * x if i != 1 else 1
        q, pol = div(degree_of_symbol_x[i][1], p)
        pol = pol.as_poly(x, domain='GF(2)')
        degree_of_symbol_x[i][1] = pol.args[0]
        degree_of_symbol_x[i][2] = '{:>0{GF}s}'.format(''.join([str(x) for x in list(pol.all_coeffs())]), GF=GF_step)

        if use_latex:
            degree_of_symbol_x_latex[i][0] = '$' + latex(degree_of_symbol_x[i][0]) + '$'
            degree_of_symbol_x_latex[i][1] = '$' + latex(degree_of_symbol_x[i][1]) + '$'
            degree_of_symbol_x_latex[i][2] = degree_of_symbol_x[i][2]

    log_table = np.zeros((2 ** GF_step, 2), dtype=object)
    for i in range(2 ** GF_step):
        log_table[i][0] = '{:>0{GF}b}'.format(i, GF=GF_step)
        if i == 0:
            log_table[i][1] = -np.inf
        else:
            k, l = np.where(degree_of_symbol_x[:-1] == '{:>0{GF}b}'.format(i, GF=GF_step))
            log_table[i][1] = k[0] - 1

    exp_table = np.fliplr(log_table[log_table[:, 1].argsort()])[1:]

    if use_latex:
        return degree_of_symbol_x_latex, log_table, exp_table
    return degree_of_symbol_x, log_table, exp_table


def sum_alpha(pol, degree_of_symbol_x):
    sum_alpha_num = 0
    if pol.is_Integer:
        sum_alpha_num ^= int(pol)
    elif pol.is_Pow:
        sum_alpha_num ^= int(degree_of_symbol_x[int(pol.args[1]) + 1][2], 2)
    elif pol.is_Symbol:
        sum_alpha_num ^= int(degree_of_symbol_x[2][2], 2)
    else:
        for i in range(len(pol.args)):
            if pol.args[i].is_Integer:
                sum_alpha_num ^= int(degree_of_symbol_x[1][2], 2)
            elif pol.args[i].is_Symbol:
                sum_alpha_num ^= int(degree_of_symbol_x[2][2], 2)
            else:
                sum_alpha_num ^= int(degree_of_symbol_x[int(pol.args[i].args[1]) + 1][2], 2)

    return sum_alpha_num


def calc_S(v_vec, alpha_degree, GF_step, degree_of_symbol_x, use_latex):
    global x
    v_alpha = Add()
    v_alpha_mod = Add()
    for i in range(len(v_vec)):
        v_alpha += v_vec[i] * x ** (i * alpha_degree)
        v_alpha_mod += v_vec[i] * x ** ((i * alpha_degree) % (2 ** GF_step - 1))
    v_alpha_mod = v_alpha_mod.as_poly(x, domain='GF(2)').args[0]
    S = sum_alpha(v_alpha_mod, degree_of_symbol_x)

    if v_alpha == v_alpha_mod:
        if use_latex:
            calc = latex(v_alpha)
        else:
            calc = v_alpha.__str__()
    else:
        if use_latex:
            calc = latex(v_alpha) + ' = ' + latex(v_alpha_mod)
        else:
            calc = v_alpha.__str__() + ' = ' + v_alpha_mod.__str__()

    if S == 0:
        return 0, 0, calc

    k, l = np.where(degree_of_symbol_x[:-1] == '{:>0{GF}b}'.format(S, GF=GF_step))
    return a ** (int(k) - 1), int(k), calc


def degree_mod(pol, mod: int):
    if pol.is_Integer or pol.is_Symbol:
        return pol

    if pol.is_Pow:
        return pol.args[0] ** (int(pol.args[1]) % mod)

    new_pol = Add()
    for i in range(len(pol.args)):
        if pol.args[i].is_Integer or pol.args[i].is_Symbol:
            new_pol += pol.args[i]
        else:
            new_pol += pol.args[i].args[0] ** (int(pol.args[i].args[1]) % mod)
    if pol.args[-1].is_Integer:
        return new_pol.as_poly(a, domain='GF(2)').args[0]
    elif pol.args[-1].is_Symbol:
        return new_pol.as_poly(pol.args[-1], domain='GF(2)').args[0]
    else:
        return new_pol.as_poly(pol.args[-1].args[0], domain='GF(2)').args[0]


def get_lambda_2(S1, S3, degree_of_symbol_x, GF_step):
    Lambda2_first = Add(S3 + S1 ** 3)
    Lambda2_second = degree_mod(S1 ** (-1), 2 ** GF_step - 1) if S1 != 0 else 0
    Lambda2_mul = Lambda2_first * Lambda2_second
    if not Lambda2_mul.is_Integer:
        Lambda2_mul = Lambda2_mul.as_poly().args[0]
    Lambda2_mul = Lambda2_mul.as_poly(a, domain='GF(2)').args[0]
    Lambda2_mod = degree_mod(Lambda2_mul, 2 ** GF_step - 1)
    if Lambda2_mod == 0:
        return False, 0, 0
    Lambda2_sum = '{:>0{GF}b}'.format(sum_alpha(Lambda2_mod, degree_of_symbol_x), GF=GF_step)
    k, l = np.where(degree_of_symbol_x[:-1] == Lambda2_sum)
    Lambda2 = a ** (int(k) - 1)

    return True, Lambda2, 0


def get_lambda_3(S1, S3, S5, degree_of_symbol_x, GF_step):
    Lambda2_first = Add(S1 ** 2 * S3 + S5)
    Lambda2_second = Add(S1 ** 3 + S3)
    Lambda2_second = Lambda2_second.as_poly(a, domain='GF(2)').args[0]
    Lambda2_second = degree_mod(Lambda2_second, 2 ** GF_step - 1)
    Lambda2_second = Lambda2_second.as_poly(a, domain='GF(2)').args[0]
    Lambda2_second = sum_alpha(Lambda2_second, degree_of_symbol_x)
    if Lambda2_second == 0:
        return False, 0, 0
    Lambda2_second = '{:>0{GF}b}'.format(Lambda2_second, GF=GF_step)
    k, l = np.where(degree_of_symbol_x[:-1] == Lambda2_second)
    Lambda2_second = degree_mod(a ** -(int(k) - 1), 2 ** GF_step - 1)
    Lambda2_mul = Lambda2_first * Lambda2_second
    if not Lambda2_mul.is_Integer:
        Lambda2_mul = Lambda2_mul.as_poly().args[0]
    Lambda2_mod = degree_mod(Lambda2_mul, 2 ** GF_step - 1)
    Lambda2_mod = Lambda2_mod.as_poly(a, domain='GF(2)').args[0]
    Lambda2_sum = '{:>0{GF}b}'.format(sum_alpha(Lambda2_mod, degree_of_symbol_x), GF=GF_step)
    if Lambda2_sum == '0000':
        Lambda2 = 0
    else:
        k, l = np.where(degree_of_symbol_x[:-1] == Lambda2_sum)
        Lambda2 = a ** (int(k) - 1)

    Lambda3_first = Add(S1 ** 3 + S3)
    Lambda3_second = Add(S1 * Lambda2)
    if not Lambda3_second.is_Integer:
        Lambda3_second = Lambda3_second.as_poly().args[0]

    Lambda3_first = Lambda3_first.as_poly(a, domain='GF(2)').args[0]
    Lambda3_second = Lambda3_second.as_poly(a, domain='GF(2)').args[0]
    Lambda3_first = degree_mod(Lambda3_first, 2 ** GF_step - 1)
    Lambda3_second = degree_mod(Lambda3_second, 2 ** GF_step - 1)
    Lambda3 = Lambda3_first + Lambda3_second
    Lambda3 = Lambda3.as_poly(a, domain='GF(2)').args[0]
    Lambda3 = '{:>0{GF}b}'.format(sum_alpha(Lambda3, degree_of_symbol_x), GF=GF_step)
    if Lambda3 == '0000':
        Lambda3 = 0
    else:
        k, l = np.where(degree_of_symbol_x[:-1] == Lambda3)
        Lambda3 = a ** (int(k) - 1)

    return True, Lambda2, Lambda3


def search_error(v_str, GF_step=4, use_latex=True):
    global a
    global x

    g = x ** 10 + x ** 8 + x ** 5 + x ** 4 + x ** 2 + x + 1
    p = x ** 4 + x + 1

    string = ''
    degree_of_symbol_x, log_table, exp_table = get_tables_log_exp(GF_step, p, use_latex)

    degree_of_symbol_x_pd = pd.DataFrame(degree_of_symbol_x, columns=['Mult', 'Ans', 'Bin'])
    if use_latex:
        string += "\\noindent\n\\begin{minipage}[c]{60mm}\n\\parindent=3em"
        table = degree_of_symbol_x_pd.to_latex(index=False, escape=False)
        table = table.replace('toprule', 'hline').replace('midrule', 'hline').replace('bottomrule', 'hline')
        string += table
        string += "\n\\end{minipage}"
        string += "\\hfill"
    else:
        string += '\n'
        string += degree_of_symbol_x_pd.to_string()

    log_table_pd = pd.DataFrame(log_table, columns=['a', 'log(a)'])
    if use_latex:
        string += "\n\\begin{minipage}[c]{30mm}\n"
        table = log_table_pd.to_latex(index=False, escape=False)
        table = table.replace('toprule', 'hline').replace('midrule', 'hline').replace('bottomrule', 'hline')
        string += table
        string += "\n\\end{minipage}"
        string += "\\hfill"
    else:
        string += '\n'
        string += log_table_pd.to_string()

    exp_table_pd = pd.DataFrame(exp_table, columns=['k', r'$\alpha^k$'])
    if use_latex:
        string += "\n\\begin{minipage}[c]{30mm}\n"
        table = exp_table_pd.to_latex(index=False, escape=False)
        table = table.replace('toprule', 'hline').replace('midrule', 'hline').replace('bottomrule', 'hline')
        string += table
        string += "\n\\end{minipage}"
        string += "\\hfill"
        string += '\n'
    else:
        string += '\n'
        string += exp_table_pd.to_string()

    string += '~\\\\ \n ~\\\\ \n\n'
    v_vec = [int(i) for i in list(v_str)]
    v = Add()
    for i in range(len(v_vec)):
        v += v_vec[i] * x ** i
    if use_latex:
        string += '{tab}\n\n$v = {}${newline}\n\n'.format(latex(v), tab=r'~\\', newline=r'\\')
    else:
        string += '\n\nv = {}\n\n'.format(v)

    S1, ind, calc = calc_S(v_vec, 1, GF_step, degree_of_symbol_x, use_latex)
    if use_latex:
        string += '$S1 = {} = {} = {}$\n\n'.format(calc, degree_of_symbol_x[ind][2], latex(S1), GF=GF_step)
    else:
        string += 'S1 = {} = {} = {}\n'.format(calc, degree_of_symbol_x[ind][2], S1, GF=GF_step)

    S3, ind, calc = calc_S(v_vec, 3, GF_step, degree_of_symbol_x, use_latex)
    if use_latex:
        string += '$S3 = {} = {} = {}$\n\n'.format(calc, degree_of_symbol_x[ind][2], latex(S3), GF=GF_step)
    else:
        string += 'S3 = {} = {} = {}\n'.format(calc, degree_of_symbol_x[ind][2], S3, GF=GF_step)

    S5, ind, calc = calc_S(v_vec, 5, GF_step, degree_of_symbol_x, use_latex)
    if use_latex:
        string += '$S5 = {} = {} = {}$\\\\\n\n'.format(calc, degree_of_symbol_x[ind][2], latex(S5), GF=GF_step)
    else:
        string += 'S5 = {} = {} = {}\n\n'.format(calc, degree_of_symbol_x[ind][2], S5, GF=GF_step)

    Lambda1 = S1

    success3, Lambda2, Lambda3 = get_lambda_3(S1, S3, S5, degree_of_symbol_x, GF_step)
    if not success3:
        success2, Lanbda2, Lambda3 = get_lambda_2(S1, S3, degree_of_symbol_x, GF_step)

    if success3:
        if use_latex:
            string += '${slash}Lambda_0 = 1$\n\n'.format(slash='\\')
            string += '${slash}Lambda_1 = S_1 = {}$\n\n'.format(latex(Lambda1), slash='\\')
            string += '${slash}Lambda_2 = (S_1^2 {slash}cdot S_3 + S_5) {slash}cdot {one} = {}$\n\n'. \
                format(latex(Lambda2), slash='\\', one=r'{(S_1^3 + S_3)}^{-1}')
            string += '${slash}Lambda_3 = (S_1^3 + S_3) + S_1{slash}cdot{slash}Lambda_2 = {}$\\\\\n\n'. \
                format(latex(Lambda3), slash='\\')
        else:
            string += 'Lambda0 = 1\n'
            string += 'Lambda1 = S1 = {}\n'.format(Lambda1)
            string += 'Lambda2 = (S1^2*S3 + S5)*(S1^3 + S3)^-1 = {}\n'.format(Lambda2)
            string += 'Lambda3 = (S1^3 + S3) + S1*Lambda2 = {}\n\n'.format(Lambda3)
    elif success2:
        if use_latex:
            string += '$\\Lambda_0 = 1$\n\n'
            string += '$\\Lambda_1 = S_1 = {}$\n\n'.format(latex(Lambda1))
            string += '$\\Lambda_2 = (S_3 + S_1^3){one} = {}$\n\n'. \
                format(latex(Lambda2), one=r'S1^{-1}')
        else:
            string += 'Lambda0 = 1\n'
            string += 'Lambda1 = S1 = {}\n'.format(Lambda1)
            string += 'Lambda2 = (S3 + S1^3)S1^-1 = {}\n\n'.format(Lambda2)
    else:
        if use_latex:
            string += '$\\Lambda_0 = 1$\n\n'
            string += '$\\Lambda_1 = S_1 = {}$\n\n'.format(latex(Lambda1))
        else:
            string += 'Lambda0 = 1\n'
            string += 'Lambda1 = S1 = {}\n\n'.format(Lambda1)

    Lambda = Add() + 1 + Lambda1 * x + Lambda2 * (x ** 2) + Lambda3 * (x ** 3)
    max_count = 0
    if Lambda1 != 0:
        max_count = 1
    if Lambda2 != 0:
        max_count = 2
    if Lambda3 != 0:
        max_count = 3
    if use_latex:
        string += '\n$\\Lambda = {}$\\\\\n\n'.format(latex(Lambda))
    else:
        string += 'Lambda = {}\n\n'.format(Lambda)

    Lambda_vec = np.zeros((2 ** GF_step - 1, 2), dtype=object)
    count = 0
    stop = 0
    for i in range(2 ** GF_step - 1):
        xreplace = Lambda.xreplace({x: a ** i}).as_poly(a, domain='GF(2)').args[0]
        Lambda_vec[i][0] = degree_mod(xreplace, 2 ** GF_step - 1)
        Lambda_vec[i][1] = sum_alpha(Lambda_vec[i][0], degree_of_symbol_x)
        if Lambda_vec[i][1] == 0:
            count += 1
        if xreplace == Lambda_vec[i][0]:
            if use_latex:
                string += '$\\Lambda({}) = {} = {}$\n\n'.format(latex(a ** i), latex(Lambda_vec[i][0]),
                                                                '{:>0{GF}b}'.format(Lambda_vec[i][1], GF=GF_step))
            else:
                string += 'Lambda({}) = {} = {}\n'.format(a ** i, Lambda_vec[i][0],
                                                          '{:>0{GF}b}'.format(Lambda_vec[i][1], GF=GF_step))
        else:
            if use_latex:
                string += '$\\Lambda({}) = {} = {} = {}$\n\n'.format(latex(a ** i), latex(xreplace),
                                                                     latex(Lambda_vec[i][0]),
                                                                     '{:>0{GF}b}'.format(Lambda_vec[i][1], GF=GF_step))
            else:
                string += 'Lambda({}) = {} = {} = {}\n'.format(a ** i, xreplace, Lambda_vec[i][0],
                                                               '{:>0{GF}b}'.format(Lambda_vec[i][1], GF=GF_step))

        if count == max_count:
            stop = i + 1
            break

    ans = np.where(Lambda_vec[:stop, 1] == 0)[0]
    ans = [a ** int(an) for an in ans]
    if use_latex:
        string += '~\\\\\n\n'
        string += "\\noindent\n\\begin{minipage}[c]{40mm}\n\\parindent=3em"
    else:
        string += '\n'
    for i in range(len(ans)):
        if use_latex:
            string += '$x_{} = {}${end}'.format(i, latex(ans[i]), end='\n~\\\\\n' if i == (len(ans)) else '\n\n')
        else:
            string += 'x{} = {}\n'.format(i, ans[i])
    if use_latex:
        string += "\n\\end{minipage}"
        string += "\\hfill"
        string += "\n\\begin{minipage}[c]{40mm}\n"
        # string += '\n\n'
    else:
        string += '\n'
    ans = [degree_mod(an ** (-1), 2 ** GF_step - 1) for an in ans]
    for i in range(len(ans)):
        if use_latex:
            string += '$x_{}^{one} = {}${end}'.format(i, latex(ans[i]), one='{-1}',
                                                      end='\n~\\\\\n' if i == (len(ans)) else '\n\n')
        else:
            string += 'x{}^-1 = {}\n'.format(i, ans[i], one='{-1}')
    if use_latex:
        string += "\n\\end{minipage}"
        string += "\\hfill"
        string += "\n\\begin{minipage}[c]{40mm}\n"
        # string += '\n\n'
    else:
        string += '\n'
    ans = [0 if an == 1 else 1 if an == a else int(an.args[1]) for an in ans]
    for i in range(len(ans)):
        if use_latex:
            string += '$\\log(x_{}^{one}) = {}$\n\n'.format(i, ans[i], one='{-1}')
        else:
            string += 'log(x{}^-1) = {}\n'.format(i, ans[i])

    if use_latex:
        string += "\n\\end{minipage}"
        string += "\\hfill"

    ans.sort()
    string += '\n~\\\\\n\nError in: {}'.format(ans)

    return string, ans
