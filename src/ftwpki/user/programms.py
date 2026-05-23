# File: src/ftwpki/user/programms.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
programms
===============================


Modul programms documentation
"""

import getpass
from argparse import Namespace
from pathlib import Path

from cryptography import x509
from securify.input.password import PasswordDoubleCheck

from ftwpki.baselibs.cert_request import CertificateRequest
from ftwpki.baselibs.cli_parser import ServerClientCSRParser, ServerClientCSRProtocol, TomlPreParser
from ftwpki.baselibs.configuration import Any, UserPKIConfig
from ftwpki.baselibs.core import (
    create_csr_name,
    create_distinguished_name,
    generate_rsa_key_pair,
    load_private_key_from_pem,
    save_pem,
)
from ftwpki.baselibs.policies import UserPolicy
from ftwpki.baselibs.toml_utils import toml2_dn, toml2dn


def prog_user_csr(argv: list[str] | None = None,**kwargs) -> int:
    """
    Execute the user Certificate Signing Request (CSR) generation process.

    This function processes command-line arguments to generate a new
    private key and a corresponding CSR for a user identity.

    :param argv: Optional list of command-line arguments. If None, sys.argv is used.
    :param kwargs: Additional keyword arguments for internal configuration overrides.
    :returns: The exit status code (0 for success, non-zero for errors).
    """
    try:
        # SECTION - Configuration
        pre_parser = TomlPreParser()
        pre_args, _ = pre_parser.parse_known_args(argv)
        config: UserPKIConfig = UserPKIConfig()
        config.set_config()
        file_conf: dict[str, Any] = {
            "privatdir": config.private_keys.relative_to(config.config_path).as_posix(),
        }
        default_namespace: Namespace = Namespace()
        default_namespace.password = None
        ca_parser: ServerClientCSRParser = ServerClientCSRParser(**kwargs)
        ca_parser.set_defaults(**toml2dn(pre_args.conf_file)) if pre_args.conf_file else ...
        # ca_parser.set_defaults(**toml2_dn(argv))
        ca_parser.set_defaults(**file_conf)
        args: ServerClientCSRProtocol = ca_parser.parse_args(argv, default_namespace)

        # !SECTION - Configuration
        # SECTION - CSR Creation
        subject: x509.Name = create_distinguished_name(
            country=args.countryName,
            state=args.stateOrProvinceName,
            location=args.localityName,
            organization=args.organizationName,
            common_name=args.commonName,
            organizational_unit=args.organizationalUnitName,
        )
        csr_file_name: str = create_csr_name(args.commonName)
        user_csr: CertificateRequest = CertificateRequest(
            subject=subject,
            policy=UserPolicy(),
        )
        san_args={"ip_addresses": args.ip_addresses, "dns_names": args.host_names}
        user_csr.verify_input_arguments(**san_args)
        # !SECTION - CSR Creation
        # SECTION - Password Input
        args.password = PasswordDoubleCheck(min_delay=1.5,
            require_terminal= False)()

        # !SECTION - Password Input

        # SECTION - Keypair Creation
        priv, pub = generate_rsa_key_pair(passphrase=args.password, key_size=4096)

        args.private_key = (
            args.private_key 
            if args.private_key 
            else str(Path(csr_file_name).with_suffix(".key.pem"))
        )  

        args.public_key = (
            args.public_key
            if args.public_key
            else str(Path(csr_file_name).with_suffix(config.ext_public))
        )  

        # !SECTION - Keypair Creation
        # SECTION - Save Keys and CSR
        save_pem(priv, config.config_path / f"{args.privatdir}/{args.private_key}", is_private=True)
        save_pem(pub, config.data_path / f"{args.public_key}", is_private=False)
        san_args={"ip_addresses": args.ip_addresses, "dns_names": args.host_names}

        save_pem(
            user_csr.build(
                load_private_key_from_pem(pem_data=priv, passphrase=args.password),
                **san_args,
            ).get_pem(),
            Path(csr_file_name),
            is_private=False,
        )
        # !SECTION - Save Keys and CSR
        return 0
    except Exception as e:
        print(f"Error in {ca_parser.prog}: {e}")
        return 1


if __name__ == "__main__": # pragma: no cover
    from doctest import FAIL_FAST, testfile
    
    be_verbose = False
    be_verbose = True
    option_flags = 0
    option_flags = FAIL_FAST
    test_sum = 0
    test_failed = 0
    passed_files = 0
    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"
    test_files = [
        "get_started_programms.ci.rst",
        "get_started_run_programms.ci.rst",
        # "get_started_programms_old.ci.rst",
    ]
    for file in test_files:
        test_file = testfiles_dir / file
        if test_file.exists():
            print(f"--- Running Doctest for {test_file.name} ---")
            doctestresult = testfile(
                str(test_file),
                module_relative=False,
                verbose=be_verbose,
                optionflags=option_flags,
            )
            test_failed += doctestresult.failed
            test_sum += doctestresult.attempted
            if doctestresult.failed > 0 and option_flags & FAIL_FAST:
                print(f"Doctest result for {test_file.name}: {doctestresult}")
                print(f"\nKeep going! You already passed {passed_files} files "
                  f"with {test_sum} tests before this hit.")                
                break  # Stop on first failure if FAIL_FAST is set
            passed_files += 1
        else:
            print(f"⚠️ Warning: Test file {test_file.name} not found.")
    if test_failed == 0:
        print(f"\nDocTests passed without errors, {test_sum} tests.")
    else:
        if not option_flags & FAIL_FAST:
            print(f"\nDocTests failed: {test_failed} tests out of {test_sum}.")
