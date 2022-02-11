#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import pytest


def setup_module():
    print("===整个.py模块开始前 只 只 只 执行一次：建立连接===")


def teardown_module():
    print("===整个.py模块结束后 只 只 只 执行一次：关闭连接===")


def setup_function():
    print("===每个函数级别用例开始执行前 都 都 都 执行setup_function()===")


def teardown_function():
    print("===每个函数级别用例结束后 都 都 都 执行teardown_function()===")


def test_one():
    print("one")


def test_two():
    print("two")


class TestCase(object):
    def setup_class(self):
        print("===整个测试类开始前只执行一次setup_class===")

    def teardown_class(self):
        print("===整个测试类结束后只执行一次teardown_class===")

    def setup_method(self):
        print("===类里面每个用例执行前都会执行setup_method()===")

    def teardown_method(self):
        print("===类里面每个用例结束后都会执行teardown_method()===")

    def setup(self):
        print("===类里面每个用例执行前都会执行setup()===")

    def teardown(self):
        print("===类里面每个用例结束后都会执行teardown()===")

    def test_three(self):
        print("three")


def test_four():
    print("four")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "-ra", "test_pytestUse.py"])
