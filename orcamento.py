import csv
from pathlib import Path
from imoveis import Imovel


class OrcamentoLocacao:
    """Gerencia o cálculo do orçamento mensal, taxa contratual e projeção anual em CSV."""

    TAXA_CONTRATUAL = 2000.00
    MAX_PARCELAS_TAXA = 5
    MESES_PROJECAO = 12

    def __init__(self, imovel: Imovel, parcelas_taxa: int) -> None:
        if not 1 <= parcelas_taxa <= self.MAX_PARCELAS_TAXA:
            raise ValueError(
                f"O parcelamento da taxa contratual deve ser entre 1 e {self.MAX_PARCELAS_TAXA} parcelas."
            )
        self.imovel = imovel
        self.parcelas_taxa = parcelas_taxa

    def valor_aluguel_mensal(self) -> float:
        return self.imovel.calcular_aluguel_mensal()

    def valor_parcela_taxa(self) -> float:
        return self.TAXA_CONTRATUAL / self.parcelas_taxa

    def gerar_projecao_anual(self) -> list[dict[str, float | int]]:
        aluguel = self.valor_aluguel_mensal()
        parcela_taxa = self.valor_parcela_taxa()
        projecao = []

        for mes in range(1, self.MESES_PROJECAO + 1):
            taxa_no_mes = parcela_taxa if mes <= self.parcelas_taxa else 0.0
            total_mes = aluguel + taxa_no_mes
            projecao.append(
                {
                    "mes": mes,
                    "aluguel_mensal": round(aluguel, 2),
                    "parcela_taxa_contratual": round(taxa_no_mes, 2),
                    "total_mes": round(total_mes, 2),
                }
            )
        return projecao

    def gerar_resumo(self) -> str:
        linhas = [
            "=" * 58,
            "        RENTSMART - RESUMO DO ORÇAMENTO (R.M IMÓVEIS)",
            "=" * 58,
            f"Categoria do imóvel: {self.imovel.tipo}",
            "-" * 58,
            "COMPOSIÇÃO DO ALUGUEL MENSAL:",
        ]

        for descricao, valor in self.imovel.detalhar_composicao():
            sinal = "-" if valor < 0 else " "
            linhas.append(f"  {descricao:<40} {sinal}R$ {abs(valor):>8.2f}")

        aluguel_final = self.valor_aluguel_mensal()
        linhas.extend(
            [
                "-" * 58,
                f"  {'ALUGUEL MENSAL FINAL':<40}  R$ {aluguel_final:>8.2f}",
                "=" * 58,
                "TAXA CONTRATUAL (SEPARADA DO ALUGUEL):",
                f"  {'Valor total da taxa contratual':<40}  R$ {self.TAXA_CONTRATUAL:>8.2f}",
                f"  {'Condição de parcelamento':<40}  {self.parcelas_taxa}x de R$ {self.valor_parcela_taxa():.2f}",
                "=" * 58,
                f"Total previsto nos primeiros {self.parcelas_taxa} mês(es): R$ {aluguel_final + self.valor_parcela_taxa():.2f}/mês",
                f"Total previsto após quitação da taxa:     R$ {aluguel_final:.2f}/mês",
                f"Total acumulado em 12 meses (aluguel+taxa): R$ {(aluguel_final * 12) + self.TAXA_CONTRATUAL:.2f}",
                "=" * 58,
            ]
        )
        return "\n".join(linhas)

    def exportar_csv(self, caminho_arquivo: str = "orcamento_rentsmart.csv") -> Path:
        destino = Path(caminho_arquivo)
        projecao = self.gerar_projecao_anual()

        with destino.open(mode="w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(
                [
                    "Mês",
                    "Categoria do Imóvel",
                    "Aluguel Mensal (R$)",
                    "Parcela Taxa Contratual (R$)",
                    "Total Previsto no Mês (R$)",
                ]
            )

            for item in projecao:
                escritor.writerow(
                    [
                        item["mes"],
                        self.imovel.tipo,
                        f"{item['aluguel_mensal']:.2f}",
                        f"{item['parcela_taxa_contratual']:.2f}",
                        f"{item['total_mes']:.2f}",
                    ]
                )

            total_aluguel_ano = self.valor_aluguel_mensal() * self.MESES_PROJECAO
            total_geral_ano = total_aluguel_ano + self.TAXA_CONTRATUAL
            escritor.writerow(
                [
                    "TOTAL 12 MESES",
                    self.imovel.tipo,
                    f"{total_aluguel_ano:.2f}",
                    f"{self.TAXA_CONTRATUAL:.2f}",
                    f"{total_geral_ano:.2f}",
                ]
            )

        return destino