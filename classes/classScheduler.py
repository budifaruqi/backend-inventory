import asyncio
from datetime import datetime
from functools import wraps, partial
from typing import Any, Awaitable, Callable

from utils.util_logger import msLogger

def run_in_event_loop(func): # type: ignore
    @wraps(func) # type: ignore
    def wrapper(self, *args, **kwargs): # type: ignore
        wrapped = partial(func, self, *args, **kwargs) # type: ignore
        self._eventloop.call_soon_threadsafe(wrapped) # type: ignore
    return wrapper # type: ignore

# return True to stop timer
TMsSchedulerCallback = Callable[..., Awaitable[bool]]

class MsScheduler:

    def __init__(
        self,
        delaySec: int | None,
        scheduleCallback: TMsSchedulerCallback | None,
        loop: asyncio.AbstractEventLoop | None = None
    ) -> None:
        self._eventloop = loop
        if (delaySec == None) or (delaySec <= 0):
            self._delaySec = 1
        else:
             self._delaySec = delaySec
        self.scheduleCallback = scheduleCallback
        self._started = False
        self._request_stop = False
        self._stoped = False
        self._user_request_stop = False
        self._timeout: asyncio.TimerHandle | None = None

    def start(self):
        if not self._eventloop:
            self._eventloop = asyncio.get_event_loop()
        self.indek = 1
        self._pending_futures: set[asyncio.Task[Any]] = set()
        self.wakeup()

    def wakeup(self):
        self._stop_timer()
        if (not self._request_stop) and (not self._user_request_stop):
            self._start_timer(self._delaySec)
        else:
            self._stoped = True
            if self._user_request_stop:
                msLogger.success("Scheduler stoped by user")

    def _start_timer(self, wait_seconds: int):
        self._stop_timer()
        if self._eventloop is not None:
            self._timeout = self._eventloop.call_later(wait_seconds, self._process_jobs)

    def _stop_timer(self):
        if hasattr(self, "_timeout"):
            if self._timeout is not None:
                self._timeout.cancel()
                del self._timeout

    @run_in_event_loop
    def _process_jobs(self):

        def callback(f: asyncio.Task[Any]):
            self._pending_futures.discard(f)
            try:
                f.result()
            except BaseException as err:
                self._started = False
                self._run_job_error(err)
            else:
                self._started = False

        if (not self._started) and (not self._user_request_stop) and (self._eventloop is not None):
            self._started = True
            coro = self.run_coroutine_job()
            f = self._eventloop.create_task(coro)
            f.add_done_callback(callback)
            self._pending_futures.add(f)

        self.wakeup()

    async def run_coroutine_job(self):
        if self.scheduleCallback:
            self._user_request_stop = await self.scheduleCallback()

    def _run_job_error(self, err: BaseException):
        pass
    
    async def shutdown(self):
        while len(self._pending_futures) > 0:
            try:
                f = self._pending_futures.pop()
                if not f.done():
                    self._request_stop = True
                    msLogger.warning("Waiting scheduler to complete. Please wait ...")
                    tStart = datetime.now().timestamp()
                    waitSeconds = 20
                    while (not self._stoped) and (not f.done()):
                        await asyncio.sleep(0.1)
                        # wait for waitSeconds seconds
                        if datetime.now().timestamp() - tStart > waitSeconds:
                            # force shutdown
                            msLogger.warning(f"Scheduller is timeout ({waitSeconds}) seconds")
                            break
                    if not f.done():
                        f.cancel()
            except:
                pass

        self._pending_futures.clear()
        self._stop_timer()