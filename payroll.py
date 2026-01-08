def calculate_salary(basic, days):
    hra = basic * 0.20
    da = basic * 0.10
    pf = basic * 0.12

    gross = basic + hra + da
    net = gross - pf
    net = (net / 30) * days

    return round(gross,2), round(net,2)
