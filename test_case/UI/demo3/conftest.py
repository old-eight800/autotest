#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : conftest.py
Description      : 
Time             : 2022/12/11 20:08:30
Author           : AllenLuo
Version          : 1.0
'''
import shutil
import os
from loguru import logger
import warnings
from typing import Any, Callable, Dict, Generator, List, Optional
import allure
import yaml
from tools import BASE_DIR
import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    BrowserType,
    Error,
    Page,
    Playwright,
    sync_playwright,
)
from slugify import slugify
import tempfile


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    iphone_11 = playwright.devices['iPhone 11 Pro']
    return {
        **browser_context_args,
        **iphone_11,
    }


@pytest.fixture(scope="session")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    page = context.new_page()
    yield page

def _build_artifact_test_folder(
    pytestconfig: Any, request: pytest.FixtureRequest, folder_or_file_name: str
) -> str:
    output_dir = pytestconfig.getoption("--output")
    return os.path.join(output_dir, slugify(request.node.nodeid), folder_or_file_name)

@pytest.fixture(scope="session")
def context(
    browser: Browser,
    browser_context_args: Dict,
    pytestconfig: Any,
    request: pytest.FixtureRequest,
) -> Generator[BrowserContext, None, None]:
    pages: List[Page] = []
    context = browser.new_context(**browser_context_args)
    context.on("page", lambda page: pages.append(page))
    tracing_option = pytestconfig.getoption("--tracing")
    capture_trace = tracing_option in ["on", "retain-on-failure"]
    if capture_trace:
        context.tracing.start(
            name=slugify(request.node.nodeid),
            screenshots=True,
            snapshots=True,
            sources=True,
        )

    yield context
    # If requst.node is missing rep_call, then some error happened during execution
    # that prevented teardown, but should still be counted as a failure
    failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else True

    if capture_trace:
        retain_trace = tracing_option == "on" or (
            failed and tracing_option == "retain-on-failure"
        )
        if retain_trace:
            trace_path = _build_artifact_test_folder(pytestconfig, request, "trace.zip")
            context.tracing.stop(path=trace_path)
        else:
            context.tracing.stop()

    screenshot_option = pytestconfig.getoption("--screenshot")
    capture_screenshot = screenshot_option == "on" or (
        failed and screenshot_option == "only-on-failure"
    )
    if capture_screenshot:
        for index, page in enumerate(pages):
            human_readable_status = "failed" if failed else "finished"
            screenshot_path = _build_artifact_test_folder(
                pytestconfig, request, f"test-{human_readable_status}-{index+1}.png"
            )
            try:
                page.screenshot(timeout=5000, path=screenshot_path)
            except Error:
                pass

    context.close()

    video_option = pytestconfig.getoption("--video")
    preserve_video = video_option == "on" or (
        failed and video_option == "retain-on-failure"
    )
    if preserve_video:
        for page in pages:
            video = page.video
            if not video:
                continue
            try:
                video_path = video.path()
                file_name = os.path.basename(video_path)
                video.save_as(
                    path=_build_artifact_test_folder(pytestconfig, request, file_name)
                )
                # 将视频文件放入allure报告
                allure.attach.file(_build_artifact_test_folder(pytestconfig, request, file_name),name=f"{request.node.name}-{human_readable_status}-{index+1}",attachment_type=allure.attachment_type.WEBM)

            except Error:
                # Silent catch empty videos.
                pass

test_case_path = os.path.join(BASE_DIR,"test_case","UI", "demo3", "test_demo3_case.yaml")
with open(test_case_path, "r", encoding="utf-8") as file:
    l = []
    d = {}
    test_case_raw_data = yaml.load(file.read(), Loader=yaml.FullLoader)
    for k,v in test_case_raw_data.items():
        l.append({k:v})

@pytest.fixture(params=l)
def demo3cases(request):
    """ 参数化测试用例 """
    return request.param