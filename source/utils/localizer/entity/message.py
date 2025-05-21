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

    @property
    def request_product_name_message(self) -> LocalizedText:
        return self._get_entity_text("request_product_name_message")

    @property
    def request_product_id_message(self) -> LocalizedText:
        return self._get_entity_text("request_product_id_message")

    @property
    def request_product_otp_message(self) -> LocalizedText:
        return self._get_entity_text("request_product_otp_message")

    @property
    def product_successfully_added_message(self) -> LocalizedText:
        return self._get_entity_text("product_successfully_added_message")

    @property
    def error_adding_product_message(self) -> LocalizedText:
        return self._get_entity_text("error_adding_product_message")

    @property
    def show_seller_products_message(self) -> LocalizedText:
        return self._get_entity_text("show_seller_products_message")

    @property
    def confirm_delete_product_message(self) -> LocalizedText:
        return self._get_entity_text("confirm_delete_product_message")

    @property
    def product_successfully_deleted_message(self) -> LocalizedText:
        return self._get_entity_text("product_successfully_deleted_message")

    @property
    def show_subscription_payment_message(self) -> LocalizedText:
        return self._get_entity_text("show_subscription_payment_message")

    @property
    def payment_confirmation_message(self) -> LocalizedText:
        return self._get_entity_text("payment_confirmation_message")

    @property
    def subscription_status_message(self) -> LocalizedText:
        return self._get_entity_text("subscription_status_message")

    @property
    def subscription_required_message(self) -> LocalizedText:
        return self._get_entity_text("subscription_required_message")



