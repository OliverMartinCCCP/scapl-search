# -*- coding: UTF-8 -*-
import abc
import argparse
import json
import logging
import os
import types
try:
    import coloredlogs
    colored_logs_present = True
except:
    print("(Install 'coloredlogs' for colored logging)")
    colored_logs_present = False


class TaskRunner(object):
    def __init__(self, prog, plugin):
        os.chdir(os.path.dirname(__file__))
        # parse input arguments
        parser = argparse.ArgumentParser(prog=__file__,
                                         description="Task runner for SCAPL plugin {}.".format(plugin),
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("-c", "--config", dest="config", help="task configuration dictionary")
        parser.add_argument("-p", "--param", dest="param", help="plugin's specific parameters")
        parser.add_argument("-t", "--task", dest="task", help="task identifier for logging purpose")
        parser.add_argument("-v", dest="verbose", action="count", default=0, help="verbose level [default: 0 (critical)]")
        args = parser.parse_args()
        args.config, args.param = eval(args.config), eval(args.param)
        # configure logging and get the root logger
        args.verbose = args.config['LOG_LEVEL_MAPPING'][min(max(args.config['LOG_LEVEL_MAPPING'].keys()), args.verbose)]
        logging.basicConfig(format='%(name)s - %(asctime)s [%(levelname)s] %(message)s', level=args.verbose)
        self.logger = logging.getLogger(args.task)
        if colored_logs_present:
            coloredlogs.install(args.verbose)
        # set arguments as attributes
        for arg in vars(args):
            setattr(self, arg, getattr(args, arg))

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        """ Run the task code, printing the result to stdout for piping the result to the parent task
        :return: None
        """

    @staticmethod
    def bind(prog, plugin):
        def _bind_wrapper(f):
            def _bind(*args, **kwargs):
                runner = TaskRunner(prog, plugin)
                runner.run = types.MethodType(f, runner)
                output = runner.run(*args, **kwargs)
                print(json.dumps(output))
                return
            return _bind
        return _bind_wrapper
