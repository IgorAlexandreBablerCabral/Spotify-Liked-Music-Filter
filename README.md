O Spotify permite curtir músicas, mas todas ficam em uma lista única e plana. Quem curte centenas ou milhares de músicas perde a capacidade de navegar por gênero. A solução: ler todas as músicas curtidas, identificar os gênero de cada uma através dos artistas, e organizar em playlists separadas por gênero automaticamente.

Documento de Design do Sistema (SDD)

Requisitos Funcionais

ID	Requisito
RF01	Autenticar o usuário via OAuth 2.0 no Spotify
RF02	Ler todas as músicas curtidas (paginando corretamente)
RF03	Para cada música, consultar os gêneros dos artistas
RF04	Classificar cada música por gênero
RF05	Criar uma playlist no Spotify para cada gênero
RF06	Adicionar as músicas nas playlists correspondentes
RF07	Gerar um relatório final com a distribuição

Requisitos Não-Funcionais

ID	Requisito
RNF01	Respeitar os rate limits da API do Spotify
RNF02	Processar até 10.000 músicas curtidas
RNF03	Usuário deve ter interface clara de progresso
RNF04	Código modular e extensível
