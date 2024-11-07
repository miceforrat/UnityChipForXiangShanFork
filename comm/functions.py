#coding=utf8
#***************************************************************************************
# This project is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#
# See the Mulan PSL v2 for more details.
#**************************************************************************************/


import os
import time
import base64
import re
import tarfile
import requests
import subprocess
import fnmatch
import importlib
import traceback
import copy
from .logger import warning, debug, info
from .cfg import get_config


def merge_dict(dict1, dict2):
    """
    Merge two dictionaries
    """
    if not dict1:
        return dict2
    if not dict2:
        return dict1
    for key in dict2:
        if key in dict1:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                merge_dict(dict1[key], dict2[key])
            else:
                dict1[key] = dict2[key]
        else:
            dict1[key] = dict2[key]
    return dict1


def get_abs_path(path, sub, cfg):
    path = replace_default_vars(path, cfg)
    ret_path = ""
    if path.startswith("/"):
        ret_path = os.path.join(path, sub)
    else:
        ret_path = os.path.abspath(os.path.join(os.path.dirname(cfg.__file__), path, sub))
    if ret_path.endswith("/"):
        ret_path = ret_path[:-1]
    return ret_path


def get_log_dir(subdir="", cfg=None):
    cfg = get_config(cfg)
    return get_abs_path(cfg.output.out_dir, os.path.join(cfg.log.file_dir, subdir), cfg)


def get_out_dir(subdir="", cfg=None):
    cfg = get_config(cfg)
    return get_abs_path(cfg.output.out_dir, subdir, cfg)


def get_rtl_dir(subdir="", cfg=None):
    cfg = get_config(cfg)
    return get_abs_path(cfg.rtl.cache_dir, subdir, cfg)


def get_rtl_lnk_version(cfg=None):
    lnk = os.path.join(get_rtl_dir(cfg=cfg), "rtl")
    assert os.path.exists(lnk), f"rtl link {lnk} not found"
    assert os.path.islink(lnk), f"{lnk} is not a link, please check"
    version = os.readlink(lnk).replace("/rtl", "").split("/")[-1].strip()
    return version


def get_root_dir(subdir=""):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../", subdir))


def is_all_file_exist(files_to_check, dir):
    for f in files_to_check:
        if not os.path.exists(os.path.join(dir, f)):
            return f
    return True


def time_format(seconds=None, fmt="%Y%m%d-%H%M%S"):
    """
    Convert seconds to time format
    """
    if seconds is None:
        seconds = time.time()
    return time.strftime(fmt, time.gmtime(seconds))


def base64_encode(input_str):
    input_bytes = input_str.encode('utf-8')
    base64_bytes = base64.b64encode(input_bytes)
    base64_str = base64_bytes.decode('utf-8')
    return base64_str


def base64_decode(base64_str):
    base64_bytes = base64_str.encode('utf-8')
    input_bytes = base64.b64decode(base64_bytes)
    return input_bytes.decode('utf-8')


def use_rtl(rtl_file, out_dir):
    rtl_path = os.path.join(out_dir, rtl_file)
    dir_name = os.path.basename(rtl_file).replace(".tar.gz", "")
    rtl_dir = os.path.join(out_dir, dir_name)
    if not os.path.exists(rtl_dir):
        debug("Extract %s to %s" % (rtl_path, out_dir))
        with tarfile.open(rtl_path, "r:gz") as tar:
            tar.extractall(path=rtl_dir)
    lnk_file = os.path.join(out_dir, "rtl")
    if os.path.exists(lnk_file):
        debug("Remove old link %s" % lnk_file)
        os.remove(lnk_file)
    os.symlink(os.path.join(rtl_dir,"rtl"), lnk_file)


def download_rtl(base_url, out_dir, version="latest"):
    """
    Download RTL from url
    """
    debug("Download RTL from %s (%s)", base_url, version)
    if version != "latest":
        for f in os.listdir(out_dir):
            if version in f and "tar.gz" in f:
                debug("find %s in %s, ignore download" % (f, out_dir))
                use_rtl(f, out_dir)
                return True
        if version in base_url and ".tar.gz" in base_url:
            os.system(f"wget {base_url} -P {out_dir}")
        for f in os.listdir(out_dir):
            if version in f and "tar.gz" in f:
                debug("download %s success" % f)
                use_rtl(f, out_dir)
                return True
    if not base_url.endswith(".tar.gz"):
        resp = requests.get(base_url).content.decode('utf-8')
        all_keys = []
        all_urls = {}
        url = None
        for u in re.findall(r'http[s]?://\S+?\.tar\.gz', resp):
            key = u.split("/")[-1].strip()
            all_keys.append(key)
            all_urls[key] = u
            if version and version in u:
                url = u
                break
        if url is None:
            if version:
                warning(f"version {version} not found in {all_urls.keys()}, download the first one")
            assert len(all_urls) > 0, "No download url found (resp: %s)" % resp
            file_to_download = all_keys[0] # find the latest version
            for f in os.listdir(out_dir):
                if file_to_download in f and "tar.gz" in f:
                    debug("find %s in %s, ignore download", f, out_dir)
                    use_rtl(f, out_dir)
                    return True
            url = all_urls[file_to_download]
        debug(f"download {url} to {out_dir}")
        assert os.system(f"wget {url} -P {out_dir}") == 0, "Download RTL failed"
        use_rtl(url.split("/")[-1], out_dir)
    else:
        assert os.system(f"wget {base_url} -P {out_dir}") == 0, "Download RTL failed"
        use_rtl(base_url.split("/")[-1], out_dir)
    return True


def build_dut(duts, cfg):
    target_duts = [d.strip() for d in duts.split(",")]
    if len(target_duts) == 0:
        return
    prefix = "build_ut_"
    build_modules = [f.replace(".py", "") for f in 
                     os.listdir(get_root_dir("scripts")) if f.startswith(prefix) and f.endswith(".py")]
    dut_to_build = []
    for d in target_duts:
        d = prefix + d
        if "*" in d or "?" in d:
            dut_to_build.extend(fnmatch.filter(build_modules, d))
        elif d in build_modules:
            dut_to_build.append(d)
    dut_to_build = list(set(dut_to_build))
    if len(dut_to_build) == 0:
        warning(f"No dut to build for: {duts}")
        return
    for d in dut_to_build:
        debug(f"Build {d}")
        try:
            module = importlib.import_module(f"scripts.{d}")
            if not module.build(cfg):
                warning(f"Build scripts/{d}.py failed")
            else:
                info(f"Build scripts/{d}.py success")
        except Exception as e:
            warning(f"Failed to build {d}, error: {e}\n{traceback.format_exc()}")


def replace_default_vars(input_str, cfg):
    if "%{time}" in input_str:
        input_str = input_str.replace("%{time}", time_format(fmt="%Y%m%d%H%M%S"))
    if "%{pid}" in input_str:
        input_str = input_str.replace("%{pid}", str(os.getpid()))
    if "%{host}" in input_str:
        input_str = input_str.replace("%{host}", os.uname().nodename)
    if "%{root}" in input_str:
        input_str = input_str.replace("%{root}", get_root_dir())
    if "%{gitag}" in input_str:
        input_str = input_str.replace("%{gitag}", get_git_tag())
    if "%{giturl}" in input_str:
        input_str = input_str.replace("%{giturl}", get_git_url_with_commit())
    return input_str


def replace_default_vars_in_dict(input_dict, cfg):
    data = copy.deepcopy(input_dict)
    def _replace_default_vars(target_dict, data_ref):
        for k, v in target_dict.items():
            if isinstance(k, str) and "%{" in k:
                del data_ref[k]
                k = replace_default_vars(k, cfg)
                data_ref[k] = v
            if isinstance(v, str) and "%{" in v:
                v = replace_default_vars(v, cfg)
                data_ref[k] = v
            elif isinstance(v, dict):
                _replace_default_vars(v, data_ref[k])
    _replace_default_vars(input_dict, data)
    return data


def get_report_dir(cfg=None):
    cfg = get_config(cfg)
    return os.path.join(get_out_dir(cfg=cfg), cfg.report.report_dir)


def new_report_name(cfg=None):
    cfg = get_config(cfg)
    report_dir = get_report_dir(cfg=cfg)
    report_name = replace_default_vars(str(cfg.report.report_name), cfg)
    os.makedirs(report_dir, exist_ok=True)
    return report_dir, report_name


def exe_cmd(cmd, no_log=False):
    if isinstance(cmd, list):
        cmd = " ".join(cmd)
    if no_log:
        result = subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout = result.stdout.decode("utf-8")
        stderr = result.stderr.decode("utf-8")
    else:
        result = subprocess.run(cmd, shell=True)
        stdout = ""
        stderr = ""
    success = result.returncode == 0
    return success, stdout, stderr


def get_git_commit():
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")
        return commit
    except subprocess.CalledProcessError as e:
        warning(f"Error getting git commit: {e}")
        return "none"


def is_git_dirty():
    try:
        status = subprocess.check_output(["git", "status", "--porcelain"]).strip().decode("utf-8")
        return len(status) > 0
    except subprocess.CalledProcessError as e:
        warning(f"Error checking if git is dirty: {e}")
        return False


def get_git_branch():
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip().decode("utf-8")
        return branch
    except subprocess.CalledProcessError as e:
        warning(f"Error getting git branch: {e}")
        return "none"


def get_git_tag():
    return get_git_branch() + "-" + get_git_commit() + ("-dirty" if is_git_dirty() else "")



def get_git_remote_url():
    try:
        url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).strip().decode("utf-8")
        return url
    except subprocess.CalledProcessError as e:
        return "none"


def get_git_url_with_commit():
    url = get_git_remote_url()
    commit = get_git_commit()
    if url != "none" and commit != "none":
        return f"{url}/commit/{commit}" + " (dirty)" if is_git_dirty() else ""
    return "none"
