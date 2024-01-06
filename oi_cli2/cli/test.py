#!/usr/bin/env python3
import datetime
import json
import logging
import os
import shutil
import subprocess
import traceback
import shlex
import psutil
import time
from typing import List, Callable
import click
from rich.console import Console
from oi_cli2.cli.constant import (
    DEFAULT,
    GREEN,
    IN_SUFFIX,
    OUT_SUFFIX,
    STATE_FILE,
    TEST_FOLDER,
)
from oi_cli2.utils.Provider2 import Provider2
from oi_cli2.core.DI import DI_LOGGER, DI_TEMPMAN
from oi_cli2.model.FolderState import FolderState
from oi_cli2.model.Template import Template
from oi_cli2.utils.diffTool import diff_result_fn
from oi_cli2.utils.template import TemplateManager

console = Console(color_system="256", style=None)


def tester(
    root_folder: str,
    test_files: List[str],
    testcase_folder: str,
    template: Template,
    diff_fn: Callable[[str, str, str], None],
    logger: logging.Logger,
):
    # TODO, 这里似乎传入参数也是 abspath, 两个folder 似乎有点冗余, 还有test_folder
    logger.debug(f"{root_folder},{test_files},{testcase_folder}")
    # makefolder & mv code 2 folder
    os.makedirs(TEST_FOLDER, exist_ok=True)
    for source_file_name in test_files:
        if not os.path.exists(source_file_name):
            raise FileNotFoundError(f"'{source_file_name}' not found!")
        shutil.copy(source_file_name, os.path.join(TEST_FOLDER, source_file_name))
    # compile
    os.chdir(TEST_FOLDER)
    logger.info("Start compiling.")

    # TODO 非系统命令diff, 改为 自己实现函数/注入式/支持交互
    if os.system(template.compilation) != 0:
        logger.error("Complete Failed.")
        return
    logger.info("Successful compilation.")

    logger.debug(
        "In Exist:" + os.path.join(root_folder, testcase_folder, f"{IN_SUFFIX}{0}")
    )

    # run  "" not better than 'time' in bash but worse is better :-)
    i = 0
    # TODO 指定测试后缀
    while os.path.isfile(os.path.join(root_folder, testcase_folder, f"{IN_SUFFIX}{i}")):
        std_in_file = os.path.join(root_folder, testcase_folder, f"{IN_SUFFIX}{i}")
        std_out_file = os.path.join(root_folder, testcase_folder, f"{OUT_SUFFIX}{i}")
        user_out_file = os.path.join(root_folder, TEST_FOLDER, f"{OUT_SUFFIX}{i}")
        start_time = datetime.datetime.now()
        # command = f'"{template.execute}" < "{std_in_file}" > "{user_out_file}"'
        # logger.debug(command)
        # os.system(command)
        try:
            args = shlex.split(template.execute)
            # 使用subprocess运行二进制程序
            process = subprocess.Popen(
                args,
                stdin=open(std_in_file),
                stdout=open(user_out_file, 'w'),
                stderr=subprocess.PIPE,
                text=True,
            )
            # 获取程序执行的进程ID
            pid = process.pid
            virtual_memory_size_mb = 0
            # 这个比 ru_maxrss 更和cf的一致
            while process.poll() is None:  # 进程存在时
                # 使用psutil获取进程的虚拟内存信息
                p = psutil.Process(pid)  # noqa: F821
                virtual_memory_info = p.memory_info()
                # 获取虚拟内存大小（以字节为单位）
                virtual_memory_size = virtual_memory_info.vms
                virtual_memory_size_mb = round(virtual_memory_size / 1024 / 1024, 2)
                # print( f"Virtual Memory Size of the binary program: {virtual_memory_size_mb} MB ")
                time.sleep(.1)  # 暂停一秒钟，可根据需要调整

            # 等待程序执行完成
            stdout, stderr = process.communicate()  # stdout is None (to the file)
            if stderr != "":
                print("stderr:", stderr)
            return_code = process.returncode
            if return_code != 0:
                print("return code:", return_code)
        except Exception as e:
            print(f"Error running binary program: {e}")
            return None

        end_time = datetime.datetime.now()
        print(f"TestCase {i}")
        # TODO COMPARE TIME
        print(
            f"\tTime spend: {GREEN}{(end_time - start_time).total_seconds()}s{DEFAULT}"
        )
        if virtual_memory_size_mb != 0:
            print(f"\tVM spend: {GREEN}{virtual_memory_size_mb}MB{DEFAULT}")
        diff_fn(std_in_file, std_out_file, user_out_file)

        i += 1

    os.chdir("../")


def tst_main() -> bool:
    logger: logging.Logger = Provider2().get(DI_LOGGER)
    tm: TemplateManager = Provider2().get(DI_TEMPMAN)

    # get language config
    if not os.path.isfile(STATE_FILE):
        raise Exception(f"STATE_FILE [{STATE_FILE}] NOT EXIST!")
    state_oj = FolderState()
    with open(STATE_FILE) as f:
        state_oj.__dict__ = json.load(f)
    logger.debug(f"Loaded state:{state_oj}")

    template = tm.get_template_by_name(
        platform=state_oj.oj, name=state_oj.template_alias
    )

    if template is None:
        logger.error(f"Template not found by [{state_oj.oj},{state_oj.template_alias}]")
        return False

    source_file_name = os.path.basename(template.path)
    tester(
        root_folder=os.path.abspath("."),
        test_files=[source_file_name],
        testcase_folder=os.path.abspath("."),
        template=template,
        diff_fn=diff_result_fn,
        logger=logger,
    )

    # shutil.rmtree(TEST_FOLDER)
    # logger.debug('test finished')
    return True


@click.command(name="test")
def tst_command() -> None:
    try:
        logger: logging.Logger = Provider2().get(DI_LOGGER)
        tst_main()
    except KeyboardInterrupt:
        logger.info("Interrupt by user")
    except Exception:
        logger.error(traceback.format_exc())
