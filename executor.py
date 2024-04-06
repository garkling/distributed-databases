from multiprocessing import pool

from timer import measure


class ProcessExecutor:

    __pool: pool.Pool = pool.Pool

    def __init__(self, *, workers: int = 10, method, pre=None, post=None):
        self.method = method
        self.post = post
        self.pre = pre

        self.workers = workers

    def run(self, *args, **kwargs):
        method_name = self.method.__name__
        print(f"{method_name:-^100}")

        ctx = ()
        if self.pre is not None:
            ctx = self.pre()
            ctx = ctx if ctx is not None else ()

        with measure(f'<{method_name}> method in {self.workers}-worker pool'):
            with self.__pool(self.workers) as p:
                workers = [p.apply_async(self.method, args=(*ctx, *args), kwds=kwargs) for _ in range(self.workers)]

                [w.wait() for w in workers]

        if self.post is not None: self.post(*ctx)


class ThreadExecutor(ProcessExecutor):

    __pool = pool.ThreadPool
