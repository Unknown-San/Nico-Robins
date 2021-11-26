from SaitamaRobot.modules.disable import DisableAbleCommandHandler, DisableAbleMessageHandler
from SaitamaRobot import dispatcher as f, LOGGER
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler
from telegram.ext.filters import BaseFilter

from typing import Optional, Union, List


class NatsunagiTelegramHandler:
    def __init__(self, f):
        self._dispatcher = f

    def command(
        self, command: str, filters: Optional[BaseFilter] = None, admin_ok: bool = False, pass_args: bool = False, pass_chat_data: bool = False, run_async: bool = True, can_disable: bool = True, group: Optional[Union[int]] = 40
    ):


        def _command(func):
            try:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleCommandHandler(command, func, filters=filters, run_async=run_async, pass_args=pass_args, admin_ok=admin_ok), group
                    )
                else:
                    self._dispatcher.add_handler(
                        CommandHandler(command, func, filters=filters, run_async=run_async, pass_args=pass_args), group
                    )
                LOGGER.debug(f"[FLARECMD] Loaded handler {command} for function {func.__name__} in group {group}")
            except TypeError:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleCommandHandler(command, func, filters=filters, run_async=run_async, pass_args=pass_args, admin_ok=admin_ok, pass_chat_data=pass_chat_data)
                    )
                else:
                    self._dispatcher.add_handler(
                        CommandHandler(command, func, filters=filters, run_async=run_async, pass_args=pass_args, pass_chat_data=pass_chat_data)
                    )
                LOGGER.debug(f"[FLARECMD] Loaded handler {command} for function {func.__name__}")

            return func

        return _command

    def message(self, pattern: Optional[str] = None, can_disable: bool = True, run_async: bool = True, group: Optional[Union[int]] = 60, friendly = None):
        def _message(func):
            try:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleMessageHandler(pattern, func, friendly=friendly, run_async=run_async), group
                    )
                else:
                    self._dispatcher.add_handler(
                        MessageHandler(pattern, func, run_async=run_async), group
                    )
                LOGGER.debug(f"[FLAREMSG] Loaded filter pattern {pattern} for function {func.__name__} in group {group}")
            except TypeError:
                if can_disable:
                    self._dispatcher.add_handler(
                        DisableAbleMessageHandler(pattern, func, friendly=friendly, run_async=run_async)
                    )
                else:
                    self._dispatcher.add_handler(
                        MessageHandler(pattern, func, run_async=run_async)
                    )
                LOGGER.debug(f"[FLAREMSG] Loaded filter pattern {pattern} for function {func.__name__}")

            return func
        return _message

    def callbackquery(self, pattern: str = None, run_async: bool = True):
        def _callbackquery(func):
            self._dispatcher.add_handler(CallbackQueryHandler(pattern=pattern, callback=func, run_async=run_async))
            LOGGER.debug(f'[FLARECALLBACK] Loaded callbackquery handler with pattern {pattern} for function {func.__name__}')
            return func
        return _callbackquery

    def inlinequery(self, pattern: Optional[str] = None, run_async: bool = True, pass_user_data: bool = True, pass_chat_data: bool = True, chat_types: List[str] = None):
        def _inlinequery(func):
            self._dispatcher.add_handler(InlineQueryHandler(pattern=pattern, callback=func, run_async=run_async, pass_user_data=pass_user_data, pass_chat_data=pass_chat_data, chat_types=chat_types))
            LOGGER.debug(f'[FLAREINLINE] Loaded inlinequery handler with pattern {pattern} for function {func.__name__} | PASSES USER DATA: {pass_user_data} | PASSES CHAT DATA: {pass_chat_data} | CHAT TYPES: {chat_types}')
            return func
        return _inlinequery

flarecmd = NatsunagiTelegramHandler(f).command
flaremsg = NatsunagiTelegramHandler(f).message
flarecallback = NatsunagiTelegramHandler(f).callbackquery
flareinline = NatsunagiTelegramHandler(f).inlinequery
