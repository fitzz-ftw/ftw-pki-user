Running the programm Successfully and Errors
==============================================

.. SECTION - Setup

>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"))
>>> env.setup(True)

.. !SECTION
.. SECTION - Prepare

>>> from pathlib import Path
>>> private_dir:Path = Path("privat")
>>> private_dir.mkdir(parents=True, exist_ok=True)




>> test_paswd_path = env.copy2cwd("privat/testpasswd")
>>> conf_file = env.copy2cwd("csr_user_conf.toml")

>>> cmd_line="--conf_file csr_user_conf.toml  "
>>> cmd_line += " --private-dir privat"
>>> cmd_line += " -hn www.secure.example.org"
>>> cmd_line += " www-admin@example.org"

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['--conf_file', 
    'csr_user_conf.toml', 
    '--private-dir', 'privat', 
    '-hn', 'www.secure.example.org',
    'www-admin@example.org']

>>> import time
>>> class StubPassword:
...     def __init__(self):
...         self.generate = self._generate()
...     def _generate(self):
...         # first run
...         yield "secret"
...         time.sleep(2)
...         yield "secret"
...     def __call__(self, prompt):
...         print(prompt, flush=True)
...         return next(self.generate)
...     def reset(self):
...         self.generate = self._generate()

>>> stubgetpasswd = StubPassword()


.. !SECTION
.. SECTION - Start programm function

>>> from ftwpki.user.programms import prog_user_csr
>>> prog_user_csr(sys_argv, prog="ftwpkiserver", pwcall=stubgetpasswd)
Enter password: 
Retype password: 
0

>>> cmd_line="--conf_file csr_user_conf.toml  "
>>> cmd_line += " --private-dir privat"
>>> cmd_line += " www-admin@example.org"

>>> sys_argv= shlex.split(cmd_line) 

>>> prog_user_csr(sys_argv, pwcall=stubgetpasswd) #doctest: +ELLIPSIS
Error in ...: At least an ip address or a hostname has to be given
1

>>> cmd_line="--conf_file csr_user_conf.toml  "
>>> cmd_line += " --private-dir privat"
>>> cmd_line += " -hn www.secure.example.org"
>>> sys_argv= shlex.split(cmd_line)

>>> stubgetpasswd.reset()
>>> prog_user_csr(sys_argv, pwcall=stubgetpasswd) #doctest: +ELLIPSIS
Error in ...: the following arguments are required: email
1


>>> cmd_line="--conf_file csr_user_conf.toml  "
>>> cmd_line += " --private-dir privat"
>>> cmd_line += " -hn org"
>>> cmd_line += " www-admin@example.org"

>>> sys_argv= shlex.split(cmd_line)
>>> prog_user_csr(sys_argv, pwcall=stubgetpasswd) #doctest: +ELLIPSIS
Error in ...: Hostname 'org' is not a FQDN (missing dot).
1

>>> cmd_line="--conf_file csr_user_conf.toml  "
>>> cmd_line += " --private-dir privat"
>>> cmd_line += " -hn localhost"
>>> cmd_line += " www-admin@example.org"

>>> sys_argv= shlex.split(cmd_line)
>>> stubgetpasswd.reset()
>>> prog_user_csr(sys_argv, pwcall=stubgetpasswd)
Enter password: 
Retype password: 
0

>>> cmd_line="--conf_file csr_user_conf.toml  "
>>> cmd_line += " --private-dir privat"
>>> cmd_line += " -hn localhost"
>>> cmd_line += " -ip 127.0.0.1"
>>> cmd_line += " www-admin@example.org"

>>> sys_argv= shlex.split(cmd_line)
>>> stubgetpasswd.reset()
>>> prog_user_csr(sys_argv, pwcall=stubgetpasswd)
Enter password: 
Retype password: 
0

>>> cmd_line="--conf_file csr_user_conf.toml  "
>>> cmd_line += " --private-dir privat"
>>> cmd_line += " -ip org"
>>> cmd_line += " www-admin@example.org"

>>> sys_argv= shlex.split(cmd_line)
>>> stubgetpasswd.reset()
>>> prog_user_csr(sys_argv, pwcall=stubgetpasswd) #doctest: +ELLIPSIS
Error in ...: 'org' does not appear to be an IPv4 or IPv6 address
1

>>> cmd_line = " --private-dir privat"
>>> cmd_line += " -ip 192.168.1.1"
>>> cmd_line += " www-admin@example.org"

>>> sys_argv= shlex.split(cmd_line)
>>> stubgetpasswd.reset()
>>> prog_user_csr(sys_argv, pwcall=stubgetpasswd) #doctest: +ELLIPSIS
Error in ...: Attribute's length must be >= 2 and <= 2, but it was 0
1

>>> cmd_line = " -C DE"
>>> cmd_line += " -CN 'IT-Security Server'"
>>> cmd_line += " --private-dir privat"
>>> cmd_line += " -ip 192.168.1.1"
>>> cmd_line += " www-admin@example.org"

>>> sys_argv= shlex.split(cmd_line)
>>> stubgetpasswd.reset()
>>> prog_user_csr(sys_argv, pwcall=stubgetpasswd)
Enter password: 
Retype password: 
0

.. !SECTION - Start programm function

.. SECTION - Teardown

>>> env.clean_home()
>>> env.teardown()

.. !SECTION - Teardown
