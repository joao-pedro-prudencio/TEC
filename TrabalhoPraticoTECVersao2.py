with open("inserir caminho do arquivo.in", "r") as f:
    texto = f.read()

linhas_processadas = []

linhas = texto.split("\n")

if linhas[0] == ';S':

    linhas_resultantes = []
    for linha in linhas:
        if ';' in linha:
            linha = linha.split(';')[0].strip()
        if not linha.strip().startswith(';'):
            linhas_resultantes.append(linha)

    linhas = linhas_resultantes

    for linha in linhas[1:]:
        partes = linha.split()
        
        if len(partes) == 5:
            linha_dict = {
                'current state': partes[0],
                'current symbol': partes[1],
                'new symbol': partes[2],
                'direction': partes[3],
                'new state': partes[4]
            }
            
            if linha_dict['current state'] == '0':
                linha_dict['current state'] = 'inicial'
            if linha_dict['new state'] == '0':
                linha_dict['new state'] = 'inicial'

            linhas_processadas.append(linha_dict)

    texto_formatado = ""

    for dicionario in linhas_processadas:
        linha_texto = f"{dicionario['current state']} {dicionario['current symbol']} {dicionario['new symbol']} {dicionario['direction']} {dicionario['new state']}"
        texto_formatado += linha_texto + "\n"

    texto_final = '0 * * l 0  \n0 _ # r inicial \n* # * r *\n' + texto_formatado

elif linhas[0] == ';I':

    linhas_resultantes = []
    for linha in linhas:
        if ';' in linha:
            linha = linha.split(';')[0].strip()
        if not linha.strip().startswith(';'):
            linhas_resultantes.append(linha)

    linhas = linhas_resultantes

    for linha in linhas[1:]:
        partes = linha.split()
        
        if len(partes) == 5:
            linha_dict = {
                'current state': partes[0],
                'current symbol': partes[1],
                'new symbol': partes[2],
                'direction': partes[3],
                'new state': partes[4]
            }
            
            if linha_dict['current state'] == '0':
                linha_dict['current state'] = 'inicial'
            if linha_dict['new state'] == '0':
                linha_dict['new state'] = 'inicial'

            linhas_processadas.append(linha_dict)

    texto_formatado = ""

    for dicionario in linhas_processadas:
        linha_texto = f"{dicionario['current state']} {dicionario['current symbol']} {dicionario['new symbol']} {dicionario['direction']} {dicionario['new state']}"
        texto_formatado += linha_texto + "\n"

    texto_inicial = """; Marcando inicio e fim
0 0 # r escreve0
0 1 # r escreve1
; empurrando todos para frente
escreve0 0 0 r escreve0
escreve0 1 0 r escreve1
escreve0 _ 0 r marcarFinal
escreve1 0 1 r escreve0
escreve1 1 1 r escreve1
escreve1 _ 1 r marcarFinal
; marcando o final da configuracao
marcarFinal _ $ * voltaPara#
; voltando para o inicio
voltaPara# * * l voltaPara#
voltaPara# # # r inicial

; Programa da linguagem do arquivo de entrada
"""
    texto_final = texto_inicial + texto_formatado

    current_states_set = set()

    for dicionario in linhas_processadas:
        current_states_set.add(dicionario['current state'])

    current_states_list = list(current_states_set)

    print(current_states_list)

    texto_chegou_simbolo_final = '\n; Caso chegue no simbolo final\n\n'

    for estado in current_states_list:
        texto_chegou_simbolo_final = texto_chegou_simbolo_final + f"{estado} $ _ r escreve$com{estado}\nescreve$com{estado} _ $ l {estado}\n\n"

    texto_final = texto_final + texto_chegou_simbolo_final

    texto_chegou_simbolo_inicial = '\n; Caso chegue no simbolo do comeco, vai para direita lembrando do estado atual\n\n'

    for estado in current_states_list:
        texto_chegou_simbolo_inicial = texto_chegou_simbolo_inicial + f'{estado} # # r escreveSimbolo_Estado{estado}\n'

    symbols_set = set()

    for dicionario in linhas_processadas:
        symbols_set.add(dicionario['current symbol'])
        symbols_set.add(dicionario['new symbol'])

    symbols_list = list(symbols_set)

    print(symbols_list)

    for estado in current_states_list:
        texto_chegou_simbolo_inicial = texto_chegou_simbolo_inicial + f'\n; Mantendo a informacao: Estado atual = {estado}\n'
        for simboloParaEscrever in symbols_list:
            texto_chegou_simbolo_inicial = texto_chegou_simbolo_inicial + f'\n; Escrevendo simbolo {simboloParaEscrever}\n\n'
            for simboloParaLer in symbols_list:
                texto_chegou_simbolo_inicial = texto_chegou_simbolo_inicial + f'escreveSimbolo{simboloParaEscrever}Estado{estado} {simboloParaLer} {simboloParaEscrever} r escreveSimbolo{simboloParaLer}Estado{estado}\n'
            texto_chegou_simbolo_inicial = texto_chegou_simbolo_inicial + f'escreveSimbolo{simboloParaEscrever}Estado{estado} $ {simboloParaEscrever} r escreveSimbolo$Estado{estado}\n'
        texto_chegou_simbolo_inicial = texto_chegou_simbolo_inicial + f'\n; Chegou no simbolo final lembrando que o estado e o {estado}\nescreveSimbolo$Estado{estado} _ $ * voltaInicioComEstado{estado}\nvoltaInicioComEstado{estado} * * l voltaInicioComEstado{estado}\nvoltaInicioComEstado{estado} # # r {estado}\n'

    texto_final = texto_final + texto_chegou_simbolo_inicial

else:
    print('O texto deve iniciar com ;S ou ;I')

with open("inserir caminho do arquivo.out", "w") as f:
        f.write(texto_final)