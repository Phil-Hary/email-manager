import pytest

from unittest.mock import MagicMock

from enums import InterfaceEnum
from interfaces import ActionsInterface, PreAuthInterface, PostAuthInterface
from utils import InterfaceUtils

class TestInterfaceUtils:
    @pytest.fixture
    def interface_utils(self):
        return InterfaceUtils()

    @pytest.fixture
    def mock_pre_auth_interface(self):
        return MagicMock(spec=PreAuthInterface)

    @pytest.fixture
    def mock_post_auth_interface(self):
        return MagicMock(spec=PostAuthInterface)

    @pytest.fixture
    def mock_actions_interface(self):
        return MagicMock(spec=ActionsInterface)

    def test_get_preauth_interface(self, interface_utils, mock_pre_auth_interface):
        interface_utils.get_interface = MagicMock(return_value=mock_pre_auth_interface)

        result = interface_utils.get_interface(InterfaceEnum.PRE_AUTH)

        assert result == mock_pre_auth_interface
        interface_utils.get_interface.assert_called_once_with(InterfaceEnum.PRE_AUTH)
    
    
    def test_get_postauth_interface(self, interface_utils, mock_post_auth_interface):
        interface_utils.get_interface = MagicMock(return_value=mock_post_auth_interface)

        result = interface_utils.get_interface(InterfaceEnum.POST_AUTH)

        assert result == mock_post_auth_interface
        interface_utils.get_interface.assert_called_once_with(InterfaceEnum.POST_AUTH)
    
    def test_get_actions_interface(self, interface_utils, mock_actions_interface):
        interface_utils.get_interface = MagicMock(return_value=mock_actions_interface)

        result = interface_utils.get_interface(InterfaceEnum.ACTIONS)

        assert result == mock_actions_interface
        interface_utils.get_interface.assert_called_once_with(InterfaceEnum.ACTIONS)
            