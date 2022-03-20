from dataclasses import dataclass

import pytest
from assertpy import assert_that
from pytest_mock import MockerFixture

from ibkr_trade_log.bootstrap.messagebus.model import Message, Command, Query, Event
from ibkr_trade_log.bootstrap.messagebus.memory import MemoryMessageBus


@dataclass(frozen=True)
class StubCommand(Command):
    message: str


@dataclass(frozen=True)
class StubEvent(Event):
    message: str


@dataclass(frozen=True)
class StubMessage(Message):
    message: str


@dataclass(frozen=True)
class StubQuery(Query[StubMessage]):
    message: str


class TestMemoryMessageBus:
    @pytest.fixture
    def messagebus(self):
        return MemoryMessageBus()

    def test_command_register_tell_flow(self, messagebus, mocker: MockerFixture):
        message_handler = mocker.MagicMock()
        messagebus.declare(StubCommand, handler=message_handler)

        command = StubCommand(message="message")
        messagebus.tell(command)

        message_handler.assert_called_with(command)

    def test_command_register_ask_flow(self, messagebus, mocker: MockerFixture):
        return_message = StubMessage(message="something")
        message_handler = mocker.MagicMock(return_value=return_message)
        messagebus.declare(StubQuery, handler=message_handler)

        query = StubQuery(message="something")
        message = messagebus.ask(query)
        assert_that(message).is_equal_to(return_message)

    def test_event_pub_sub_flow(self, messagebus, mocker: MockerFixture):
        event_handler = mocker.MagicMock()
        messagebus.subscribe(StubEvent, handler=event_handler)

        event_handler2 = mocker.MagicMock()
        messagebus.subscribe(StubEvent, handler=event_handler2)

        event = StubEvent(message="something")
        messagebus.publish(event)

        event_handler.assert_called_once_with(event)
        event_handler2.assert_called_once_with(event)
