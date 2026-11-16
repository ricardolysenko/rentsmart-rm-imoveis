from abc import ABC, abstractmethod


class Imovel(ABC):
    """Classe base abstrata que representa um imóvel disponível para locação na R.M Imóveis."""

    def __init__(self, tipo: str, aluguel_base: float) -> None:
        self._tipo = tipo
        self._aluguel_base = aluguel_base

    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def aluguel_base(self) -> float:
        return self._aluguel_base

    @abstractmethod
    def calcular_aluguel_mensal(self) -> float:
        """Calcula e retorna o valor final do aluguel mensal do imóvel."""
        pass

    @abstractmethod
    def detalhar_composicao(self) -> list[tuple[str, float]]:
        """Retorna uma lista de tuplas (descrição, valor) detalhando a composição do aluguel."""
        pass


class Apartamento(Imovel):
    """Representa um apartamento para locação, com regras de quartos, garagem e desconto."""

    ALUGUEL_BASE = 700.00
    ADICIONAL_SEGUNDO_QUARTO = 200.00
    ADICIONAL_GARAGEM = 300.00
    PERCENTUAL_DESCONTO_SEM_CRIANCAS = 0.05

    def __init__(self, quartos: int, tem_garagem: bool, possui_criancas: bool) -> None:
        super().__init__("Apartamento", self.ALUGUEL_BASE)
        if quartos not in (1, 2):
            raise ValueError("Apartamento deve ter 1 ou 2 quartos.")
        self.quartos = quartos
        self.tem_garagem = tem_garagem
        self.possui_criancas = possui_criancas

    def _calcular_subtotal(self) -> float:
        subtotal = self.aluguel_base
        if self.quartos == 2:
            subtotal += self.ADICIONAL_SEGUNDO_QUARTO
        if self.tem_garagem:
            subtotal += self.ADICIONAL_GARAGEM
        return subtotal

    def calcular_desconto(self) -> float:
        if not self.possui_criancas:
            return self._calcular_subtotal() * self.PERCENTUAL_DESCONTO_SEM_CRIANCAS
        return 0.0

    def calcular_aluguel_mensal(self) -> float:
        return self._calcular_subtotal() - self.calcular_desconto()

    def detalhar_composicao(self) -> list[tuple[str, float]]:
        itens = [(f"Aluguel-base ({self.tipo} - 1 quarto)", self.aluguel_base)]
        if self.quartos == 2:
            itens.append(("Adicional 2º quarto", self.ADICIONAL_SEGUNDO_QUARTO))
        if self.tem_garagem:
            itens.append(("Adicional vaga de garagem (1 vaga)", self.ADICIONAL_GARAGEM))
        desconto = self.calcular_desconto()
        if desconto > 0:
            itens.append(("Desconto 5% (cliente sem crianças)", -desconto))
        return itens


class Casa(Imovel):
    """Representa uma casa para locação, com regras de quartos e vaga de garagem."""

    ALUGUEL_BASE = 900.00
    ADICIONAL_SEGUNDO_QUARTO = 250.00
    ADICIONAL_GARAGEM = 300.00

    def __init__(self, quartos: int, tem_garagem: bool) -> None:
        super().__init__("Casa", self.ALUGUEL_BASE)
        if quartos not in (1, 2):
            raise ValueError("Casa deve ter 1 ou 2 quartos.")
        self.quartos = quartos
        self.tem_garagem = tem_garagem

    def calcular_aluguel_mensal(self) -> float:
        total = self.aluguel_base
        if self.quartos == 2:
            total += self.ADICIONAL_SEGUNDO_QUARTO
        if self.tem_garagem:
            total += self.ADICIONAL_GARAGEM
        return total

    def detalhar_composicao(self) -> list[tuple[str, float]]:
        itens = [(f"Aluguel-base ({self.tipo} - 1 quarto)", self.aluguel_base)]
        if self.quartos == 2:
            itens.append(("Adicional 2º quarto", self.ADICIONAL_SEGUNDO_QUARTO))
        if self.tem_garagem:
            itens.append(("Adicional vaga de garagem (1 vaga)", self.ADICIONAL_GARAGEM))
        return itens


class Estudio(Imovel):
    """Representa um estúdio para locação, com pacote inicial de 2 vagas e vagas extras."""

    ALUGUEL_BASE = 1200.00
    PACOTE_DUAS_VAGAS = 250.00
    VALOR_VAGA_ADICIONAL = 60.00

    def __init__(self, contratar_estacionamento: bool, vagas_adicionais: int = 0) -> None:
        super().__init__("Estúdio", self.ALUGUEL_BASE)
        if vagas_adicionais < 0:
            raise ValueError("A quantidade de vagas adicionais não pode ser negativa.")
        if not contratar_estacionamento and vagas_adicionais > 0:
            raise ValueError("Vagas adicionais exigem a contratação do pacote inicial de 2 vagas.")
        self.contratar_estacionamento = contratar_estacionamento
        self.vagas_adicionais = vagas_adicionais

    def calcular_aluguel_mensal(self) -> float:
        total = self.aluguel_base
        if self.contratar_estacionamento:
            total += self.PACOTE_DUAS_VAGAS
            total += self.vagas_adicionais * self.VALOR_VAGA_ADICIONAL
        return total

    def detalhar_composicao(self) -> list[tuple[str, float]]:
        itens = [(f"Aluguel-base ({self.tipo})", self.aluguel_base)]
        if self.contratar_estacionamento:
            itens.append(("Pacote de estacionamento (2 vagas iniciais)", self.PACOTE_DUAS_VAGAS))
            if self.vagas_adicionais > 0:
                valor_extras = self.vagas_adicionais * self.VALOR_VAGA_ADICIONAL
                itens.append(
                    (f"Vagas adicionais ({self.vagas_adicionais}x R$ 60,00)", valor_extras)
                )
        return itens