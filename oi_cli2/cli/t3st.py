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
from rich.table import Table
from oi_cli2.cli.constant import (
    APP_NAME,
    IN_PREFIX,
    OUT_PREFIX,
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

applogger: logging.Logger = Provider2().get(DI_LOGGER)
logger = logging.getLogger(APP_NAME + ".tester")


def tester(
    in_out_list: list[tuple[str, str]],
    work_folder: str,
    test_files: List[str],
    template: Template,
    diff_fn: Callable[[str, str, str], None],
):
    """
    all path is abspath

    - copy code into work_folder
    - run compilation command
    - run binary with std_in and user output into work_folder
    - compare std_out with user_out
    """
    print()
    # makefolder & mv code 2 folder
    for code_path in test_files:
        fname = os.path.split(code_path)[-1]
        if not os.path.exists(code_path):
            raise FileNotFoundError(f"'{code_path}' not found!")
        shutil.copy(code_path, os.path.join(work_folder, fname))
    # compile
    os.chdir(work_folder)
    logger.info(f"Tester folder: {work_folder}")
    logger.info("Start compiling.")
    logger.info(f"Run [{template.compilation}]")
    if os.system(template.compilation) != 0:
        logger.error("Complete Failed.")
        return
    logger.info("Successful compilation.")
    # run  "" not better than 'time' in bash but worse is better :-)
    # TODO 指定测试后缀
    for std_in_file, std_out_file in in_out_list:
        user_out_file = os.path.join(work_folder, os.path.split(std_out_file)[-1])
        start_time = datetime.datetime.now()
        # command = f'"{template.execute}" < "{std_in_file}" > "{user_out_file}"'
        # logger.debug(command)
        # os.system(command)
        try:
            args = shlex.split(template.execute)
            logger.info(f"Execute: [{args}]")
            logger.debug(f"in: [{std_in_file}]")
            logger.debug(f"out: [{user_out_file}]")
            # 使用subprocess运行二进制程序
            process = subprocess.Popen(
                args,
                stdin=open(std_in_file),
                stdout=open(user_out_file, "w"),
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
                time.sleep(0.1)  # 暂停一秒钟，可根据需要调整

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

        table = Table().grid()
        table.add_column(min_width=20)
        table.add_column()
        table.add_row(
            "TestCase",
            f"{os.path.split(std_in_file)[-1]} => {os.path.split(std_out_file)[-1]}",
        )
        table.add_row(
            "Time spend",
            f"[green]{(end_time - start_time).total_seconds()} s[/green]",
        )
        # TODO COMPARE TIME
        if virtual_memory_size_mb != 0:
            table.add_row(
                "Virtual Memory", f"[green]{virtual_memory_size_mb} MB[/green]"
            )
        console.print(table)
        diff_fn(std_in_file, std_out_file, user_out_file)

    os.chdir("../")


# t3st is test, don't trigger pytest
def t3st_main(in_out_list: list[tuple[str, str]]) -> bool:
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

    if len(in_out_list) == 0:
        testcase_folder = os.path.abspath(".")
        assert IN_PREFIX != OUT_PREFIX
        files = set(os.listdir(os.path.join(testcase_folder)))
        for filename in files:
            if filename.startswith(IN_PREFIX):
                out_name = OUT_PREFIX + filename[len(IN_PREFIX) :]
                if out_name in files:
                    in_out_list.append(
                        (
                            os.path.join(testcase_folder, filename),
                            os.path.join(testcase_folder, out_name),
                        )
                    )
                else:
                    logger.warn(
                        f"[red]Input file found <{filename}>, output file not found.[/red]"
                    )
                    console.print(
                        f"[red]Input file found <{filename}>, output file not found.[/red]"
                    )

    os.makedirs(TEST_FOLDER, exist_ok=True)
    tester(
        in_out_list=in_out_list,
        work_folder=os.path.abspath(TEST_FOLDER),
        test_files=[os.path.abspath(source_file_name)],
        template=template,
        diff_fn=diff_result_fn,
    )

    # shutil.rmtree(TEST_FOLDER)
    # logger.debug('test finished')
    return True


@click.command(name="test")
@click.option("-i", "--input", default="")
@click.option("-o", "--output", default="")
def t3st_command(input: str, output: str) -> None:
    try:
        if (input != "") == (output != ""):
            if input != "":
                t3st_main([(os.path.abspath(input), os.path.abspath(output))])
            else:
                t3st_main([])
        else:
            console.print("[red] input and output should be both provided[/red]")
    except KeyboardInterrupt:
        logger.info("Interrupt by user")
    except Exception:
        logger.error(traceback.format_exc())
