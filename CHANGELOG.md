# 📝 Changelog - WhatsApp QR Code Connector

## [1.0.2] - 2024-12-04

### 🔧 Alterado
- **Porta alterada de 8000 para 8010**
  - Motivo: Porta 8000 não estava disponível
  - Arquivos atualizados:
    - `app.py` - Padrão alterado para 8010
    - `.env` - PORT=8010
    - `.env.example` - PORT=8010
    - `docker-compose.yml` - Mapeamento 8010:8010
    - `Dockerfile` - EXPOSE 8010
    - `test_api.py` - BASE_URL atualizada
    - `setup.sh` - Mensagens atualizadas
    - Toda documentação (*.md)

### 📝 Notas
- Nova porta: **8010**
- Acesso local: `http://localhost:8010`
- Sistema 100% funcional

---

## [1.0.1] - 2024-12-04

### ✅ Alterado
- **URL da UazAPI atualizada**: `https://benitechlab.uazapi.com`
  - Anteriormente: `https://free.uazapi.com`
  - Arquivos atualizados:
    - `app.py` - Backend principal
    - `.env` - Configuração pronta
    - `.env.example` - Template
    - `docker-compose.yml` - Docker Compose
    - Toda documentação (*.md)

### 📝 Notas
- Esta URL é específica para o servidor UazAPI do cliente
- Nenhuma outra alteração no código foi necessária
- Sistema continua 100% funcional

---

## [1.0.0] - 2024-12-04

### 🎉 Lançamento Inicial
- Sistema completo de conexão WhatsApp via QR Code
- Conexão via Código de Pareamento
- Interface moderna e responsiva
- API REST completa (5 endpoints)
- Monitoramento automático de conexão
- Docker containerizado
- Scripts de automação (setup.sh, deploy.sh)
- Documentação completa (10 arquivos)
- 17+ exemplos práticos
- Testes automatizados
- Deploy facilitado para Easypanel

### ✨ Features
- ✅ Conexão QR Code
- ✅ Conexão Código de Pareamento
- ✅ Monitoramento a cada 3 segundos
- ✅ Interface responsiva
- ✅ API REST
- ✅ Docker ready
- ✅ Pronto para produção

---

## 🔄 Versionamento

O projeto segue [Semantic Versioning](https://semver.org/):
- **MAJOR** - Mudanças incompatíveis
- **MINOR** - Novas funcionalidades (compatível)
- **PATCH** - Correções de bugs

---

## 📞 Suporte

Para issues ou sugestões, abra um ticket no GitHub.
