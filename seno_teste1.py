# Constantes da série de Taylor
k2 = -0.50000000000000000000
k3 = -0.16666666666666666666
k4 = 0.04166666666666666666
k5 = 0.00833333333333333333
k6 = -1.388888888888889E-03
k7 = -1.984126984126984E-04
k8 = 2.480158730158730E-05
k9 = 2.755731922398589E-06
k10 = -2.755731922398589E-07
k11 = -2.505210838544172E-08
k12 = 2.087675698786810E-09

# Constantes de PI com alta precisão
PI = 3.14159265358979323846264
PI4 = PI / 4.0
PI2 = PI / 2.0
dPI = PI * 2.0


def fabs(x):
    """Valor absoluto sem usar math"""
    return x if x >= 0 else -x


def seno(x):
    """
    Calcula o seno usando série de Taylor com redução de argumento.
    Funciona para qualquer ângulo usando periodicidade e simetria.
    """
    # Redução para o intervalo [0, 2π] usando periodicidade
    # sen(x + 2πk) = sen(x)
    if x > dPI or x < 0:
        # Normaliza o ângulo para [0, 2π]
        k = int(x / dPI)
        x = x - k * dPI
        if x < 0:
            x = x + dPI
    
    # Agora x está em [0, 2π]
    # Reduzimos para [-π/2, π/2] usando simetrias
    
    # Segundo quadrante: [π/2, π]
    # sen(x) = sen(π - x)
    if x > PI2 and x <= PI:
        x = PI - x
    
    # Terceiro quadrante: [π, 3π/2]
    # sen(x) = -sen(x - π)
    elif x > PI and x <= PI + PI2:
        x = x - PI
        return -seno(x)  # chamada recursiva com sinal negativo
    
    # Quarto quadrante: [3π/2, 2π]
    # sen(x) = -sen(2π - x)
    elif x > PI + PI2:
        x = dPI - x
        return -seno(x)  # chamada recursiva com sinal negativo
    
    # Agora x está em [-π/2, π/2]
    
    # Intervalo de confiança primário: [-π/4, π/4]
    if fabs(x) <= PI4:
        y = x * x
        return x * (1 + y * (k3 + y * (k5 + y * (k7 + y * (k9 + k11 * y)))))
    
    # Primeiro quadrante estendido: [π/4, π/2]
    # seno(x) = cos(π/2 - x)
    if x > PI4 and x <= PI2:
        xr = PI2 - x
        y = xr * xr
        return 1 + y * (k2 + y * (k4 + y * (k6 + y * (k8 + y * (k10 + k12 * y)))))
    
    # Quarto quadrante estendido: [-π/2, -π/4]
    # seno(x) = -cos(-π/2 - x)
    if x >= -PI2 and x < -PI4:
        xr = -(PI2 + x)
        y = xr * xr
        return -(1 + y * (k2 + y * (k4 + y * (k6 + y * (k8 + y * (k10 + k12 * y))))))
    
    return 0.0


def main():
    # Para comparação, importamos math apenas para verificação
    import math
    
    print("=" * 60)
    print("CÁLCULO DO SENO USANDO SÉRIE DE TAYLOR")
    print("=" * 60)
    
    # Testes específicos
    print("\nTestes específicos:")
    print("-" * 60)
    
    angulos_teste = [
        0,           # zero
        PI/6,        # 1º quadrante (30°)
        PI/4,        # 1º quadrante (45°)
        PI/3,        # 1º quadrante (60°)
        PI/2,        # 90°
        2*PI/3,      # 2º quadrante (120°)
        3*PI/4,      # 2º quadrante (135°)
        5*PI/6,      # 2º quadrante (150°)
        PI,          # 180°
        -PI/6,       # 4º quadrante (-30°)
        -PI/3,       # 4º quadrante (-60°)
        -PI/2,       # -90°
        -2*PI/3,     # 3º quadrante (-120°)
        -PI,         # -180°
        7*PI/4,      # 4º quadrante (315°)
        2*PI         # 360°
    ]
    
    for a in angulos_teste:
        s = seno(a)
        s_math = math.sin(a)
        erro = fabs(s - s_math)
        print(f"x = {a:10.6f} | seno(x) = {s:18.15f} | erro = {erro:.6e}")
    
    # Geração de dados para o gráfico (intervalo completo [0, 2π])
    print("\n" + "=" * 60)
    print("DADOS PARA O SCILAB - Intervalo [0, 2π]:")
    print("=" * 60)
    
    num_pontos = 100
    da = dPI / num_pontos  # incremento do ângulo
    
    print("\nae = [", end="")
    
    a = 0.0
    while a <= dPI:
        s = seno(a)
        s_math = math.sin(a)
        erro = fabs(s - s_math)
        print(f"{a:.6f} {erro:.6e}")
        a += da
    
    print("];")
    
    # Também gera para o intervalo [-π, π]
    print("\n" + "=" * 60)
    print("DADOS PARA O SCILAB - Intervalo [-π, π]:")
    print("=" * 60)
    
    da2 = dPI / num_pontos
    
    print("\nae2 = [", end="")
    
    a = -PI
    while a <= PI:
        s = seno(a)
        s_math = math.sin(a)
        erro = fabs(s - s_math)
        print(f"{a:.6f} {erro:.6e}")
        a += da2
    
    print("];")
    
    # Estatísticas para [0, 2π]
    print("\n" + "=" * 60)
    print("ESTATÍSTICAS [0, 2π]:")
    print("=" * 60)
    
    erros = []
    a = 0.0
    while a <= dPI:
        s = seno(a)
        s_math = math.sin(a)
        erro = fabs(s - s_math)
        erros.append(erro)
        a += da
    
    erro_max = max(erros)
    erro_min = min(erros)
    erro_medio = sum(erros) / len(erros)
    
    print(f"Erro máximo:  {erro_max:.6e}")
    print(f"Erro mínimo:  {erro_min:.6e}")
    print(f"Erro médio:   {erro_medio:.6e}")
    print(f"Número de termos da série: 6 (até ordem 11)")
    print(f"Intervalo testado: [0, 2π]")
    print(f"Número de pontos: {len(erros)}")
    
    # Verificação da precisão
    digitos_precisao = -1
    if erro_max > 0:
        import math as m
        digitos_precisao = int(-m.log10(erro_max))
    
    print(f"Dígitos de precisão estimados: {digitos_precisao}")
    print("=" * 60)


if __name__ == "__main__":
    main()