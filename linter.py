# Copyright (c) 2013 Aparajita Fishman
# Change for CudaLint: Alexey T.
# License: MIT

import os

import shlex
import tempfile

from cuda_lint import Linter, util, options

class GometaLint(Linter):
    
    cmd = 'gometalinter --fast .'
    regex = r'(?:[^:]+):(?P<line>\d+):(?P<col>\d+)?:(?:(?P<warning>warning)|(?P<error>error)):\s*(?P<message>.*)'
    error_stream = util.STREAM_BOTH
    syntax = ('Go')
    default_type = options.KIND_ERROR
    defaults = {
        'selector': 'source.go'
    }

    def run(self, cmd, code):
        return self._live_lint(cmd, code)

    def _live_lint(self, cmd, code):
        dir = os.path.dirname(self.filename)
        if not dir:
            print('gometalinter: skipped linting of unsaved file')
            return
        filename = os.path.basename(self.filename)
        cmd = cmd + ['-I', '^'+filename]
        print('gometalinter: live linting {} in {}: {}'.format(filename, dir, ' '.join(map(shlex.quote, cmd))))
        files = [f for f in os.listdir(dir) if f.endswith('.go')]
        if len(files) > 40:
            print("gometalinter: too many files ({}), live linting skipped".format(len(files)))
            return ''
        return self.tmpdir(cmd, dir, files, self.filename, code)

    def _in_place_lint(self, cmd):
        dir = os.path.dirname(self.filename)
        if not dir:
            print('gometalinter: skipped linting of unsaved file')
            return
        filename = os.path.basename(self.filename)
        cmd = cmd + ['-I', '^'+filename]
        print('gometalinter: in-place linting {}: {}'.format(filename, ' '.join(map(shlex.quote, cmd))))
        out = self.communicate(cmd)
        return out or ''

    def tmpdir(self, cmd, dir, files, filename, code):
        """Run an external executable using a temp dir filled with files and return its output."""
        with tempfile.TemporaryDirectory(dir=dir, prefix=".gometalinter-") as tmpdir:
            for f in files:
                target = os.path.join(tmpdir, f)
                f = os.path.join(dir, f)

                if os.path.basename(target) == os.path.basename(filename):
                    # source file hasn't been saved since change, so update it from our live buffer
                    with open(target, 'wb') as f:
                        if isinstance(code, str):
                            code = code.encode('utf8')

                        f.write(code)
                else:
                    os.link(f, target)

            out = self.communicate(cmd)
        return out or ''
        '''
    
    syntax = ('HTML', 'HTML_','Go')
    cmd = (_exe, '-errors', '-quiet', '-utf8')

    regex = r'^line (?P<line>\d+) column (?P<col>\d+) - (?:(?P<error>Error)|(?P<warning>Warning)): (?P<message>.+)'
    error_stream = util.STREAM_STDERR'''
