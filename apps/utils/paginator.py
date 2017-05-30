# -*- coding:utf-8 -*-
"""
分页器，获取分页列表
"""


def get_page_num_list(page_count, page_current, length=7):
    """
    获取分页器的页面列表
    :param page_count: 总共多少页
    :param page_current: 当前page
    :param length: 也没列表取几个
    :return: page_num_list
    """
    if page_count <= length:
        # 如果总共的页数，小于或者等于要取的长度，那么就返回全部的页面列表
        page_num_list = range(1, page_count + 1)
    else:
        # 一般是，当前页面在最中间，两边各一半，比如获取7页，当前页面是8，那么要返回
        # [5,6,7,"8",9,10,11]
        length_half = int((length - 1) / 2)
        # 先取出列表最开始的序号
        # 如果当前页面 - 一半长度，小于1，页面不能从0或者负数开始的，最小的start是1
        start = 1 if (page_current - length_half) < 1 else \
            (page_current - length_half)
        # 获取结束页面序号：开始页面  +  长度 -1 就是结尾页面的序号
        # 但是有时候 算出的end大于page_count了，就给end赋值为page_count
        end = page_count if (start + length - 1) > page_count else \
            (start + length - 1)
        # 最后当end为page_count的时候还需要对start重新计算，确保返回的列表长度是length
        if end == page_count:
            start = end - length + 1 if (end - length + 1) > 1 else 1
        page_num_list = range(start, end + 1)
    # 返回列表序号
    return page_num_list
