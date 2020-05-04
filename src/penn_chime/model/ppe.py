"""Personal Protective Equipment."""

import os
from typing import Dict


class PPE:

    def __init__(self, env: Dict[str, str]):
        """__init__."""
        self.assets = assets = env['ASSETS']
        self.filename = filename = "PPE_Calculator_COVID-19.xlsx"
        self.src = os.path.join(assets, filename)
