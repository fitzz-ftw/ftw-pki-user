# File: src/ftwpki/user/programms.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
programms
===============================


Modul programms documentation
"""

import getpass  # noqa: F401
import sys
import traceback
from pathlib import Path

from ftwpki.baselibs.workflows import CSRWorkflow


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
        csr_creator = CSRWorkflow()
        csr_creator.mandantory_san=False
        # SECTION - Configuration
        csr_creator.configuration(argv)
        # !SECTION - Configuration
        # SECTION - CSR Creation
        csr_creator.csr_creation()
        # !SECTION - CSR Creation
        # SECTION - Password Input
        csr_creator.create_password()
        # !SECTION - Password Input

        # SECTION - Keypair Creation
        csr_creator.key_pair_creation()

        # !SECTION - Keypair Creation
        # SECTION - Save Keys
        csr_creator.save_keys()
        # !SECTION - Save Keys
        # SECTION - Save CSR
        csr_creator.save_csr()
        # !SECTION - Save CSR
        # SECTION - pki- Container
        csr_creator.process_pki_container()
        # !SECTION - pki- Container
        # SECTION - Cleanup
        csr_creator.cleanup()
        # !SECTION - Cleanup
        return 0
    except KeyboardInterrupt:
        return 2
    except Exception as e:
        traceback.print_exc()
        print(f"Error in {sys.argv[0]}: {e}")
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
        # "get_started_programms.ci.rst",
        "get_started_run_programms.ci.rst",
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
