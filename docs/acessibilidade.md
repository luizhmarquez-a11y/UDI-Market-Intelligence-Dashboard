# Acessibilidade da edição Beta 1.0

**Estado:** avaliação parcial, não certificada em WCAG. Referência: [WCAG 2.2](https://www.w3.org/TR/WCAG22/). O objetivo é melhorar o acesso sem alterar a identidade visual V14 ou os valores.

## Recursos existentes no painel

- Idioma português do Brasil; regiões semânticas de navegação, cabeçalho e conteúdo principal.
- Filtros com rótulos associados, estados de navegação e menu móvel anunciados, descrição textual do gráfico anual e foco visível nos controles.
- Preferência por movimento reduzido reconhecida na interface, e navegação com transferência de foco ao conteúdo.
- Interface responsiva testada no Chromium em 1440, 390 e 320 px; 21 cenários aprovados em 24/11/2026.
- Exportações CSV/HTML e dados documentais consultáveis em texto, sem depender exclusivamente dos gráficos.

## Ajustes da apresentação — 27/11/2026

O README mantém as imagens estáticas e seus textos alternativos. O GIF fica visível inicialmente no README, em seção expansível que pode ser fechada pelo leitor para ocultar a animação. Na galeria do GIF, a seção permanece fechada inicialmente. O vídeo não inicia automaticamente, e ganhou [alternativa textual](../assets/videos/README.md). Nenhum arquivo de mídia ou HTML do dashboard foi alterado nesta etapa.

## Limites

Em 27/11/2026, a edição distribuída (mesmo SHA-256 registrado em [registro da edição](registro-edicao.md)) passou por uma avaliação automatizada com axe-core 4.10.3:

| Verificação | Resultado |
|---|---|
| Sete páginas × duas larguras (1440 e 390 px) | 14 cenários |
| Violações confirmadas | 0 |
| Ocorrências de regras incompletas | 18 (14 de contraste e 4 de distinção de links) |
| Transbordamento horizontal | 0 nos cenários |
| Navegação por Enter e foco após troca de página | Funcionaram nos controles testados |
| Alteração de filtro pelo teclado | Valor alterado; foco não permaneceu no controle |

A ausência de violações confirmadas não significa conformidade integral. Testes físicos, leitores de tela, contraste em todos os estados, retenção de foco, ampliação e navegação exclusivamente por teclado ainda requerem avaliação complementar.

[Voltar à apresentação](../README.md)
