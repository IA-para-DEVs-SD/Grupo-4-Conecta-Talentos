# Script para criar PR via API do GitHub

# Configurações
$owner = "IA-para-DEVs-SD"
$repo = "Grupo-4-Conecta-Talentos"
$head = "feature/logging-error-handling"
$base = "develop"
$title = "feat: Sistema de Logging e Tratamento de Erros (Issue #64)"

$body = @"
## Descrição

Implementa sistema completo de logging e tratamento de erros para o ConectaTalentos, conforme Issue #64 (Requisito 10).

## Alterações Principais

### 1. Sistema de Logging Centralizado (\`app/logging_config.py\`)
- Logs estruturados para arquivo (\`logs/conecta_talentos.log\`)
- Logs de erros separados (\`logs/errors.log\`)
- Logs para console com formatação simplificada
- Função \`get_logger(__name__)\` para obter loggers configurados
- Função \`log_exception()\` para registrar exceções com contexto adicional
- Silenciamento de logs verbosos de bibliotecas externas

### 2. Hierarquia Completa de Exceções (\`app/processors/exceptions.py\`)
- \`ConectaTalentosError\` - Exceção base do sistema
- **Exceções de PDF**: \`PDFError\`, \`PDFCorromidoError\`, \`PDFMuitoGrandeError\`, \`PDFVazioError\`, \`PDFFormatoInvalidoError\`
- **Exceções de Upload**: \`UploadError\`, \`ArquivoNaoEncontradoError\`, \`TipoArquivoInvalidoError\`, \`TamanhoArquivoExcedidoError\`
- **Exceções de Anonimização**: \`AnonimizacaoError\`, \`PresidioIndisponivelError\`, \`ModeloNLPNaoEncontradoError\`
- **Exceções de LLM**: Expandidas com \`LLMRespostaInvalidaError\`
- **Exceções de Banco de Dados**: \`DatabaseError\`, \`RegistroNaoEncontradoError\`, \`ViolacaoIntegridadeError\`
- **Exceções de Validação**: \`ValidationError\`, \`CampoObrigatorioError\`, \`ValorInvalidoError\`

### 3. Middleware de Tratamento de Erros (\`app/middleware/error_handler.py\`)
- \`ErrorHandlerMiddleware\` para captura global de exceções
- Tratamento específico para cada tipo de erro com mensagens claras
- Respostas JSON estruturadas com códigos HTTP apropriados
- Logging automático de todas as exceções com contexto
- Tratamento especial para erros de anonimização (não-críticos)

### 4. Integração no FastAPI (\`app/main.py\`)
- Configuração automática de logging no startup
- Middleware de erros como primeiro na cadeia
- Logs de inicialização e encerramento da aplicação

## Requisitos Atendidos (Issue #64)

✅ **Task 1**: Tratamento de erros de PDF com mensagens específicas  
✅ **Task 2**: Tratamento de erros de anonimização (não-crítico, continua processamento)  
✅ **Task 3**: Tratamento de erros de LLM/IA (timeout, rate limit, API errors)  
✅ **Task 4**: Tratamento de erros de upload com validações  
✅ **Task 5**: Sistema de logging estruturado com arquivos separados  

## Testes

- [ ] Testes unitários para exceções (próximo commit)
- [ ] Testes de integração para middleware (próximo commit)
- [ ] Testes de logging (próximo commit)

## Checklist

- [x] Código segue padrões do projeto
- [x] Mensagens de commit seguem conventional commits
- [x] Documentação inline (docstrings) completa
- [x] Exceções com contexto adicional quando necessário
- [ ] Testes implementados (próximo commit)
- [x] Sem warnings do Ruff

## Relacionado

Closes #46, #47, #48, #49, #50  
Parte da Issue #64
"@

# Tenta obter token do git credential helper
Write-Host "Obtendo credenciais do GitHub..." -ForegroundColor Cyan

try {
    # Tenta usar o token do git credential helper
    $gitConfig = git config --get credential.helper
    
    if ($gitConfig) {
        Write-Host "Git credential helper encontrado: $gitConfig" -ForegroundColor Green
        
        # Tenta obter o token via git credential fill
        $credInput = "protocol=https`nhost=github.com`n`n"
        $cred = $credInput | git credential fill 2>$null
        
        if ($cred -match "password=(.+)") {
            $token = $matches[1]
            Write-Host "Token obtido com sucesso!" -ForegroundColor Green
        }
    }
    
    # Se não conseguiu obter o token, pede ao usuário
    if (-not $token) {
        Write-Host "`nNão foi possível obter o token automaticamente." -ForegroundColor Yellow
        Write-Host "Por favor, forneça um Personal Access Token do GitHub." -ForegroundColor Yellow
        Write-Host "Você pode criar um em: https://github.com/settings/tokens" -ForegroundColor Cyan
        Write-Host "Permissões necessárias: repo (Full control of private repositories)" -ForegroundColor Cyan
        $token = Read-Host "`nToken do GitHub"
    }
    
    if (-not $token) {
        Write-Host "Token não fornecido. Abortando." -ForegroundColor Red
        exit 1
    }
    
    # Cria o payload JSON
    $payload = @{
        title = $title
        body = $body
        head = $head
        base = $base
    } | ConvertTo-Json
    
    # Headers para autenticação
    $headers = @{
        "Authorization" = "Bearer $token"
        "Accept" = "application/vnd.github+json"
        "X-GitHub-Api-Version" = "2022-11-28"
    }
    
    # URL da API
    $url = "https://api.github.com/repos/$owner/$repo/pulls"
    
    Write-Host "`nCriando Pull Request..." -ForegroundColor Cyan
    Write-Host "Repositório: $owner/$repo" -ForegroundColor Gray
    Write-Host "Base: $base <- Head: $head" -ForegroundColor Gray
    
    # Faz a requisição
    $response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $payload -ContentType "application/json"
    
    Write-Host "`n✅ Pull Request criado com sucesso!" -ForegroundColor Green
    Write-Host "Número: #$($response.number)" -ForegroundColor Cyan
    Write-Host "URL: $($response.html_url)" -ForegroundColor Cyan
    Write-Host "Título: $($response.title)" -ForegroundColor Gray
    
} catch {
    Write-Host "`n❌ Erro ao criar Pull Request:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "`nDetalhes do erro:" -ForegroundColor Yellow
        Write-Host $responseBody -ForegroundColor Gray
    }
    
    exit 1
}
