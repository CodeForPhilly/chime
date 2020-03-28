"""component/footer
appears at the bottom of the page

source text located in app/templates/en/footer.md
"""
from typing import List

from dash.development.base_component import ComponentMeta
from dash_core_components import Markdown

from chime_dash.app.utils.components import Component


class Footer(Component):
    localization_file = "footer.md"

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the header dash html
        """
        return [Markdown(self.content)]
