"""Script para verificar status da conta OpenAI."""
import os
from openai import OpenAI
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ OPENAI_API_KEY não encontrada no .env")
    exit(1)

print(f"✓ API Key encontrada: {api_key[:20]}...{api_key[-4:]}")
print()

# Testa conexão básica
try:
    client = OpenAI(api_key=api_key)
    print("✓ Cliente OpenAI criado com sucesso")
    print()
    
    # Tenta fazer uma chamada simples
    print("Testando chamada à API...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Responda apenas: OK"}
        ],
        max_tokens=10
    )
    
    print(f"✓ Resposta recebida: {response.choices[0].message.content}")
    print(f"✓ Tokens usados: {response.usage.total_tokens}")
    print()
    print("🎉 Sua conta OpenAI está funcionando!")
    print()
    
except Exception as e:
    error_msg = str(e)
    print(f"❌ Erro ao chamar API: {error_msg}")
    print()
    
    if "insufficient_quota" in error_msg.lower() or "quota" in error_msg.lower():
        print("💳 PROBLEMA: Sem créditos na conta OpenAI")
        print()
        print("Para adicionar créditos:")
        print("1. Acesse: https://platform.openai.com/account/billing/overview")
        print("2. Clique em 'Add payment method' ou 'Add credits'")
        print("3. Adicione um método de pagamento ou compre créditos")
        print()
        print("Nota: Contas gratuitas têm limite de uso. Pode ser necessário upgrade.")
        
    elif "invalid_api_key" in error_msg.lower():
        print("🔑 PROBLEMA: API Key inválida")
        print()
        print("Verifique sua chave em:")
        print("https://platform.openai.com/api-keys")
        
    elif "rate_limit" in error_msg.lower():
        print("⏱️ PROBLEMA: Limite de taxa excedido")
        print()
        print("Aguarde alguns minutos e tente novamente.")
        
    else:
        print("Erro desconhecido. Verifique:")
        print("- Conexão com internet")
        print("- Status da OpenAI: https://status.openai.com/")
