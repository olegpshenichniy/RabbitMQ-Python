#!/usr/bin/env python
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue
from txamqp.content import Content

from switch.broker.example_txamqp.helper import connected_amq_client

MESSAGE = 'Hello world!'


@inlineCallbacks
def publish4(result, message):
    connection, channel = result

    yield channel.exchange_declare(exchange='exchange_topic_log',
                                   type='topic')

    msg = Content('%s [%s]' % (message, 'error',))
    yield channel.basic_publish(exchange='exchange_topic_log',
                                routing_key='notification.error',
                                content=msg)
    print ' [x] Sent "%s [%s]"' % (message, 'error',)

    msg = Content('%s [%s]' % (message, 'error',))
    yield channel.basic_publish(exchange='exchange_topic_log',
                                routing_key='notification.error',
                                content=msg)
    print ' [x] Sent "%s [%s]"' % (message, 'error',)

    msg = Content('%s [%s]' % (message, 'info',))
    yield channel.basic_publish(exchange='exchange_topic_log',
                                routing_key='notification.info',
                                content=msg)
    print ' [x] Sent "%s [%s]"' % (message, 'info',)

    msg = Content('%s [%s]' % (message, 'warning',))
    yield channel.basic_publish(exchange='exchange_topic_log',
                                routing_key='notification.warning',
                                content=msg)
    print ' [x] Sent "%s [%s]"' % (message, 'warning',)

    msg = Content('%s [%s]' % (message, 'warning',))
    yield channel.basic_publish(exchange='exchange_topic_log',
                                routing_key='notification.warning',
                                content=msg)
    print ' [x] Sent "%s [%s]"' % (message, 'warning',)

    returnValue(result)


@inlineCallbacks
def publisher_cleanup(result):
    connection, channel = result

    yield channel.channel_close()
    chan0 = yield connection.channel(0)
    yield chan0.connection_close()
    reactor.stop()


def main():
    d = connected_amq_client()
    d.addCallback(publish4, MESSAGE)
    d.addCallback(publisher_cleanup)

    reactor.run()

if __name__ == "__main__":
    main()

