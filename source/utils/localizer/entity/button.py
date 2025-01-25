from .base_localized_object import BaseLocalizedObject
from .localized_text_model import LocalizedText


class LocalizedButtonText(BaseLocalizedObject):
    """class with buttons localization from localization.json"""

    def __init__(
        self,
    ) -> None:
        super().__init__(entity_type="button")

    @property
    def main_menu(self) -> LocalizedText:
        return self._get_entity_text("main_menu")

