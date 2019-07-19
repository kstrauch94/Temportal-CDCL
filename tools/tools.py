import os
import logging
import sys
import config_file
import subprocess

def setup_logging(no_stream_output=False, logtofile=None):

    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(levelname)s: %(message)s")

    if logtofile is not None:
        fileHandler = logging.FileHandler(logtofile, mode="w")
        fileHandler.setFormatter(formatter)
        rootLogger.addHandler(fileHandler)

    if not no_stream_output:
        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(formatter)
        rootLogger.addHandler(consoleHandler)

def plasp_domain_search(instance):
    # look for domain in the same folder
    logging.info("testing domain path: {}".format(os.path.join(get_parent_dir(instance), "domain.pddl")))
    if os.path.isfile(os.path.join(get_parent_dir(instance), "domain.pddl")):
        domain = os.path.join(get_parent_dir(instance), "domain.pddl")
        logging.info("Succes finding domain!")
    # look for domain in parent folder
    else:
        logging.info("testing domain path: {}".format(os.path.join(get_parent_dir(get_parent_dir(instance)), "domain.pddl"))) 
        if os.path.isfile(os.path.join(get_parent_dir(get_parent_dir(instance)), "../domain.pddl")):
            domain = os.path.join(get_parent_dir(get_parent_dir(instance)), "../domain.pddl")
            logging.info("Succes finding domain!")

        else:
            return None

    return domain
            
def plasp_translate(instance, domain, filename, no_fd):

    if domain is None:
        domain = plasp_domain_search(instance)
        if domain is None:
            logging.error("no domain could be found. Exiting...")
            sys.exit(-1)

    logging.info("translating instance {}\nwith domain {}".format(instance, domain))

    if not no_fd:
        logging.info("Calling Fast Downward preprocessing...")
        fd_call = config_file.FD_CALL + [domain, instance]
        instance_files = ["output.sas"]

        output = subprocess.check_output(fd_call).decode("utf-8")

    else:
        instance_files = [domain, instance]

    logging.info("Translating with plasp...")
    plasp_call = [config_file.PLASP, "translate"] + instance_files

    output = subprocess.check_output(plasp_call).decode("utf-8")
    with open(filename, "w") as f:
        f.write(output)

    logging.info("saved translation into {}".format(filename))

    if not no_fd:
        os.remove("output.sas")

def plasp2_translate(instance, domain, filename):
    if domain is None:
        domain = plasp_domain_search(instance)
        if domain is None:
            logging.error("no domain could be found. Exiting...")
            sys.exit(-1)

    instance_files = [domain, instance]

    logging.info("translating instance {}\nwith domain {}".format(instance, domain))
    logging.info("Translating with plasp 2...")
    plasp_call = [config_file.PLASP, "-c"] + instance_files

    output = subprocess.check_output(plasp_call).decode("utf-8")

    logging.info(output)

    ls_call = ["ls", "plasp_output"]
    output = subprocess.check_output(ls_call).decode("utf-8")
    logging.info(output)
    files = output.split()
    files = [os.path.join("plasp_output", f) for f in files if "plasp.log" not in f and "generated_encoding" not in f]
    logging.info(files)
    translated_instance = ""
    for _f in files:
        with open(_f, "r") as f:
            translated_instance += f.read()

    with open(filename, "w") as f:
        f.write(translated_instance.replace("#base.", ""))

    logging.info("saved translation into {}".format(filename))


def get_parent_dir(path):
    # this gets the name of the parent folder

    # if there is a trailing backslash then delete it
    if path.endswith("/"):
        path = path[:-1]

    return os.path.dirname(path)