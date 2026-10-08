# IAAC — classificação de ataques cibernéticos

**Autor desta componente:** Guilherme Jesus

**Turma:** 2.º Ciber

Este repositório contém a minha componente individual do dataset de tráfego. Classifica registos como Normal, DDoS, PortScan ou BruteForce. As restantes áreas e datasets do grupo não estão incluídos.

## Por onde começar

1. Usa `docs/GUIA_SIMPLES.md` para executar o script e compreender a comparação.
2. Consulta `docs/RESULTADOS.md` para métricas, gráficos e limitações.
3. O planeamento e o âmbito estão em `docs/BACKLOG.md`, `docs/SPRINTS.md` e `docs/MACHINE_LEARNING_CANVAS.md`.
4. `docs/RELATORIO_PESSOAL.md` apresenta o relatório desta componente.

## Resultado principal

O Random Forest obteve macro-F1 CV de 1,0000 e métricas perfeitas no teste retido. Como alguns atributos têm relações quase determinísticas com os rótulos, estes números não demonstram generalização para tráfego real. O modelo não é uma ferramenta de defesa validada.

## Executar no Windows

Na pasta raiz do projeto:

```powershell
.\.venv\Scripts\python.exe iaac_minimum_apply.py
```

O script também aceita o caminho para um CSV como primeiro argumento. O modelo, o resumo JSON e os gráficos são guardados em `resultados/`.
