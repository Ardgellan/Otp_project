from .base_localized_object import BaseLocalizedObject
from .localized_text_model import LocalizedText


class LocalizedMessageText(BaseLocalizedObject):
    """class with messages localization from localization.json"""

    def __init__(
        self,
    ) -> None:
        super().__init__(entity_type="message")

    @property
    def greetings_message(self) -> LocalizedText:
        return self._get_entity_text("greetings_message")
    
    @property
    def seller_menu_message(self) -> LocalizedText:
        return self._get_entity_text("seller_menu_message")

