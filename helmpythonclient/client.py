import json
import logging
import subprocess


class HelmPythonClient:

    def __init__(self, helm='helm', kubeconfig=None,
                 default_namespace='default', default_chart_dir='',
                 raise_ex_on_err=False):

        self.helm = helm
        self.kubeconfig = kubeconfig
        self.default_namespace = default_namespace
        self.default_chart_dir = default_chart_dir
        self.raise_ex_on_err = raise_ex_on_err

    def _run_command(self, command, **kwargs):

        final_command = list(command)

        if 'kubeconfig' in kwargs and kwargs['kubeconfig']:
            final_command.append('--kubeconfig %s' % kwargs['kubeconfig'])
        else:
            final_command.append('--kubeconfig %s' % self.kubeconfig)

        if 'namespace' in kwargs and kwargs['namespace']:
            final_command.append('--namespace %s' % kwargs['namespace'])
        else:
            final_command.append('--namespace %s' % self.default_namespace)

        if 'wait' in kwargs and kwargs['wait']:
            final_command.append('--wait')

        raise_ex_on_err = self.raise_ex_on_err
        if 'raise_ex_on_err' in kwargs:
            raise_ex_on_err = kwargs['raise_ex_on_err']

        json_mode = False
        if 'json' in kwargs and kwargs['json']:
            final_command.append('-o json')
            json_mode = True

        final_command = ' '.join(final_command)

        logging.debug('running command: %s' % final_command)

        result = subprocess.run(final_command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)

        if result.stderr.decode('utf-8') != '':
            err = result.stderr.decode('utf-8')
            if raise_ex_on_err:
                raise ValueError(err)
        else:
            err = None

        data = None
        if not err:
            if json_mode:
                data = json.loads(result.stdout)
            else:
                data = result.stdout.decode('utf-8')

        return data, err

    def search(self, keyword, **kwargs):

        command = [self.helm, 'search', 'repo', keyword]
        return self._run_command(command, json=True, **kwargs)

    def pull(self, chart_name, **kwargs):

        chart_dir = self.default_chart_dir
        if 'chart_dir' in kwargs:
            chart_dir = kwargs['chart_dir']

        command = [self.helm, 'pull', chart_name, '--untar',
                   '--untardir', chart_dir]
        return self._run_command(command, **kwargs)

    def list(self, **kwargs):

        command = [self.helm, 'list']
        return self._run_command(command, json=True, **kwargs)

    def install(self, release_name, chart_name, upgrade=False, **kwargs):

        chart_dir = self.default_chart_dir
        if 'chart_dir' in kwargs:
            chart_dir = kwargs['chart_dir']

        command = [self.helm]

        if upgrade:
            command.append('upgrade')
        else:
            command.append('install')

        command.append(release_name)

        if '/' in chart_name:
            command.append(chart_name)
        else:
            command.append('%s/%s' % (chart_dir, chart_name))

        return self._run_command(command, json=True, **kwargs)

    def uninstall(self, release_name, **kwargs):

        command = [self.helm, 'uninstall', release_name]
        return self._run_command(command, **kwargs)

    def status(self, release_name, **kwargs):

        command = [self.helm, 'status', release_name]
        return self._run_command(command, json=True, **kwargs)

    def get_values(self, release_name, **kwargs):

        command = [self.helm, 'get', 'values', release_name, '--all']
        return self._run_command(command, json=True, **kwargs)

    def show_info(self, chart_name, component=all, **kwargs):

        chart_dir = self.default_chart_dir
        if 'chart_dir' in kwargs:
            chart_dir = kwargs['chart_dir']

        command = [self.helm, 'show', component]

        if '/' in chart_name:
            command.append(chart_name)
        else:
            command.append('%s/%s' % (chart_dir, chart_name))

        return self._run_command(command, **kwargs)

    def repo_list(self, **kwargs):

        command = [self.helm, 'repo', 'list']

        data, err = self._run_command(command, json=True, **kwargs)
        if data is None:
            data = []  # workaround for an Helm bug, fixed in the next release
        return data, err

    def repo_add(self, name, url, username=None, password=None, **kwargs):

        command = [self.helm, 'repo', 'add', name, url]
        if username is not None and password is not None:
            command = command + ['--username', username, '--password', password]
        return self._run_command(command, **kwargs)

    def repo_remove(self, name, **kwargs):

        command = [self.helm, 'repo', 'remove', name]
        return self._run_command(command, **kwargs)

    def repo_update(self, **kwargs):

        command = [self.helm, 'repo', 'update']
        return self._run_command(command, **kwargs)

