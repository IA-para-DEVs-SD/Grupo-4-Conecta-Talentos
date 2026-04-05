"""Script para verificar currículos no banco de dados."""
import sqlite3

# Conecta ao banco
conn = sqlite3.connect('data/database.db')
cursor = conn.cursor()

# Busca currículos
cursor.execute("""
    SELECT 
        id, 
        vaga_id, 
        nome_arquivo, 
        LENGTH(texto_extraido) as tamanho_texto,
        SUBSTR(texto_extraido, 1, 100) as preview_texto,
        status,
        enviado_em
    FROM curriculos
    ORDER BY id
""")

curriculos = cursor.fetchall()

print(f"\n{'='*80}")
print(f"CURRÍCULOS NO BANCO DE DADOS ({len(curriculos)} encontrados)")
print(f"{'='*80}\n")

for curr in curriculos:
    id_curr, vaga_id, nome, tamanho, preview, status, enviado = curr
    print(f"ID: {id_curr}")
    print(f"Vaga ID: {vaga_id}")
    print(f"Nome: {nome}")
    print(f"Tamanho do texto: {tamanho if tamanho else 'NULL (sem texto)'}")
    print(f"Status: {status}")
    print(f"Enviado em: {enviado}")
    if preview:
        print(f"Preview: {preview[:80]}...")
    else:
        print("Preview: (sem texto extraído)")
    print(f"{'-'*80}\n")

conn.close()
