"""NCClient connection funtion"""

from netmiko import ConnectHandler, ssh_exception
from ncclient import manager

def create_netconf_connection(username, password, host, port) -> manager:
    """Creates NETCONF Session"""

    retries = 0
    netconf_session = 'error'

    # Attempt connection 3 times
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

