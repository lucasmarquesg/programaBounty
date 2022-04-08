import pandas as pd
from datetime import datetime


def menu():
    while True:
        print("""\n( 1 ) LISTA JOGADORES
( 2 ) ELIMINAÇÃO
( 3 ) ADICIONAR CABEÇA
( 4 ) EXCLUIR JOGADOR
( SAIR ) FINALIZAR PROGRAMA
        """)
        x = input().strip().upper()
        opções = ["1", "2", "3", "4", "SAIR"]
        if x in opções:
            break
        else:
            print("OPÇÃO INVÁLIDA")
    return x


def imprimir_lista():
    lista_df = pd.read_csv("bountys.txt")
    return(lista_df)


def relatorio(relato):
    relatorio_df = pd.read_csv("relatorio.txt", delimiter="-")
    relatorio_df.loc[len(relatorio.df)] = relato
    relatorio_df.to_csv("relatorio.txt", index=False)


x = input("Deseja reiniciar os Bountys e o Relatorio? S/N ").strip().upper()
if x == "S":
    tempo = datetime.now()
    backup_df = pd.read_csv("bountys.txt")
    backup_df.to_csv("bountys{}-mes{}-dia{}-{}h{}.txt".format(tempo.year, tempo.month, tempo.day, tempo.hour, tempo.minute), index=False)
    for i in range(0,len(backup_df["NOME"]), 1):
        backup_df = backup_df.drop(i, axis=0)
    backup_df.to_csv("bountys.txt", index=False)
    backup_df = pd.read_csv("relatorio.txt")
    backup_df.to_csv("relatorio{}-mes{}-dia{}-{}h{}.txt".format(tempo.year, tempo.month, tempo.day, tempo.hour, tempo.minute), index=False)
    for i in range(0, len(backup_df["RELATÓRIO"]), 1):
        backup_df = backup_df.drop(i, axis=0)
    backup_df.to_csv("relatorio.txt", index=False)

print("TORNEIO PROGRESSIVE K.O.\n    GL POKER CLUB")
cabeça = float(input("\n\nDigite o valor da cabeça: R$"))
while True:

    x = menu()
    if x == "SAIR":
        break
    else:
        x = int(x)
    lista_df = imprimir_lista()

    if x == 1:
        print("{}\n".format(imprimir_lista()))


    if x == 2:
        lista_df = imprimir_lista()
        nomes = []
        eliminado = input("NOME DO ELIMINADO: ").strip().lower().capitalize()
        eliminador = input("NOME DO ELIMINADOR: ").strip().lower().capitalize()
        for i in lista_df["NOME"]:
            nomes.append(i)
        if eliminador != eliminado:
            if eliminador and eliminado in nomes:
                if lista_df.loc[nomes.index(eliminador), "BOUNTY"] == 0 or lista_df.loc[nomes.index(eliminado), "BOUNTY"] == 0:
                    print("\nJOGADORES INVÁLIDOS\nJOGADORES COM BOUNTY ZERADO\n")
                else:
                    lista_df = imprimir_lista()
                    bounty = (lista_df.loc[lista_df["NOME"] == eliminado, ["BOUNTY"]])
                    bounty = (bounty.iat[0,0])/2
                    bounty = float("{:.2f}".format(bounty))
                    saldo_eliminado = (lista_df.loc[lista_df["NOME"] == eliminado, ["SALDO"]])
                    saldo_eliminado = saldo_eliminado.iat[0,0]
                    saldo_eliminador = (lista_df.loc[lista_df["NOME"] == eliminador, ["SALDO"]])
                    saldo_eliminador = saldo_eliminador.iat[0,0]
                    lista_df.loc[lista_df["NOME"] == eliminador, ["BOUNTY"]] += bounty
                    lista_df.loc[lista_df["NOME"] == eliminador, ["SALDO"]] += bounty
                    lista_df.loc[lista_df["NOME"] == eliminado, ["BOUNTY"]] = float(0)
                    relato = "{} com bounty R${:.2f} e saldo R${:.2f} foi eliminado por {} com bounty R${:.2f} e saldo R${:.2f}, agora com R${:.2f} BOUNTY e R${:.2f} SALDO".format(eliminado,
                                                                                                                                                                                    bounty * 2, saldo_eliminado, eliminador, (lista_df.loc[lista_df["NOME"] == eliminador, ["BOUNTY"]]).iat[0, 0] - bounty, saldo_eliminador, (lista_df.loc[lista_df["NOME"] == eliminador, ["BOUNTY"]]).iat[0, 0], (lista_df.loc[lista_df["NOME"] == eliminador, ["SALDO"]]).iat[0, 0])
                    lista_df.to_csv("bountys.txt", index=False)
                    relatorio(relato)
            else:
                print("\nJOGADORES INVÁLIDOS\nJOGADORES NÃO ENCONTRADOS\n")
        else:
            print("\nJOGADORES INVÁLIDOS\nJOGADORES NÃO ENCONTRADOS\n")

    if x == 3:
        lista_df = imprimir_lista()
        nomes = []
        nome = input("Digite o nome do jogador: ").strip().lower().capitalize()
        for i in lista_df["NOME"]:
            nomes.append(i)
        if nome in nomes and lista_df.loc[lista_df["NOME"] == nome].iat[0, 1] == 0.0:
            lista_df.loc[lista_df["NOME"] == nome, "BOUNTY"] = cabeça
            relato = "REBUY {}".format(nome)
            relatorio(relato)
        elif nome not in nomes:
            lista_df.loc[len(nomes) + 1] = [nome, cabeça , 0.0]
            relato = "INSCRIÇÃO {}".format(nome)
            relatorio(relato)
        else:
            print("JOGADOR INVÁLIDO")
        lista_df.to_csv("bountys.txt", index=False)

    if x == 4:
        lista_df = imprimir_lista()
        print(lista_df)
        nomes = []
        nome = input("\nDigite o nome do jogador excluído: ").strip().lower().capitalize()
        for i in lista_df["NOME"]:
            nomes.append(i)
        if nome in nomes:
            lista_df = lista_df.drop(nomes.index(nome), axis=0)
            relato = "JOGADOR EXCLUIDO {}".format(nome)
            relatorio(relato)
        else:
            print("\nJOGADORES INVÁLIDOS\n")
        lista_df.to_csv("bountys.txt", index=False)
