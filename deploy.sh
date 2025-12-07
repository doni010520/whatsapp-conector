#!/bin/bash

# 🚀 Script de Deploy - WhatsApp QR Code Connector
# Este script facilita o push para GitHub

echo "🚀 Deploy para GitHub - WhatsApp QR Code Connector"
echo "=================================================="
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar se Git está instalado
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git não está instalado!${NC}"
    echo "Instale o Git primeiro: https://git-scm.com/downloads"
    exit 1
fi

# Verificar se já é um repositório Git
if [ ! -d .git ]; then
    echo -e "${YELLOW}📦 Inicializando repositório Git...${NC}"
    git init
    echo -e "${GREEN}✅ Git inicializado!${NC}"
    echo ""
fi

# Verificar se há remote configurado
if ! git remote | grep -q origin; then
    echo -e "${YELLOW}🔗 Configure o repositório remoto do GitHub:${NC}"
    echo ""
    echo "Exemplo:"
    echo "  https://github.com/seu-usuario/whatsapp-qr-connector.git"
    echo ""
    read -p "Cole a URL do seu repositório GitHub: " REPO_URL
    
    if [ -z "$REPO_URL" ]; then
        echo -e "${RED}❌ URL não fornecida!${NC}"
        exit 1
    fi
    
    git remote add origin "$REPO_URL"
    echo -e "${GREEN}✅ Remote configurado!${NC}"
    echo ""
fi

# Mostrar status
echo -e "${YELLOW}📊 Status do repositório:${NC}"
git status
echo ""

# Confirmar commit
read -p "📝 Digite a mensagem do commit (ou Enter para usar padrão): " COMMIT_MSG

if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="🔄 Update $(date '+%Y-%m-%d %H:%M:%S')"
fi

# Adicionar todos os arquivos
echo -e "${YELLOW}📦 Adicionando arquivos...${NC}"
git add .

# Fazer commit
echo -e "${YELLOW}💾 Fazendo commit...${NC}"
git commit -m "$COMMIT_MSG"

# Verificar se há mudanças para commitar
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Nenhuma mudança para commitar${NC}"
    read -p "Deseja fazer push mesmo assim? (s/n): " FORCE_PUSH
    if [ "$FORCE_PUSH" != "s" ]; then
        echo -e "${YELLOW}Operação cancelada${NC}"
        exit 0
    fi
fi

# Definir branch principal
BRANCH=$(git branch --show-current)
if [ -z "$BRANCH" ]; then
    BRANCH="main"
    git branch -M main
fi

# Push para GitHub
echo -e "${YELLOW}🚀 Enviando para GitHub (branch: $BRANCH)...${NC}"
git push -u origin "$BRANCH"

# Verificar resultado
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Deploy para GitHub concluído com sucesso!${NC}"
    echo ""
    echo "🌐 Próximos passos:"
    echo "  1. Acesse seu Easypanel"
    echo "  2. Crie um novo App"
    echo "  3. Conecte ao repositório GitHub"
    echo "  4. Configure e faça deploy"
    echo ""
    echo "📖 Consulte DEPLOY.md para mais detalhes"
else
    echo ""
    echo -e "${RED}❌ Erro ao fazer push para GitHub${NC}"
    echo ""
    echo "Possíveis soluções:"
    echo "  1. Verifique suas credenciais do GitHub"
    echo "  2. Configure SSH ou Personal Access Token"
    echo "  3. Verifique se a URL do repositório está correta"
    echo ""
    echo "Mais informações: https://docs.github.com/en/authentication"
fi
