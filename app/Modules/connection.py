"""NCClient connection funtion"""

from ncclient import manager

def create_netconf_connection(username, password, host, port) -> manager:
    """Creates NETCONF Session"""

    netconf_session = 'error'
    
    try:

        netconf_session = manager.connect(host=host, port=port, username=username,
                                          password=password,
                                          device_params={'name': 'csr'})
        
    except manager.operations.errors.TimeoutExpiredError:
        pass
    except (AttributeError, OSError):
        pass
    except manager.transport.TransportError:
        pass
    except manager.transport.AuthenticationError:
        pass
    except manager.operations.rpc.RPCError:
        pass
    except manager.operations.rpc.RPCError:
        pass

    return netconf_session

