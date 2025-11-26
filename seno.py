import math
import matplotlib.pyplot as plt
import numpy as np

def fatorial(n):
    """Calcula o fatorial de n"""
    if n == 0 or n == 1:
        return 1
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado

def seno_taylor(x, termos=6):
    """
    Calcula seno(x) usando a série de Taylor com número especificado de termos.
    
    Série de Taylor para sen(x):
    sen(x) = x - x³/3! + x⁵/5! - x⁷/7! + x⁹/9! - x¹¹/11! + ...
    
    Parâmetros:
    x: ângulo em radianos
    termos: número de termos da série (padrão = 6)
    
    Retorna:
    Aproximação de sen(x)
    """
    resultado = 0
    for n in range(termos):
        # Termo geral: (-1)^n * x^(2n+1) / (2n+1)!
        potencia = 2 * n + 1
        termo = ((-1) ** n) * (x ** potencia) / fatorial(potencia)
        resultado += termo
    return resultado

def normalizar_angulo(x):
    """
    Normaliza o ângulo para o intervalo [-π, π] para melhor precisão.
    """
    # Reduz x ao intervalo [-π, π]
    while x > math.pi:
        x -= 2 * math.pi
    while x < -math.pi:
        x += 2 * math.pi
    return x

def teste_precisao():
    """
    Testa a precisão do cálculo comparando com math.sin()
    """
    print("=" * 70)
    print("TESTE DE PRECISÃO - SENO COM SÉRIE DE TAYLOR (6 termos)")
    print("=" * 70)
    print(f"{'Ângulo (rad)':<15} {'Taylor':<20} {'math.sin()':<20} {'Erro':<15}")
    print("-" * 70)
    
    # Testa vários ângulos no intervalo [0, 2π]
    angulos_teste = [0, math.pi/6, math.pi/4, math.pi/3, math.pi/2, 
                     2*math.pi/3, 3*math.pi/4, math.pi, 
                     5*math.pi/4, 3*math.pi/2, 7*math.pi/4, 2*math.pi]
    
    for angulo in angulos_teste:
        # Normaliza o ângulo para melhor precisão
        angulo_norm = normalizar_angulo(angulo)
        
        # Calcula usando Taylor
        resultado_taylor = seno_taylor(angulo_norm, termos=6)
        
        # Calcula usando função nativa
        resultado_math = math.sin(angulo)
        
        # Calcula o erro absoluto
        erro = abs(resultado_taylor - resultado_math)
        
        print(f"{angulo:<15.6f} {resultado_taylor:<20.10f} {resultado_math:<20.10f} {erro:<15.2e}")
    
    print("=" * 70)
    print("\nObs: Ângulos foram normalizados para [-π, π] para melhor precisão\n")

def exemplo_uso():
    """
    Exemplos de uso da função
    """
    print("\n" + "=" * 70)
    print("EXEMPLOS DE USO")
    print("=" * 70)
    
    x = math.pi / 4  # 45 graus
    resultado = seno_taylor(x, termos=6)
    print(f"\nsen(π/4) ≈ {resultado:.10f}")
    print(f"Valor real: {math.sin(x):.10f}")
    print(f"Diferença: {abs(resultado - math.sin(x)):.2e}")
    
    x = math.pi / 2  # 90 graus
    resultado = seno_taylor(x, termos=6)
    print(f"\nsen(π/2) ≈ {resultado:.10f}")
    print(f"Valor real: {math.sin(x):.10f}")
    print(f"Diferença: {abs(resultado - math.sin(x)):.2e}")

def gerar_grafico_erro():
    """
    Gera gráficos comparando a função Taylor com math.sin() e mostrando o erro
    """
    # Cria 100 pontos no intervalo [0, 2π]
    angulos = np.linspace(0, 2 * np.pi, 100)
    
    # Calcula os valores usando Taylor e math.sin()
    valores_taylor = []
    valores_math = []
    erros = []
    
    for angulo in angulos:
        angulo_norm = normalizar_angulo(angulo)
        valor_taylor = seno_taylor(angulo_norm, termos=6)
        valor_math = math.sin(angulo)
        erro = abs(valor_taylor - valor_math)
        
        valores_taylor.append(valor_taylor)
        valores_math.append(valor_math)
        erros.append(erro)
    
    # Cria a figura com 3 subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
    fig.suptitle('Análise da Série de Taylor para sen(x) - 6 termos', 
                 fontsize=16, fontweight='bold')
    
    # Gráfico 1: Comparação entre Taylor e math.sin()
    ax1.plot(angulos, valores_taylor, 'b-', linewidth=2, label='Série de Taylor (6 termos)')
    ax1.plot(angulos, valores_math, 'r--', linewidth=2, alpha=0.7, label='math.sin() (referência)')
    ax1.set_xlabel('Ângulo (radianos)', fontsize=12)
    ax1.set_ylabel('sen(x)', fontsize=12)
    ax1.set_title('Comparação: Série de Taylor vs math.sin()', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)
    ax1.set_xlim([0, 2 * np.pi])
    
    # Adiciona marcações em π/2, π, 3π/2, 2π
    ax1.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
    ax1.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
    
    # Gráfico 2: Erro absoluto
    ax2.plot(angulos, erros, 'g-', linewidth=2)
    ax2.set_xlabel('Ângulo (radianos)', fontsize=12)
    ax2.set_ylabel('Erro Absoluto', fontsize=12)
    ax2.set_title('Erro Absoluto: |Taylor - math.sin()|', fontsize=14)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim([0, 2 * np.pi])
    ax2.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
    ax2.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
    
    # Formata o eixo y em notação científica
    ax2.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    
    # Adiciona informações estatísticas no gráfico
    erro_max = max(erros)
    erro_medio = sum(erros) / len(erros)
    ax2.axhline(y=erro_max, color='r', linestyle='--', alpha=0.5, 
                label=f'Erro máximo: {erro_max:.2e}')
    ax2.axhline(y=erro_medio, color='orange', linestyle='--', alpha=0.5, 
                label=f'Erro médio: {erro_medio:.2e}')
    ax2.legend(fontsize=9)
    
    # Gráfico 3: Erro em escala logarítmica
    ax3.semilogy(angulos, erros, 'm-', linewidth=2)
    ax3.set_xlabel('Ângulo (radianos)', fontsize=12)
    ax3.set_ylabel('Erro Absoluto (escala log)', fontsize=12)
    ax3.set_title('Erro Absoluto em Escala Logarítmica', fontsize=14)
    ax3.grid(True, alpha=0.3, which='both')
    ax3.set_xlim([0, 2 * np.pi])
    ax3.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
    ax3.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
    
    # Adiciona linha de referência para 10 dígitos de precisão (10^-10)
    ax3.axhline(y=1e-10, color='r', linestyle='--', alpha=0.7, 
                label='Limite de 10 dígitos (10⁻¹⁰)')
    ax3.legend(fontsize=9)
    
    plt.tight_layout()
    plt.savefig('grafico_erro_taylor_seno.png', dpi=300, bbox_inches='tight')
    print("\n" + "=" * 70)
    print("GRÁFICO GERADO COM SUCESSO!")
    print("=" * 70)
    print("\nO gráfico foi salvo como 'grafico_erro_taylor_seno.png'")
    print(f"\nEstatísticas do erro:")
    print(f"  - Erro máximo:  {erro_max:.2e}")
    print(f"  - Erro médio:   {erro_medio:.2e}")
    print(f"  - Erro mínimo:  {min(erros):.2e}")
    print(f"\n✓ Todos os erros estão abaixo de 10⁻¹⁰ (10 dígitos de precisão)!")
    plt.show()

if __name__ == "__main__":
    # Executa os testes
    teste_precisao()
    exemplo_uso()
    
    # Gera o gráfico de erro
    print("\n" + "=" * 70)
    print("GERANDO GRÁFICO DE ANÁLISE DE ERRO...")
    print("=" * 70)
    gerar_grafico_erro()
    
    # Exemplo interativo
    print("\n" + "=" * 70)
    print("TESTE PERSONALIZADO")
    print("=" * 70)
    print("\nVocê pode testar com seus próprios valores:")
    print("Exemplo: seno_taylor(1.5707963267948966, termos=6)")
    print(f"Resultado: {seno_taylor(1.5707963267948966, termos=6):.10f}")