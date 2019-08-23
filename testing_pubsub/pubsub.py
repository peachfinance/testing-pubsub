import subprocess
import os
import signal
import psutil


class PubSubRunner:
    def __init__(self):
        self.process = None
        self.pid_file = None

    def _is_running(self):
        for proc in psutil.process_iter():
            if proc.name().find("java") > -1:
                for item in proc.cmdline():
                    if item.find("pubsub") > -1:
                        return True
        
        return False

    def start(self, port='8538'):
        if self._is_running():
            return

        port_args = f'--host-port=127.0.0.1:{port}'
        self.process = subprocess.Popen(
            " ".join(['gcloud', 'beta', 'emulators', 'pubsub', 'start', port_args]),
            shell=True,
            preexec_fn=os.setsid,
        )            

        os.environ['PUBSUB_EMULATOR_HOST'] = f'localhost:{port}'        

    def kill(self):
        del os.environ['PUBSUB_EMULATOR_HOST']        
        if self._is_running():
            os.killpg(self.process.pid, signal.SIGTERM)
