The Certificat Sign Request Creation
#########################################




.. SECTION - Setup

>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"))
>>> env.setup(True)
>>> env.clean_home()

.. !SECTION
.. SECTION - Prepare

>>> from pathlib import Path

>>> import getpass

>>> conf_file = env.copy2cwd("csr_user_conf.toml")

>>> def getpasswd(prompt:str)->str:
...     print(prompt)
...     return "strenggeheim"

>>> cmd_line="--conf-file csr_user_conf.toml  "
>>> cmd_line += " -hn www.secure.example.org"
>>> cmd_line += " www-admin@example.org"

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['--conf-file', 
    'csr_user_conf.toml', 
    '-hn', 'www.secure.example.org',
    'www-admin@example.org']



.. !SECTION

.. SECTION - Start programm

.. SECTION - Configuration

>>> from ftwpki.baselibs.toml_utils import toml2dn

>>> from ftwpki.baselibs.cli_parser import ServerClientCSRParser, ServerClientCSRProtocol

>>> from ftwpki.baselibs.configuration import UserPKIConfig

>>> from argparse import Namespace

>>> config:UserPKIConfig = UserPKIConfig()
>>> config.set_config()


>>> from typing import Any
>>> file_conf:dict[str,Any]={"privatdir":config.private_keys.relative_to(config.config_path).as_posix(),}

>>> default_namespace:Namespace=Namespace()
>>> default_namespace.password = None

>>> ca_parser: ServerClientCSRParser = ServerClientCSRParser(prog="ftwpkicsruser")
>>> ca_parser.set_defaults(**toml2dn(sys_argv))
>>> ca_parser.set_defaults(**file_conf)

>>> args: ServerClientCSRProtocol = ca_parser.parse_args(sys_argv,default_namespace)
>>> args #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS 
Namespace(password=None, 
    countryName='DE', 
    stateOrProvinceName='', 
    localityName='Somewherecity', 
    organizationName='Fitzz TeXnik Welt', 
    organizationalUnitName='IT-Security', 
    commonName='IT-Security Server', 
    dnsubject={'countryName': 'DE', 
        'organizationName': 'Fitzz TeXnik Welt', 
        'commonName': 'IT-Security Server', 
        'localityName': 'Somewherecity', 
        'organizationalUnitName': 'IT-Security'}, 
    conf_file=...Path('csr_user_conf.toml'), 
    key_name='',  
    privatdir='.private', 
    email='www-admin@example.org', 
    ip_addresses=[], 
    host_names=['www.secure.example.org'], 
    private_key='', 
    public_key='')

.. !SECTION - Configuration


.. SECTION - CSR Creation

>>> from ftwpki.baselibs.cert_request import CertificateRequest
>>> from ftwpki.baselibs.policies import UserPolicy
>>> from ftwpki.baselibs.core import (
...         create_distinguished_name,
...         load_private_key_from_pem, 
...         generate_rsa_key_pair,
...         )

>>> from cryptography import x509

>>> subject: x509.Name = create_distinguished_name(
...     country=args.countryName,
...     state=args.stateOrProvinceName,
...     location=args.localityName,
...     organization=args.organizationName,
...     common_name=args.commonName,
...     organizational_unit=args.organizationalUnitName,
... )

>>> subject #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
<Name(...)>

<Name(C=DE,ST=,L=Somewherecity,O=Fitzz TeXnik Welt,OU=IT-Security,CN=IT-Security user)>

>>> from ftwpki.baselibs.core import create_csr_name

>>> csr_file_name: str = create_csr_name(args.commonName)

>>> csr_file_name
'IT-Security-Server.csr'



>>> user_csr: CertificateRequest = CertificateRequest(
...     subject = subject,
...     policy = UserPolicy(),
... )

>>> user_csr #doctest: +NORMALIZE_WHITESPACE
CertificateRequest(subject=<Name(CN=IT-Security Server,OU=IT-Security,O=Fitzz TeXnik Welt,L=Somewherecity,ST=,C=DE)>)

>>> san_args={"ip_addresses": args.ip_addresses, "dns_names": args.host_names}


>>> user_csr.verify_input_arguments(**san_args)

.. !SECTION - CSR Creation

.. SECTION - Password Input

Simulating User Input
----------------------

The :external+securify:class:`~securify.input.password.PasswordDoubleCheck` class is designed for 
interactive use. 
To demonstrate its behavior in a non-interactive environment like this 
documentation, we use a helper class called :class:`StubPassword`.

This stub acts as a "script" for our tests:

* **State Management:**
  It uses a Python generator to remember which password to return next.

* **Timing Simulation:** 
  It uses :external+python:func:`time.sleep` to simulate the time a human needs to 
  type. This allows us to test security features like the minimum delay.
* **Visibility:** 
  It prints the prompt strings so you can see exactly when the application 
  asks for input.


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

>>> getpass.getpass= StubPassword()

>>> from securify.input.password import PasswordDoubleCheck

.. note::
   
   In automated environments (like GitHub Actions), there is no interactive terminal (TTY) available. 
   To prevent the CI process from failing with a ``PasswordTerminalError``, we must explicitly 
   set ``require_terminal=False``.

   **The error you would otherwise see in the CI logs:**

   .. code-block:: text

      154 >>> checkpw()
      Differences (unified diff with -expected +actual):
          @@ -1,3 +1,12 @@
           Traceback (most recent call last):
          -    ...
          -securify.input.exceptions.PasswordSpeedError: Input rejected: Entry was too fast (0.00s). Minimum required: 1.5s.
          +  File "/opt/hostedtoolcache/Python/3.13.13/x64/lib/python3.13/doctest.py", line 1398, in __run
          +    exec(compile(example.source, filename, "single",
          +    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          +                 compileflags, True), test.globs)
          +                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          +  File "<doctest get_started_password.rst[25]>", line 1, in <module>
          +    checkpw()
          +    ~~~~~~~^^
          +  File "/home/runner/work/securify/securify/.tox/py313/lib/python3.13/site-packages/securify/input/password.py", line 172, in __call__
          +    raise PasswordTerminalError("Operation rejected: Input is not a terminal (TTY).")
          +securify.input.exceptions.PasswordTerminalError: Operation rejected: Input is not a terminal (TTY).
      
      /home/runner/work/securify/securify/doc/source/devel/get_started_password.rst:154: DocTestFailure


>>> args.password = PasswordDoubleCheck(min_delay=1.5,
...     require_terminal= False)()
Enter password: 
Retype password: 

.. !SECTION - Password Input
.. SECTION - Keypair Creation

>>> priv, pub = generate_rsa_key_pair(passphrase=args.password, key_size=4096)


>>> priv #doctest: +ELLIPSIS
b'-----BEGIN ENCRYPTED PRIVATE KEY-...

>>> pub #doctest: +ELLIPSIS
b'-----BEGIN PUBLIC KEY---...

>>> args.private_key = args.private_key if args.private_key else str(Path(csr_file_name).with_suffix(".key.pem"))


>>> args.public_key = args.public_key if args.public_key else str(Path(csr_file_name).with_suffix(config.ext_public))

.. !SECTION - Keypair Creation

.. SECTION - Transport encryption
.. FIXME - Verschlüsselung mit transport-Modul einbauen
    Kann erst gemacht werden wenn ein userzertifikat
    vorhanden ist.

.. !SECTION - Transport encryption

.. SECTION - Save Keys and CSR

>>> from ftwpki.baselibs.core import save_pem
>>> save_pem(priv, 
...     config.config_path / f"{args.privatdir}/{args.private_key}", 
...     is_private=True)
>>> save_pem(pub, config.data_path /f"{args.public_key}", is_private=False)

>>> san_args={"ip_addresses": args.ip_addresses, "dns_names": args.host_names}

>>> save_pem(user_csr.build(load_private_key_from_pem(pem_data=priv, passphrase= args.password
... ),**san_args).get_pem(), 
... Path(csr_file_name), is_private=False)

.. !SECTION - Save Keys and CSR

.. !SECTION - Stop programm

.. SECTION - Test existing keys

>>> conf_path:Path = config.config_path
>>> public_path:Path = config.data_path

>>> (conf_path / ".private"/ "IT-Security-Server.key.pem").is_file()
True

>>> (public_path / "IT-Security-Server.pub.pem").is_file()
True


.. !SECTION - Test existing keys

.. SECTION - Load and read CSR

>>> from ftwpki.baselibs.core import load_csr_from_pem

>>> csr_obj = load_csr_from_pem(Path(csr_file_name).read_bytes()) 

>>> csr_obj #doctest: +ELLIPSIS
<cryptography.hazmat.bindings._rust.x509.CertificateSigningRequest object at ...>

>>> from ftwpki.baselibs.core import get_subject_dict

>>> get_subject_dict(csr_obj) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
{'countryName': 'DE', 
 'stateOrProvinceName': '', 
 'localityName': 'Somewherecity', 
 'organizationName': 'Fitzz TeXnik Welt', 
 'organizationalUnitName': 'IT-Security', 
 'commonName': 'IT-Security Server'}

.. !SECTION - Load and read CSR


.. SECTION - Teardown

>>> env.clean_home()
>>> env.teardown()

.. !SECTION - Teardown
