#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread
# from time import sleep
from core import critical, info


class ThreadEngine(object):
    def __init__(self, max_threads):
        if max_threads < 1:
            print critical('Threads number must be > 0')
            exit()
        self.max_threads = max_threads
        self.threads = []
        print info('Start %d threads ...' % self.max_threads)

    def new_task(self, task, args):
        """ Try to launch the new task,
            try again if thread limit exception raised
        """
        while True:
            try:
                self.launch_task(task, args)
            except ThreadLimitError:
                # sleep(0.1)
                continue
            break

    def launch_task(self, task, args):
        """ Lanch task in a new thread """
        self.clean_threads()
        if len(self.threads) < self.max_threads:
            t = Thread(target=task, args=args)
            self.threads.append(t)
            t.start()
        else:
            raise ThreadLimitError("Reached threads limit")

    def clean_threads(self):
        """ Remove ended threads """
    	for thread in self.threads:
    		if not thread.isAlive():
    			self.threads.remove(thread)

    def wait(self):
        """ Wait for threads end """
        for thread in self.threads:
            thread.join()

class ThreadLimitError(Exception):
    pass
