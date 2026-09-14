Spotify lets you like songs, but they all end up in a single, flat list. If you like hundreds or thousands of songs, you lose the ability to navigate by genre. The solution: read all the liked songs, identify the genres of each through the artists, and automatically organize them into playlists separated by genre.

System Design Document (SDD)

Functional Requirements

ID Requirement RF01 Authenticate the user via OAuth 2.0 on Spotify RF02 Read all liked songs (paged correctly) RF03 For each song, check the genres of the artists RF04 Categorize each song by genre RF05 Create a playlist on Spotify for each genre RF06 Add the songs to the corresponding playlists RF07 Generate a final report with the distribution

Non-Functional Requirements

ID Requirement RNF01 Respect Spotify API rate limits RNF02 Process up to 10,000 liked songs RNF03 User should have a clear progress interface RNF04 Modular and extensible code

------------------------------------------------------------------------------------------------------------------------
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
