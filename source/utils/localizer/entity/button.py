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

    @property
    def trial_period_button(self) -> LocalizedText:
        return self._get_entity_text("trial_period_button")

    @property
    def subscription_button(self) -> LocalizedText:
        return self._get_entity_text("subscription_button")

    @property
    def status_subscription_button(self) -> LocalizedText:
        return self._get_entity_text("status_subscription_button")

    @property
    def my_products_button(self) -> LocalizedText:
        return self._get_entity_text("my_products_button")

    @property
    def add_product_button(self) -> LocalizedText:
        return self._get_entity_text("add_product_button")

    @property
    def edit_product_button(self) -> LocalizedText:
        return self._get_entity_text("edit_product_button")

    @property
    def delete_product_button(self) -> LocalizedText:
        return self._get_entity_text("delete_product_button")

    @property
    def confirm_delete_button(self) -> LocalizedText:
        return self._get_entity_text("confirm_delete_button")

    @property
    def pay_one_thousand_rubles_button(self) -> LocalizedText:
        return self._get_entity_text("pay_one_thousand_rubles_button")

    @property
    def pay_two_thousand_rubles_button(self) -> LocalizedText:
        return self._get_entity_text("pay_two_thousand_rubles_button")

    @property
    def pay_three_thousand_rubles_button(self) -> LocalizedText:
        return self._get_entity_text("pay_three_thousand_rubles_button")

    @property
    def pay_six_thousand_rubles_button(self) -> LocalizedText:
        return self._get_entity_text("pay_six_thousand_rubles_button")

    @property
    def pay_twelve_thousand_rubles_button(self) -> LocalizedText:
        return self._get_entity_text("pay_twelve_thousand_rubles_button")

    @property
    def confirm_payment_button(self) -> LocalizedText:
        return self._get_entity_text("confirm_payment_button")

    @property
    def confirm_trial_button(self) -> LocalizedText:
        return self._get_entity_text("confirm_trial_button")



