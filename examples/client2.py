#!/usr/bin/env python
#encoding:utf-8

# MIT License
#
# Copyright (c) 2017 Evan Liu (hmisty@gmail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
An exmaple client

Run in shell

    $ python -m bson_rpc.example_client

Or in python interactive shell

    >>> from bson_rpc import example_client
    >>> example_client.main('127.0.0.1', 8181)

"""
from time import time
from bson_rpc import connect 

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8181

    connections = []

    for i in range(10):
        connections.append(connect(host, port))
        print('connected to server %d' % i)

    for i, proxy in enumerate(connections):
        print('call server %d' % i)
        proxy.use_service(['hi', 'echo', 'add']);
        err, res = proxy.hi()
        print('response from server %d: %s' % (i, str(res)))
        err, res = proxy.echo('你好')
        print('response from server %d: %s' % (i, str(res)))
        err, res = proxy.add(1,2)
        print('response from server %d: %s' % (i, str(res)))

        proxy.disconnect();
        print('disproxyected from server %d' % i)

    proxy = connect(host, port)
    #proxy = connect('ipc:///tmp/bson_rpc')
    proxy.use_service(['add'])
    begin = time()
    success = 0
    failure = 0
    while (time() - begin) < 5: # duration: 5 sec
        err, result = proxy.add(1,2)
        if err == 0 and result == 3: #1+2=3
            success += 1
        else:
            failure += 1

    proxy.disconnect()
    end = time()
    print('Time elapsed: %d s' % int(end - begin))
    print('Successful request: %d ' % success)
    print('Failed request: %d ' % failure)
    print('Request per second: %d ' % (success / (end - begin)))

