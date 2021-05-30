from typing import Optional
import sublime_asyncio
import sublime_asyncio.commands
import sublime_plugin
import sublime
import asyncio


async def exit_handler() -> None:
    print("sublime_asyncio_example: shutting down lots of asynchronous processes...")
    await asyncio.sleep(1.0)
    if _task:
        _task.cancel()
    print("Done shutting down")


async def run() -> None:
    try:
        while True:
            print("Hello from sublime_asyncio_example coroutine")
            await asyncio.sleep(1.0)
    except asyncio.CancelledError:
        print("sublime_asyncio_example got cancelled")


_exit_handler_id = 0
_task: Optional[asyncio.Task] = None


async def do_stuff() -> None:
    # window = sublime.active_window()
    # string = await sublime_asyncio.show_input_panel(window, "Give a string", "asdf")
    # saved_as = await sublime_asyncio.save_dialog(name=string)
    # sublime.message_dialog("You saved this file: {}".format(saved_as))
    pass


def plugin_loaded() -> None:
    global _exit_handler_id
    _exit_handler_id = sublime_asyncio.acquire(exit_handler)

    def store_task(task: asyncio.Task) -> None:
        global _task
        _task = task

    sublime_asyncio.run_coroutine(run(), store_task)
    sublime_asyncio.run_coroutine(do_stuff())


def plugin_unloaded() -> None:
    sublime_asyncio.release(at_exit=False, exit_handler_id=_exit_handler_id)


class FooCommand(sublime_asyncio.commands.WindowCommand):
    async def execute(self, action: str = "") -> None:
        try:
            print(self.__class__.__name__, "sleeping for two seconds...")
            await asyncio.sleep(2.0)
            print(self.__class__.__name__, "done sleeping")
        except asyncio.CancelledError:
            print(self.__class__.__name__, "was cancelled!")


class EventListener(sublime_plugin.EventListener):
    def on_exit(self) -> None:
        print("on_exit was called for sublime_asyncio_example")
        sublime_asyncio.release(at_exit=True)
