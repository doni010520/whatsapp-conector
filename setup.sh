#!/bin/bash

# 🎯 Setup Inicial - WhatsApp QR Code Connector
# Este script configura tudo automaticamente

clear
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🚀 Setup Inicial - WhatsApp QR Code Connector             ║"
echo "║  Configuração automática para deploy no Easypanel          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Função para imprimir com cor
print_step() {
    echo -e "${CYAN}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar se Git está instalado
print_step "Verificando Git..."
if ! command -v git &> /dev/null; then
    print_error "Git não está instalado!"
    echo ""
    echo "Instale o Git:"
    echo "  • Windows: https://git-scm.com/download/win"
    echo "  • Mac: brew install git"
    echo "  • Linux: sudo apt install git"
    exit 1
fi
print_success "Git encontrado: $(git --version)"
echo ""

# Verificar se Python está instalado
print_step "Verificando Python..."
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    print_error "Python não está instalado!"
    echo ""
    echo "Instale o Python 3.8+:"
    echo "  • Windows/Mac: https://www.python.org/downloads/"
    echo "  • Linux: sudo apt install python3 python3-pip"
    exit 1
fi

if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    PIP_CMD=pip3
else
    PYTHON_CMD=python
    PIP_CMD=pip
fi

PYTHON_VERSION=$($PYTHON_CMD --version)
print_success "Python encontrado: $PYTHON_VERSION"
echo ""

# Verificar se Docker está instalado (opcional)
print_step "Verificando Docker (opcional)..."
if command -v docker &> /dev/null; then
    print_success "Docker encontrado: $(docker --version)"
else
    print_warning "Docker não encontrado (opcional para desenvolvimento local)"
fi
echo ""

# Criar .env se não existir
print_step "Configurando variáveis de ambiente..."
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        print_success "Arquivo .env criado a partir do .env.example"
    else
        print_warning ".env.example não encontrado"
    fi
else
    print_success "Arquivo .env já existe"
fi
echo ""

# Instalar dependências
print_step "Instalando dependências Python..."
if [ -f requirements.txt ]; then
    $PIP_CMD install -r requirements.txt
    if [ $? -eq 0 ]; then
        print_success "Dependências instaladas com sucesso!"
    else
        print_error "Erro ao instalar dependências"
        exit 1
    fi
else
    print_error "requirements.txt não encontrado!"
    exit 1
fi
echo ""

# Inicializar Git se necessário
print_step "Configurando Git..."
if [ ! -d .git ]; then
    git init
    print_success "Repositório Git inicializado"
else
    print_success "Repositório Git já existe"
fi
echo ""

# Configurar usuário Git se necessário
GIT_USER=$(git config --global user.name)
if [ -z "$GIT_USER" ]; then
    print_warning "Git user.name não configurado"
    read -p "Digite seu nome para o Git: " USER_NAME
    git config --global user.name "$USER_NAME"
    print_success "Git user.name configurado"
fi

GIT_EMAIL=$(git config --global user.email)
if [ -z "$GIT_EMAIL" ]; then
    print_warning "Git user.email não configurado"
    read -p "Digite seu email para o Git: " USER_EMAIL
    git config --global user.email "$USER_EMAIL"
    print_success "Git user.email configurado"
fi
echo ""

# Perguntar sobre repositório GitHub
print_step "Configuração do GitHub..."
if ! git remote | grep -q origin; then
    echo ""
    echo -e "${BLUE}┌────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${BLUE}│ Você precisa criar um repositório no GitHub:              │${NC}"
    echo -e "${BLUE}│                                                            │${NC}"
    echo -e "${BLUE}│ 1. Acesse: https://github.com/new                         │${NC}"
    echo -e "${BLUE}│ 2. Nomeie: whatsapp-qr-connector                          │${NC}"
    echo -e "${BLUE}│ 3. Deixe público ou privado (sua escolha)                 │${NC}"
    echo -e "${BLUE}│ 4. NÃO inicialize com README                              │${NC}"
    echo -e "${BLUE}│ 5. Copie a URL do repositório                             │${NC}"
    echo -e "${BLUE}└────────────────────────────────────────────────────────────┘${NC}"
    echo ""
    read -p "Já criou o repositório? (s/n): " REPO_CREATED
    
    if [ "$REPO_CREATED" = "s" ] || [ "$REPO_CREATED" = "S" ]; then
        echo ""
        echo "Exemplo de URL:"
        echo "  https://github.com/seu-usuario/whatsapp-qr-connector.git"
        echo ""
        read -p "Cole a URL do repositório: " REPO_URL
        
        if [ ! -z "$REPO_URL" ]; then
            git remote add origin "$REPO_URL"
            print_success "Repositório remoto configurado!"
        else
            print_warning "URL não fornecida. Configure manualmente depois:"
            echo "  git remote add origin SUA-URL"
        fi
    else
        print_warning "Configure o repositório depois com:"
        echo "  git remote add origin SUA-URL"
    fi
else
    REMOTE_URL=$(git remote get-url origin)
    print_success "Repositório remoto já configurado: $REMOTE_URL"
fi
echo ""

# Tornar script de deploy executável
print_step "Configurando permissões de scripts..."
if [ -f deploy.sh ]; then
    chmod +x deploy.sh
    print_success "deploy.sh está executável"
fi
echo ""

# Teste rápido
print_step "Testando configuração..."
if $PYTHON_CMD -c "import fastapi, uvicorn, httpx, pydantic" 2>/dev/null; then
    print_success "Todas as dependências estão instaladas!"
else
    print_error "Algumas dependências estão faltando"
    echo "Execute: $PIP_CMD install -r requirements.txt"
fi
echo ""

# Resumo
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ Setup Concluído!                                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}🎉 Tudo pronto para começar!${NC}"
echo ""
echo "📋 Próximos passos:"
echo ""
echo "  1️⃣  Testar localmente:"
echo "     ${CYAN}$PYTHON_CMD app.py${NC}"
echo "     Acesse: http://localhost:8010"
echo ""
echo "  2️⃣  Fazer primeiro commit:"
echo "     ${CYAN}git add .${NC}"
echo "     ${CYAN}git commit -m \"🎉 Initial commit\"${NC}"
echo ""
echo "  3️⃣  Enviar para GitHub:"
echo "     ${CYAN}git branch -M main${NC}"
echo "     ${CYAN}git push -u origin main${NC}"
echo ""
echo "  4️⃣  Deploy no Easypanel:"
echo "     • Acesse seu Easypanel"
echo "     • Create New App → GitHub"
echo "     • Selecione o repositório"
echo "     • Configure e deploy"
echo ""
echo "📚 Documentação:"
echo "  • DEPLOY.md    - Guia completo de deploy"
echo "  • COMANDOS.md  - Comandos rápidos"
echo "  • README.md    - Documentação geral"
echo ""
echo "🚀 Atalhos úteis:"
echo "  • Deploy rápido: ${CYAN}./deploy.sh${NC}"
echo "  • Testar API: ${CYAN}$PYTHON_CMD test_api.py${NC}"
echo "  • Docker local: ${CYAN}docker-compose up${NC}"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo -e "${BLUE}💡 Dica:${NC} Use ${CYAN}./deploy.sh${NC} sempre que quiser enviar mudanças!"
echo ""
