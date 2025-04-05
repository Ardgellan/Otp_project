from .base_localized_object import BaseLocalizedObject
from .localized_text_model import LocalizedText


class LocalizedButtonText(BaseLocalizedObject):
    """class with buttons localization from localization.json"""

    def __init__(
        self,
    ) -> None:
        super().__init__(entity_type="button")

    @property
    def main_menu_button(self) -> LocalizedText:
        return self._get_entity_text("main_menu_button")

    @property
    def seller_button(self) -> LocalizedText:
        return self._get_entity_text("seller_button")

    @property
    def buyer_button(self) -> LocalizedText:
        return self._get_entity_text("buyer_button")

