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

    @property
    def trial_period_message(self) -> LocalizedText:
        return self._get_entity_text("trial_period_message")

    @property
    def trial_period_refusal_message(self) -> LocalizedText:
        return self._get_entity_text("trial_period_refusal_message")

    @property
    def trial_period_activated_message(self) -> LocalizedText:
        return self._get_entity_text("trial_period_activated_message")

    @property
    def subscription_expired_notification_message(self) -> LocalizedText:
        return self._get_entity_text("subscription_expired_notification_message")

    @property
    def subscription_last_day_left_notification_message(self) -> LocalizedText:
        return self._get_entity_text("subscription_last_day_left_notification_message")
    
    @property
    def subscription_last_two_days_left_notification_message(self) -> LocalizedText:
        return self._get_entity_text("subscription_last_two_days_left_notification_message")

    @property
    def subscription_terminated_notification_message(self) -> LocalizedText:
        return self._get_entity_text("subscription_terminated_notification_message")

    @property
    def subscription_last_day_left_termination_notification_message(self) -> LocalizedText:
        return self._get_entity_text("subscription_last_day_left_termination_notification_message")
    
    @property
    def subscription_last_two_days_left_termination_notification_message(self) -> LocalizedText:
        return self._get_entity_text("subscription_last_two_days_left_termination_notification_message")

    @property
    def support_question_sent_by_user_message(self) -> LocalizedText:
        return self._get_entity_text("support_question_sent_by_user_message")

    @property
    def admin_notification_about_new_support_question_message(self) -> LocalizedText:
        return self._get_entity_text("admin_notification_about_new_support_question_message")

    @property
    def ask_admin_for_support_answer_message(self) -> LocalizedText:
        return self._get_entity_text("ask_admin_for_support_answer_message")

    @property
    def support_answer_from_admin_message(self) -> LocalizedText:
        return self._get_entity_text("support_answer_from_admin_message")

    @property
    def support_answer_sent_to_user_message(self) -> LocalizedText:
        return self._get_entity_text("support_answer_sent_to_user_message")




