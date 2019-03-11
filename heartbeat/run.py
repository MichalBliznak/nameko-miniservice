#!/usr/bin/env python3
"""
THIS RUNNER SHOULD BE USED FOR DEBUGGING PURPOSES ONLY
"""

import os
import eventlet
#
os.environ["GEVENT_SUPPORT"] = "True"  # forgotten line
#
# import pydevd
# pydevd.settrace('10.79.97.54', port=11111, stdoutToServer=True, stderrToServer=True)
#
eventlet.monkey_patch()

import heartbeat
import sys
import yaml
import re
import errno

from nameko.runners import ServiceRunner
from functools import partial

try:
    import regex
except ImportError:  # pragma: no cover
    ENV_VAR_MATCHER = re.compile(
        r"""
            \$\{       # match characters `${` literally
            ([^}:\s]+) # 1st group: matches any character except `}` or `:`
            :?         # matches the literal `:` character zero or one times
            ([^}]+)?   # 2nd group: matches any character except `}`
            \}         # match character `}` literally
        """, re.VERBOSE
    )
else:  # pragma: no cover
    ENV_VAR_MATCHER = regex.compile(
        r"""
        \$\{                #  match ${
        (                   #  first capturing group: variable name
            [^{}:\s]+       #  variable name without {,},: or spaces
        )
        (?:                 # non capturing optional group for value
            :               # match :
            (               # 2nd capturing group: default value
                (?:         # non capturing group for OR
                    [^{}]   # any non bracket
                |           # OR
                    \{      # literal {
                    (?2)    # recursive 2nd capturing group aka ([^{}]|{(?2)})
                    \}      # literal }
                )*          #
            )
        )?
        \}                  # end of macher }
        """,
        regex.VERBOSE
    )

IMPLICIT_ENV_VAR_MATCHER = re.compile(
    r"""
        .*          # matches any number of any characters
        \$\{.*\}    # matches any number of any characters
                    # between `${` and `}` literally
        .*          # matches any number of any characters
    """, re.VERBOSE
)


def _replace_env_var(match):
    env_var, default = match.groups()
    value = os.environ.get(env_var, None)
    if value is None:
        # expand default using other vars
        if default is None:
            # regex module return None instead of
            #  '' if engine didn't entered default capture group
            default = ''

        value = default
        while IMPLICIT_ENV_VAR_MATCHER.match(value):  # pragma: no cover
            value = ENV_VAR_MATCHER.sub(_replace_env_var, value)
    return value


def env_var_constructor(loader, node, raw=False):
    raw_value = loader.construct_scalar(node)
    value = ENV_VAR_MATCHER.sub(_replace_env_var, raw_value)
    return value if raw else yaml.safe_load(value)


def setup_yaml_parser():
    yaml.add_constructor('!env_var', env_var_constructor)
    yaml.add_constructor('!raw_env_var',
                         partial(env_var_constructor, raw=True))
    yaml.add_implicit_resolver('!env_var', IMPLICIT_ENV_VAR_MATCHER)


if __name__ == "__main__":
    setup_yaml_parser()
    with open(sys.argv[1]) as f:
        config = yaml.load(f)

    runner = ServiceRunner(config=config)
    runner.add_service(heartbeat.HeartbeatService)
    runner.start()

    runnlet = eventlet.spawn(runner.wait)

    while True:
        try:
            runnlet.wait()
        except OSError as exc:
            if exc.errno == errno.EINTR:
                # this is the OSError(4) caused by the signalhandler.
                # ignore and go back to waiting on the runner
                continue
            raise
        except KeyboardInterrupt:
            print()  # looks nicer with the ^C e.g. bash prints in the terminal
            try:
                runner.stop()
            except KeyboardInterrupt:
                print()  # as above
                runner.kill()
        else:
            # runner.wait completed
            break
