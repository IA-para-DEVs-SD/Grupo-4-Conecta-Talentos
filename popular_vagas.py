"""Script para popular o banco de dados com vagas fake."""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from app.database import SessionLocal
from app.repositories.vaga_repository import VagaRepository
from app.models.domain import VagaCreate

def criar_vagas():
    """Cria 30 vagas diversificadas."""
    
    vagas = [
        # Tecnologia - Júnior
        VagaCreate(
            titulo="Desenvolvedor Python Júnior",
            descricao="Desenvolvimento de APIs REST com FastAPI e integração com bancos de dados.",
            requisitos_tecnicos=["Python", "FastAPI", "SQL", "Git"],
            experiencia_minima="1-2 anos",
            competencias_desejadas=["Trabalho em equipe", "Proatividade", "Vontade de aprender"]
        ),
        VagaCreate(
            titulo="Desenvolvedor Frontend Júnior",
            descricao="Desenvolvimento de interfaces web responsivas com React.",
            requisitos_tecnicos=["JavaScript", "React", "HTML", "CSS", "Git"],
            experiencia_minima="1 ano",
            competencias_desejadas=["Criatividade", "Atenção aos detalhes", "Comunicação"]
        ),
        VagaCreate(
            titulo="Analista de QA Júnior",
            descricao="Testes manuais e automatizados de aplicações web e mobile.",
            requisitos_tecnicos=["Testes manuais", "Selenium", "Postman", "SQL básico"],
            experiencia_minima="6 meses",
            competencias_desejadas=["Atenção aos detalhes", "Organização", "Pensamento crítico"]
        ),
        
        # Tecnologia - Pleno
        VagaCreate(
            titulo="Desenvolvedor Full Stack Pleno",
            descricao="Desenvolvimento de aplicações completas com Node.js e React.",
            requisitos_tecnicos=["Node.js", "React", "TypeScript", "MongoDB", "Docker", "AWS"],
            experiencia_minima="3-5 anos",
            competencias_desejadas=["Liderança técnica", "Mentoria", "Resolução de problemas"]
        ),
        VagaCreate(
            titulo="Engenheiro de Dados Pleno",
            descricao="Construção de pipelines de dados e ETL com Python e Spark.",
            requisitos_tecnicos=["Python", "Apache Spark", "SQL", "Airflow", "AWS", "Kafka"],
            experiencia_minima="4 anos",
            competencias_desejadas=["Análise de dados", "Otimização", "Documentação técnica"]
        ),
        VagaCreate(
            titulo="DevOps Engineer Pleno",
            descricao="Automação de infraestrutura e CI/CD com Kubernetes e Terraform.",
            requisitos_tecnicos=["Kubernetes", "Docker", "Terraform", "Jenkins", "AWS", "Linux"],
            experiencia_minima="3-4 anos",
            competencias_desejadas=["Automação", "Troubleshooting", "Colaboração"]
        ),
        
        # Tecnologia - Sênior
        VagaCreate(
            titulo="Arquiteto de Software Sênior",
            descricao="Definição de arquitetura de sistemas distribuídos e microserviços.",
            requisitos_tecnicos=["Microserviços", "Cloud Architecture", "Kubernetes", "Event-Driven", "DDD"],
            experiencia_minima="8+ anos",
            competencias_desejadas=["Visão estratégica", "Liderança", "Comunicação executiva"]
        ),
        VagaCreate(
            titulo="Tech Lead Backend Sênior",
            descricao="Liderança técnica de time backend e definição de padrões de código.",
            requisitos_tecnicos=["Java", "Spring Boot", "Microserviços", "PostgreSQL", "Redis", "Kafka"],
            experiencia_minima="7+ anos",
            competencias_desejadas=["Liderança de equipe", "Mentoria", "Code review"]
        ),
        VagaCreate(
            titulo="Especialista em Machine Learning",
            descricao="Desenvolvimento de modelos de ML e deploy em produção.",
            requisitos_tecnicos=["Python", "TensorFlow", "PyTorch", "MLOps", "AWS SageMaker", "Docker"],
            experiencia_minima="5+ anos",
            competencias_desejadas=["Pesquisa", "Inovação", "Apresentação de resultados"]
        ),
        
        # Design
        VagaCreate(
            titulo="UX/UI Designer Júnior",
            descricao="Criação de interfaces e experiências de usuário para aplicações web.",
            requisitos_tecnicos=["Figma", "Adobe XD", "Prototipagem", "Design System"],
            experiencia_minima="1-2 anos",
            competencias_desejadas=["Criatividade", "Empatia", "Comunicação visual"]
        ),
        VagaCreate(
            titulo="Product Designer Pleno",
            descricao="Design de produtos digitais com foco em UX research e testes.",
            requisitos_tecnicos=["Figma", "User Research", "Testes de Usabilidade", "Design Thinking"],
            experiencia_minima="3-4 anos",
            competencias_desejadas=["Pensamento analítico", "Colaboração", "Storytelling"]
        ),
        VagaCreate(
            titulo="Design System Lead",
            descricao="Liderança na criação e manutenção de design systems corporativos.",
            requisitos_tecnicos=["Figma", "Design Tokens", "Component Library", "Acessibilidade"],
            experiencia_minima="6+ anos",
            competencias_desejadas=["Liderança", "Documentação", "Evangelização"]
        ),
        
        # Marketing
        VagaCreate(
            titulo="Analista de Marketing Digital Júnior",
            descricao="Gestão de campanhas em Google Ads e redes sociais.",
            requisitos_tecnicos=["Google Ads", "Facebook Ads", "Google Analytics", "SEO básico"],
            experiencia_minima="1 ano",
            competencias_desejadas=["Criatividade", "Análise de dados", "Redação"]
        ),
        VagaCreate(
            titulo="Growth Hacker Pleno",
            descricao="Estratégias de crescimento e otimização de funil de conversão.",
            requisitos_tecnicos=["Google Analytics", "A/B Testing", "SQL", "Python", "CRO"],
            experiencia_minima="3-4 anos",
            competencias_desejadas=["Experimentação", "Data-driven", "Criatividade"]
        ),
        VagaCreate(
            titulo="Head de Marketing",
            descricao="Liderança estratégica de marketing e gestão de equipe.",
            requisitos_tecnicos=["Marketing Strategy", "Budget Management", "Analytics", "CRM"],
            experiencia_minima="8+ anos",
            competencias_desejadas=["Liderança estratégica", "Visão de negócio", "Networking"]
        ),
        
        # Vendas
        VagaCreate(
            titulo="SDR - Sales Development Representative",
            descricao="Prospecção ativa e qualificação de leads B2B.",
            requisitos_tecnicos=["CRM (Salesforce/HubSpot)", "LinkedIn Sales Navigator", "Cold calling"],
            experiencia_minima="6 meses",
            competencias_desejadas=["Comunicação", "Persistência", "Organização"]
        ),
        VagaCreate(
            titulo="Account Executive Pleno",
            descricao="Fechamento de vendas B2B e gestão de pipeline comercial.",
            requisitos_tecnicos=["Salesforce", "Negociação", "Apresentações", "Análise de ROI"],
            experiencia_minima="3-5 anos",
            competencias_desejadas=["Negociação", "Relacionamento", "Orientação a resultados"]
        ),
        VagaCreate(
            titulo="Gerente Comercial",
            descricao="Gestão de equipe de vendas e estratégia comercial.",
            requisitos_tecnicos=["CRM", "Sales Management", "Forecasting", "KPIs"],
            experiencia_minima="7+ anos",
            competencias_desejadas=["Liderança de equipe", "Estratégia", "Coaching"]
        ),
        
        # Produto
        VagaCreate(
            titulo="Product Owner Júnior",
            descricao="Gestão de backlog e priorização de features em squad ágil.",
            requisitos_tecnicos=["Scrum", "Jira", "User Stories", "Roadmap"],
            experiencia_minima="1-2 anos",
            competencias_desejadas=["Organização", "Comunicação", "Visão de produto"]
        ),
        VagaCreate(
            titulo="Product Manager Pleno",
            descricao="Definição de estratégia de produto e roadmap.",
            requisitos_tecnicos=["Product Discovery", "Analytics", "A/B Testing", "SQL", "Roadmapping"],
            experiencia_minima="4-5 anos",
            competencias_desejadas=["Visão estratégica", "Data-driven", "Stakeholder management"]
        ),
        VagaCreate(
            titulo="Head of Product",
            descricao="Liderança de produto e definição de visão estratégica.",
            requisitos_tecnicos=["Product Strategy", "OKRs", "Team Management", "Market Analysis"],
            experiencia_minima="8+ anos",
            competencias_desejadas=["Liderança executiva", "Visão de negócio", "Inovação"]
        ),
        
        # RH
        VagaCreate(
            titulo="Analista de Recrutamento e Seleção",
            descricao="Condução de processos seletivos para vagas de tecnologia.",
            requisitos_tecnicos=["ATS", "LinkedIn Recruiter", "Entrevistas comportamentais", "Testes técnicos"],
            experiencia_minima="2-3 anos",
            competencias_desejadas=["Comunicação", "Empatia", "Organização"]
        ),
        VagaCreate(
            titulo="Business Partner de RH",
            descricao="Parceria estratégica com lideranças e gestão de pessoas.",
            requisitos_tecnicos=["People Analytics", "Performance Management", "Desenvolvimento organizacional"],
            experiencia_minima="5+ anos",
            competencias_desejadas=["Visão estratégica", "Influência", "Resolução de conflitos"]
        ),
        VagaCreate(
            titulo="Coordenador de Cultura e Engajamento",
            descricao="Desenvolvimento de programas de cultura e engajamento de colaboradores.",
            requisitos_tecnicos=["Employee Experience", "Pesquisas de clima", "Eventos corporativos", "Comunicação interna"],
            experiencia_minima="4-5 anos",
            competencias_desejadas=["Criatividade", "Empatia", "Comunicação"]
        ),
        
        # Financeiro
        VagaCreate(
            titulo="Analista Financeiro Júnior",
            descricao="Análise de demonstrativos financeiros e controle de budget.",
            requisitos_tecnicos=["Excel avançado", "Power BI", "Contabilidade básica", "ERP"],
            experiencia_minima="1-2 anos",
            competencias_desejadas=["Atenção aos detalhes", "Organização", "Análise numérica"]
        ),
        VagaCreate(
            titulo="Controller Pleno",
            descricao="Controladoria e análise de performance financeira.",
            requisitos_tecnicos=["Controladoria", "FP&A", "Power BI", "SQL", "ERP SAP"],
            experiencia_minima="5-6 anos",
            competencias_desejadas=["Análise estratégica", "Comunicação executiva", "Visão de negócio"]
        ),
        VagaCreate(
            titulo="CFO - Chief Financial Officer",
            descricao="Liderança financeira e estratégia de investimentos.",
            requisitos_tecnicos=["Financial Strategy", "M&A", "Investor Relations", "Risk Management"],
            experiencia_minima="12+ anos",
            competencias_desejadas=["Liderança executiva", "Visão estratégica", "Negociação"]
        ),
        
        # Operações
        VagaCreate(
            titulo="Analista de Processos",
            descricao="Mapeamento e otimização de processos operacionais.",
            requisitos_tecnicos=["BPMN", "Lean", "Six Sigma", "Automação de processos"],
            experiencia_minima="2-3 anos",
            competencias_desejadas=["Pensamento analítico", "Melhoria contínua", "Documentação"]
        ),
        VagaCreate(
            titulo="Gerente de Operações",
            descricao="Gestão de operações e otimização de eficiência operacional.",
            requisitos_tecnicos=["Operations Management", "KPIs", "Process Improvement", "Project Management"],
            experiencia_minima="6-8 anos",
            competencias_desejadas=["Liderança", "Resolução de problemas", "Gestão de crises"]
        ),
        VagaCreate(
            titulo="Especialista em Customer Success",
            descricao="Gestão de relacionamento com clientes e redução de churn.",
            requisitos_tecnicos=["CRM", "Customer Analytics", "Onboarding", "Health Score"],
            experiencia_minima="3-4 anos",
            competencias_desejadas=["Empatia", "Proatividade", "Orientação ao cliente"]
        ),
    ]
    
    db = SessionLocal()
    try:
        repo = VagaRepository(db)
        
        print(f"\n{'='*80}")
        print(f"POPULANDO BANCO DE DADOS COM {len(vagas)} VAGAS")
        print(f"{'='*80}\n")
        
        for i, vaga_data in enumerate(vagas, 1):
            vaga = repo.criar(vaga_data)
            print(f"✓ [{i:2d}/30] {vaga.titulo} (ID: {vaga.id})")
        
        print(f"\n{'='*80}")
        print(f"✓ {len(vagas)} VAGAS CRIADAS COM SUCESSO!")
        print(f"{'='*80}\n")
        
    finally:
        db.close()

if __name__ == "__main__":
    criar_vagas()
