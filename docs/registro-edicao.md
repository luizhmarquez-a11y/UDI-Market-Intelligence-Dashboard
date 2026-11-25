# Registro da edição candidata — Beta 1.0

**Data:** 24/11/2026. **Estado:** preparação privada, não publicada.

A edição estática em `docs/index.html` deriva do candidato de desenvolvimento auditado em 24/11/2026 (commit de origem `9431dc5`; SHA-256 do HTML de origem: `073991a2db0bc43d16bb57ba410aa611d0b4fe4d3c92d7d0856576242178c346`). Os indicadores quantitativos e eventos são preservados. A edição de portfólio corrige exclusivamente a descrição de Q05, a nota de obtenção dos pilotos e o crédito de autoria do rodapé; não altera CSS, layout, navegação, cálculos ou valores. Hash SHA-256 da edição de portfólio: `7598e5cc21e8d897906acef26ba391da5050b8bb21418a6e6d949736937dd239`. Blob Git: `471cbdf7e0dac91add593b06c21976efb7c25404`. A reprodução independente da edição confirmou identidade exata do blob, CSS inalterado e igualdade dos indicadores, eventos, taxonomia, cobertura e extratos históricos com a origem. A execução de navegador própria está sendo verificada separadamente.

## Superfície disponibilizável

`docs/index.html`: interface estática autônoma, com CSS, JavaScript e dados documentais embutidos; `docs/.nojekyll`: entrega sem transformação Jekyll; `docs/PAINEL-LICENSE.txt`: licença do software. Os demais arquivos Markdown em docs contêm documentação de apresentação. Nenhum ETL, arquivo bruto, API key ou aplicação Streamlit integra o site. A inspeção estática da edição não detectou padrões usuais de CPF, CNPJ formatado, e-mail, token ou chave privada. Não é certificação jurídica ou teste de intrusão.

## Evidência e limites

25 P2, 38 acontecimentos, 29 extratos históricos, 7 alertas, 82 recortes catalogados e nenhuma série P4. Cadastur e CNES: arquivos candidatos obtidos, recortes não homologados. ANEEL: aquisição não confirmada. O catálogo conserva links de investigação, cuja disponibilidade e licença específicas podem mudar; não republica os arquivos de terceiros. A etapa de revisão independente de direitos, contraste, leitores de tela, dispositivos físicos e validação HTTPS pública permanece aberta.

## Aprovação de publicação

A aprovação não deve ser confundida com a preparação. Antes de abrir este repositório, revisar todos os arquivos versionados, inclusive o histórico e branches de QA; reconhecer a visibilidade do front-end e de seus dados incorporados; confirmar as limitações metodológicas, os direitos de terceiros e a revisão das mídias. A interface não é um produto financeiro, não consulta dados ao vivo e não está certificada para WCAG. Não publicar dados brutos, identificadores individuais ou arquivos internos.

## Ativação

Somente após aprovação do responsável: tornar **este** repositório público; em Settings → Pages escolher Deploy from a branch, main, /docs; salvar; confirmar o endereço divulgado e testar anonimamente. GitHub Pages pode expor um site mesmo com repositório privado, por isso nenhuma configuração de hospedagem deve ser ativada antes da autorização. O repositório de desenvolvimento deve permanecer privado.

Endereço previsto: https://luizhmarquez-a11y.github.io/UDI-Market-Intelligence-Dashboard/

[Voltar ao README](../README.md)
