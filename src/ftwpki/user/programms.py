# File: src/ftwpki/user/programms.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
programms
===============================


Modul programms documentation
"""

from argparse import Namespace
from collections.abc import Callable
from getpass import getpass
from pathlib import Path

from cryptography import x509
from securify.input.password import PasswordDoubleCheck

from ftwpki.baselibs.cert_request import CertificateRequest
from ftwpki.baselibs.cli_parser import ServerClientCSRParser, ServerClientCSRProtocol
from ftwpki.baselibs.core import (
    create_csr_name,
    create_distinguished_name,
    generate_rsa_key_pair,
    load_private_key_from_pem,
    save_pem,
)
from ftwpki.baselibs.policies import UserPolicy
from ftwpki.baselibs.toml_utils import toml2dn


def prog_user_csr(argv: list[str] | None = None,**kwargs) -> int:
    """
    This is the prog_user function.

    It does something useful.

    Example:
        >>> prog_user()
        'Hello, User!'
    """
    try:
        # SECTION - Configuration
        default_namespace: Namespace = Namespace()
        default_namespace.password = None
        pwcall:Callable[[], str] = kwargs.pop("pwcall", getpass)
        pwcall = pwcall if pwcall else getpass
        ca_parser: ServerClientCSRParser = ServerClientCSRParser(**kwargs)
        ca_parser.set_defaults(**toml2dn(argv))
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
            require_terminal= False,
            pwcall=pwcall)()

        # !SECTION - Password Input

        # SECTION - Keypair Creation
        priv, pub = generate_rsa_key_pair(passphrase=args.password, key_size=4096)

        args.private_key = (
            args.private_key if args.private_key else str(Path(csr_file_name).with_suffix(".key"))
        )  # noqa: E501

        args.public_key = (
            args.public_key if args.public_key else str(Path(csr_file_name).with_suffix(".pub"))
        )  # noqa: E501

        # !SECTION - Keypair Creation
        # SECTION - Transport encryption
        # FIXME - Verschlüsselung mit transport-Modul einbauen
        #    Kann erst gemacht werden wenn ein userzertifikat
        #    vorhanden ist.
        # !SECTION - Transport encryption
        # SECTION - Save Keys and CSR
        save_pem(priv, Path(f"{args.privatdir}/{args.private_key}"), is_private=True)
        save_pem(pub, Path(f"{args.public_key}"), is_private=False)
        san_args = {"ip_addresses": args.ip_addresses, "dns_names": args.host_names}

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
        "get_started_programms_old.ci.rst",
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
