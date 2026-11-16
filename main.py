from imoveis import Apartamento, Casa, Estudio, Imovel
from orcamento import OrcamentoLocacao


def ler_inteiro(mensagem: str, minimo: int, maximo: int) -> int:
    while True:
        entrada = input(mensagem).strip()
        try:
            valor = int(entrada)
            if minimo <= valor <= maximo:
                return valor
            print(f"Opção inválida. Digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("Entrada inválida. Digite apenas números inteiros.")


def ler_sim_nao(mensagem: str) -> bool:
    while True:
        entrada = input(mensagem).strip().upper()
        if entrada in ("S", "SIM"):
            return True
        if entrada in ("N", "NAO", "NÃO"):
            return False
        print("Resposta inválida. Digite 'S' para Sim ou 'N' para Não.")


def criar_imovel_interativo() -> Imovel:
    print("\nSelecione a categoria do imóvel:")
    print("  [1] Apartamento (Base: R$ 700,00)")
    print("  [2] Casa        (Base: R$ 900,00)")
    print("  [3] Estúdio     (Base: R$ 1.200,00)")

    categoria = ler_inteiro("Escolha uma opção (1-3): ", 1, 3)

    if categoria == 1:
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        tem_garagem = ler_sim_nao("Deseja incluir 1 vaga de garagem (+R$ 300,00/mês)? [S/N]: ")
        possui_criancas = ler_sim_nao("O cliente possui crianças? [S/N]: ")
        return Apartamento(
            quartos=quartos,
            tem_garagem=tem_garagem,
            possui_criancas=possui_criancas,
        )

    if categoria == 2:
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        tem_garagem = ler_sim_nao("Deseja incluir 1 vaga de garagem (+R$ 300,00/mês)? [S/N]: ")
        return Casa(quartos=quartos, tem_garagem=tem_garagem)

    contratar_estacionamento = ler_sim_nao(
        "Deseja contratar o pacote de estacionamento de 2 vagas (+R$ 250,00/mês)? [S/N]: "
    )
    vagas_adicionais = 0
    if contratar_estacionamento:
        vagas_adicionais = ler_inteiro(
            "Quantas vagas adicionais deseja incluir (+R$ 60,00/mês cada)? [0 ou mais]: ",
            0,
            20,
        )
    return Estudio(
        contratar_estacionamento=contratar_estacionamento,
        vagas_adicionais=vagas_adicionais,
    )


def main() -> None:
    print("=" * 58)
    print("       BEM-VINDO AO RENTSMART - R.M IMÓVEIS")
    print("=" * 58)

    imovel = criar_imovel_interativo()
    parcelas_taxa = ler_inteiro(
        "\nEm quantas parcelas deseja pagar a taxa contratual de R$ 2.000,00? (1 a 5): ",
        1,
        5,
    )

    orcamento = OrcamentoLocacao(imovel=imovel, parcelas_taxa=parcelas_taxa)
    print("\n" + orcamento.gerar_resumo())

    caminho_csv = orcamento.exportar_csv("orcamento_rentsmart.csv")
    print(f"\nProjeção anual (12 meses) exportada com sucesso para: {caminho_csv.resolve()}")


if __name__ == "__main__":
    main()