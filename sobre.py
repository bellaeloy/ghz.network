from pathlib import Path

# CONFIGURAÇÕES
nome = "Isabella Cavalcanti"
email = "isabellaeloy.be@gmail.com"
github = "https://github.com/bellaeloy"
imagem_fundo = "https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/bg_rede.jpg"
orcid = "https://orcid.org/0000-0002-6462-5849"
lattes = "http://lattes.cnpq.br/0165490242445275"

# CONTEÚDO CENTRAL DA PÁGINA "SOBRE"
sobre_html = f"""
<div style="min-height: 100vh;
             background: url('{imagem_fundo}') no-repeat center center fixed;
             background-size: cover;
             display: flex;
             align-items: center;
             justify-content: center;
             font-family: 'Montserrat', sans-serif;
             padding: 60px 20px;">

  <div style="background: rgba(255,255,255,0.94);
              padding: 50px 60px;
              border-radius: 10px;
              text-align: left;
              box-shadow: 0 2px 8px rgba(0,0,0,0.15);
              color: #333;
              max-width: 800px;
              width: 100%;">

    
    <!-- Imagem única ocupando 30% da largura da caixa -->
    <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/img1.png" alt="icone_redeGHZ" style="width: 30%; display: block; margin: 0 auto 15px auto; border-radius: 4px;">

    <h1 style="text-align: center; font-size: 26px; margin-bottom: 25px; font-weight: 700;">Sobre a Rede GHZ</h1>

    <p style="font-size: 15px; line-height: 1.6; color: #444; margin-bottom: 18px;">
      A <strong>Rede GHZ</strong> é um dos resultados de uma pesquisa de doutorado desenvolvida no 
      Programa de Pós-Graduação do Instituto de Arquitetura e Urbanismo da Universidade de São Paulo (IAU-USP), 
      na área de <strong>Arquitetura, Urbanismo e Tecnologia</strong>.
    </p>

    <p style="font-size: 15px; line-height: 1.6; color: #444; margin-bottom: 18px;">
      Intitulada <em>“Governança coletiva de dados: modelagem horizontal da informação para formulação de políticas públicas urbanas”</em>, 
      a pesquisa, desenvolvida entre <strong>2022 e 2026</strong>, integra o grupo de pesquisa <strong>Nomads.usp</strong> e é orientada pelo 
      Prof. Dr. Marcelo Tramontano.
    </p>

    <p style="font-size: 15px; line-height: 1.6; color: #444; margin-bottom: 18px;">
      Este site constitui uma das plataformas experimentais do projeto e tem como propósito apoiar a investigação sobre 
      <strong>novos modos de interação e integração entre agentes sociais</strong>, visando a uma 
      modelagem de dados mais horizontalizada. O foco da pesquisa recai sobre o 
      espaço urbano, com ênfase nos <strong>processos de formulação de políticas públicas</strong>.
    </p>

    <p style="font-size: 15px; line-height: 1.6; color: #444; margin-bottom: 18px;">
      Articulando as ciências sociais aplicadas e a ciência da computação, adotamos uma 
      <strong>abordagem sistêmica</strong> para identificar e analisar as conexões existentes entre agentes que atuam em 
      <strong>territórios e com grupos sociais</strong>, mobilizando-os pela defesa de suas pautas por meio de <strong>ferramentas digitais</strong>.
    </p>

    <p style="font-size: 15px; line-height: 1.6; color: #444; margin-bottom: 18px;">
      Com base em uma <strong>pesquisa documental</strong>, construímos um banco de dados que reúne informações sobre esses 
      agentes e suas inter-relações. A partir da modelagem de uma rede complexa e da geração de medidas de rede, 
      buscamos compreender, sob uma <strong>perspectiva decolonial e urbanística</strong>, as dinâmicas dessas interações, não apenas para 
      interpretar a realidade observada, mas também para propor <strong>novos caminhos de fortalecimento dos sistemas de colaboração e da 
      construção coletiva da informação</strong>.
    </p>

    <h2 style="text-align: center; font-size: 20px; margin: 35px 0 15px;">Objetivo Geral da Pesquisa</h2>

    <blockquote style="font-size: 15px; line-height: 1.6; color: #333; font-style: italic; border-left: 4px solid #0066cc; padding-left: 15px; margin-bottom: 35px;">
      Explorar como a abertura da governança de dados à coletividade pode contribuir para a construção de um 
      embasamento informacional mais justo, equitativo e participativo na formulação de 
      políticas públicas urbanas.
    </blockquote>

    <hr style="border: none; border-top: 1px solid #ccc; margin: 40px 0;">

    <!-- Imagem única ocupando 30% da largura da caixa -->
    <img src="https://raw.githubusercontent.com/bellaeloy/ghz.network/main/imagens/img1.png" alt="icone_contato" style="width: 30%; display: block; margin: 0 auto 15px auto; border-radius: 4px;">


    <h2 style="text-align: center; font-size: 20px; margin-bottom: 20px;">Contato</h2>

    <div style="text-align: center;">
      <strong style="font-size: 18px; display: block; margin-bottom: 10px;">{nome}</strong>
      <p style="font-size: 15px; color: #555; margin-bottom: 25px;">Pesquisadora e desenvolvedora da Rede GHZ</p>
      <p><strong>E-mail:</strong> <a href="mailto:{email}" style="color: #0066cc; text-decoration: none;">{email}</a></p>
      <p><strong>GitHub:</strong> <a href="{github}" target="_blank" style="color: #0066cc; text-decoration: none;">{github}</a></p>
      <p><strong>Orcid:</strong> <a href="{orcid}" target="_blank" style="color: #0066cc; text-decoration: none;">{orcid}</a></p>
      <p><strong>Lattes:</strong> <a href="{lattes}" target="_blank" style="color: #0066cc; text-decoration: none;">{lattes}</a></p>
    </div>

  </div>
</div>
"""

# CARREGAR HEADER E FOOTER
header_html = Path("header.html").read_text(encoding="utf-8") if Path("header.html").exists() else ""
footer_html = Path("footer.html").read_text(encoding="utf-8") if Path("footer.html").exists() else ""

# MONTAR HTML FINAL
html_final = f"""
{header_html}
{sobre_html}
{footer_html}
"""

# SALVAR COMO sobre.html
Path("sobre.html").write_text(html_final, encoding="utf-8")

print("Página 'sobre.html' criada!")
