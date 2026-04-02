"""Script para popular o banco de dados com vagas de atendente comercial."""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from app.database import SessionLocal
from app.repositories.vaga_repository import VagaRepository
from app.models.domain import VagaCreate

def criar_vagas_atendente():
    """Cria 10 vagas de atendente comercial básicas."""
    
    vagas = [
        VagaCreate(
            titulo="Atendente Comercial - Loja de Roupas",
            descricao="Atendimento ao cliente em loja física, organização de produtos e auxílio em vendas.",
            requisitos_tecnicos=["Atendimento ao cliente", "Organização", "Uso básico de computador"],
            experiencia_minima="Sem experiência",
            competencias_desejadas=["Simpatia", "Boa comunicação", "Disposição para aprender"]
        ),
        VagaCreate(
            titulo="Atendente de Loja - Varejo",
            descricao="Recepção de clientes, demonstração de produtos e fechamento de vendas.",
            requisitos_tecnicos=["Atendimento presencial", "Operação de caixa", "Conhecimento básico de produtos"],
            experiencia_minima="Não exigida",
            competencias_desejadas=["Proatividade", "Paciência", "Trabalho em equipe"]
        ),
        VagaCreate(
            titulo="Atendente Comercial - Telemarketing",
            descricao="Atendimento telefônico, esclarecimento de dúvidas e registro de pedidos.",
            requisitos_tecnicos=["Telefone", "Computador básico", "Digitação"],
            experiencia_minima="Não necessária",
            competencias_desejadas=["Boa dicção", "Paciência", "Organização"]
        ),
        VagaCreate(
            titulo="Atendente de Farmácia",
            descricao="Atendimento ao público, organização de medicamentos e auxílio ao farmacêutico.",
            requisitos_tecnicos=["Atendimento ao cliente", "Organização de estoque", "Sistema de vendas"],
            experiencia_minima="Desejável 6 meses",
            competencias_desejadas=["Responsabilidade", "Atenção", "Empatia"]
        ),
        VagaCreate(
            titulo="Atendente Comercial - Loja de Calçados",
            descricao="Atendimento em loja, medição de calçados e auxílio na escolha de produtos.",
            requisitos_tecnicos=["Atendimento presencial", "Conhecimento de numeração", "Organização"],
            experiencia_minima="Não exigida",
            competencias_desejadas=["Simpatia", "Paciência", "Boa apresentação"]
        ),
        VagaCreate(
            titulo="Atendente de Loja - Supermercado",
            descricao="Reposição de produtos, atendimento ao cliente e organização de setor.",
            requisitos_tecnicos=["Atendimento ao público", "Organização", "Trabalho físico leve"],
            experiencia_minima="Primeira experiência aceita",
            competencias_desejadas=["Agilidade", "Disposição", "Pontualidade"]
        ),
        VagaCreate(
            titulo="Atendente Comercial - Loja de Eletrônicos",
            descricao="Demonstração de produtos eletrônicos e auxílio técnico básico aos clientes.",
            requisitos_tecnicos=["Conhecimento básico de eletrônicos", "Atendimento", "Informática básica"],
            experiencia_minima="6 meses desejável",
            competencias_desejadas=["Interesse por tecnologia", "Comunicação", "Proatividade"]
        ),
        VagaCreate(
            titulo="Atendente de Recepção - Clínica",
            descricao="Recepção de pacientes, agendamento de consultas e atendimento telefônico.",
            requisitos_tecnicos=["Atendimento ao público", "Telefone", "Computador básico", "Agenda"],
            experiencia_minima="Não necessária",
            competencias_desejadas=["Organização", "Discrição", "Empatia"]
        ),
        VagaCreate(
            titulo="Atendente Comercial - Loja de Cosméticos",
            descricao="Atendimento personalizado, demonstração de produtos de beleza e vendas.",
            requisitos_tecnicos=["Atendimento ao cliente", "Conhecimento de cosméticos", "Vendas"],
            experiencia_minima="Não exigida",
            competencias_desejadas=["Interesse por beleza", "Simpatia", "Persuasão"]
        ),
        VagaCreate(
            titulo="Atendente de Loja - Pet Shop",
            descricao="Atendimento a clientes, orientação sobre produtos pet e organização da loja.",
            requisitos_tecnicos=["Atendimento ao público", "Conhecimento básico de pets", "Organização"],
            experiencia_minima="Primeira experiência",
            competencias_desejadas=["Amor por animais", "Paciência", "Responsabilidade"]
        ),
    ]
    
    db = SessionLocal()
    try:
        repo = VagaRepository(db)
        
        print(f"\n{'='*80}")
        print(f"POPULANDO BANCO COM {len(vagas)} VAGAS DE ATENDENTE COMERCIAL")
        print(f"{'='*80}\n")
        
        for i, vaga_data in enumerate(vagas, 1):
            vaga = repo.criar(vaga_data)
            print(f"✓ [{i:2d}/10] {vaga.titulo} (ID: {vaga.id})")
        
        print(f"\n{'='*80}")
        print(f"✓ {len(vagas)} VAGAS DE ATENDENTE CRIADAS COM SUCESSO!")
        print(f"{'='*80}\n")
        
    finally:
        db.close()

if __name__ == "__main__":
    criar_vagas_atendente()
