# TerminalQuest/plugins/__init__.py

from .basic_commands import BasicCommandsPlugin
from .advanced_interactions import AdvancedInteractionsPlugin

def load_plugins():
    return [
        BasicCommandsPlugin(),
        AdvancedInteractionsPlugin(),
        # Add any additional plugins here
    ]

__all__ = ['load_plugins', 'BasicCommandsPlugin', 'AdvancedInteractionsPlugin']