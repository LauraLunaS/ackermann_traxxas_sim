"""
Relatorio da suite de cenarios (submodulo 4.4 da Fase 4 - bancada de avaliacao).

Formata os resumos do `comparador` (4.2, um por cenario rodado pela 4.3) em
uma tabela Markdown legivel. Sem ROS - so formatacao de texto, testavel com
resumos sinteticos.
"""

COLUNAS = [
    'num_frames', 'mota', 'motp',
    'num_switches', 'num_false_positives', 'num_misses', 'num_matches',
]


def formatar_relatorio(resultados):
    """
    Monta uma tabela Markdown a partir de `resultados`.

    `resultados`: lista de `(nome_cenario, resumo)`, onde `resumo` e um
    dict ou uma linha de DataFrame do `motmetrics` com as chaves de
    `COLUNAS` (o `comparador.calcular_metricas(...).iloc[0]` ja serve).
    """
    linhas = ['| cenario | ' + ' | '.join(COLUNAS) + ' |',
              '|' + '---|' * (len(COLUNAS) + 1)]

    for nome_cenario, resumo in resultados:
        valores = [_formatar_valor(resumo[c]) for c in COLUNAS]
        linhas.append('| ' + nome_cenario + ' | ' + ' | '.join(valores) + ' |')

    return '\n'.join(linhas)


def _formatar_valor(valor):
    if isinstance(valor, float):
        return f'{valor:.3f}'
    return str(valor)
