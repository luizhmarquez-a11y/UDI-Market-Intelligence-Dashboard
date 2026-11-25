# Hospedagem privada — avaliação Beta 1.0

**Estado:** preparação; nenhuma implantação realizada ou URL ativa confirmada. Não alterar a visibilidade do repositório.

## Proposta

Vercel Authentication com proteção de **All Deployments**, inclusive produção, conforme a [atualização oficial de 9 de setembro de 2026](https://vercel.com/changelog/protect-production-deployments-for-free-on-every-plan). A plataforma disponibiliza autenticação em todos os planos; conferir limites de convidados na conta e manter acesso nominal. Não contratar plano pago sem autorização.

## Ordem obrigatória

1. Conectar a conta de hospedagem, autorizar apenas o necessário. Criar projeto sem conteúdo do painel, sem importação automática do GitHub original.
2. Habilitar Vercel Authentication em All Deployments antes de enviar o painel. Não usar exceções, links com bypass ou credenciais no README. Confirmar proteção em ambiente vazio e testar sem sessão. Se não puder configurar antes do envio, não implantar.
3. Implantar somente docs/index.html (blob Git 471cbdf7e0dac91add593b06c21976efb7c25404, SHA-256 7598e5cc21e8d897906acef26ba391da5050b8bb21418a6e6d949736937dd239) e docs/PAINEL-LICENSE.txt. Não enviar Git, documentação interna, dados brutos nem scripts de processamento. Não incorporar senha no JavaScript.
4. Confirmar que todos os URLs, incluindo aliases, produção, preview e index.html, negam acesso anônimo sem entregar o HTML. Conferir a resposta autenticada e testar navegação, busca, filtros e exportação. Se houver exposição, retirar o deploy.
5. Conceder acesso individual à avaliadora por sua conta Vercel. Confirmar a experiência após login e permitir revogação posterior.
6. Somente após esses controles, atualizar o README com o link verificado e instruções de login.

O conteúdo entregue ao navegador de uma pessoa autenticada pode ser inspecionado e copiado; o controle de acesso não é DRM. O repositório original e o de demonstração permanecem privados. GitHub Pages público não faz parte desta etapa.

Referências: [Vercel Authentication](https://vercel.com/docs/deployment-protection/methods-to-protect-deployments/vercel-authentication), [compartilhamento](https://vercel.com/docs/deployments/sharing-deployments).
