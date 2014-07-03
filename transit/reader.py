## Copyright (c) Cognitect, Inc.
## All rights reserved.

import json
import msgpack
from decoder import Decoder
from collections import OrderedDict

class Reader(object):
    def __init__(self, protocol="json", stream=None):
        if protocol in ("json", "json_verbose"):
            self.reader = JsonUnmarshaler()
        else:
            self.reader = MsgPackUnmarshaler()
        self.default_stream = stream

    def read(self, stream=None):
        stream = stream or self.default_stream
        if stream is None:
            raise Exception("Stream is None, please .read(some-stream)")
        return self.reader.load(stream)

    def register(self, key_or_tag, val):
        self.reader.decoder.register(key_or_tag, val)

class JsonUnmarshaler(object):
    def __init__(self):
        self.decoder = Decoder()

    def load(self, stream):
        return self.decoder.decode(json.load(stream, object_pairs_hook=OrderedDict))


class MsgPackUnmarshaler(object):
    def __init__(self):
        self.decoder = Decoder()

    def load(self, stream):
        return self.decoder.decode(msgpack.load(stream, object_pairs_hook=OrderedDict))

