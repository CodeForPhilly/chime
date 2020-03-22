import dash_core_components as dcc
import dash_bootstrap_components as dbc

row1 = dbc.Row([
    dcc.Markdown("""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
     tempor incididunt ut labore et dolore magna aliqua. Eleifend quam
      adipiscing vitae proin. Blandit cursus risus at ultrices mi tempus
    imperdiet nulla malesuada. Magna etiam tempor orci eu lobortis elementum.
     Dignissim sodales ut eu sem integer vitae. Bibendum arcu vitae elementum
      curabitur vitae nunc sed velit dignissim. Diam quam nulla porttitor massa
       id neque aliquam vestibulum. Egestas diam in arcu cursus. Egestas purus 
       viverra accumsan in nisl nisi scelerisque eu ultrices. Lorem dolor sed 
       viverra ipsum nunc aliquet bibendum. Malesuada bibendum arcu vitae elementum
       """)
])

layout = dbc.Row([
    row1
])
