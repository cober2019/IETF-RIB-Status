from ncclient import manager
import sys
from lxml import etree
import xmltodict
import collections
import time

def is_instance(list_or_dict):
    """Converts dictionary object to list"""

    if isinstance(list_or_dict, list):
        make_list = list_or_dict
    else:
        make_list = [list_or_dict]

    return make_list

class Routing:
    
    def __init__(self):

        self.routes = collections.defaultdict(list)
        self.previous_routes = []
        self.protocols = []
        self._flapping_routes = collections.defaultdict(list)
        
        def _routing_protocols(self, data, name, type, interfaces):
        """Collect and store configured routing protocols"""
        print(interfaces)
    
        for i in is_instance(data.get('routing-protocol')):
            details = {}
            if isinstance(i.get('type'), dict):
    
                details['protocol'] = i.get('type').get('#text', {})
                details['id'] = i.get('name', {})
                details['name'] = name
                details['type'] = type

                if isinstance(interfaces.get('interface'), list):
                    details['interfaces'] = ', '.join(interfaces.get('interface', 'Not Assigned'))
                else:
                    details['interfaces'] = interfaces.get('interface', 'Not Assigned')
    
            else:
                details['protocol'] = i.get('type')
                details['id'] = i.get('name', {})
                details['name'] = name
                details['type'] = type

                if isinstance(interfaces.get('interface'), list):
                    details['interfaces'] = ', '.join(interfaces.get('interface', 'Not Assigned'))
                else:
                    details['interfaces'] = interfaces.get('interface', 'Not Assigned')
    
            self.protocols.append(details)
    
        else:
            pass
    
    
    def _rib(self, data):
        """Gets routes from RIB"""
    
        # Iterate through RIB routes and create k, v pairs
        for j in data.get('rib'):
            for i in is_instance(j.get('routes', {}).get('route', {})):
                route_details = {}
                route_details['name'] = j.get('name')
                route_details['address_family'] = j.get('address-family')
                if isinstance(i, str):
                    pass
                else:
                    try:
                        route_details['dest_prefix'] = i.get('destination-prefix')
                        route_details['route_preference'] = i.get('route-preference')
                        route_details['metric'] = i.get('metric')
    
                        if i.get('next-hop').get('outgoing-interface') is None:
                            route_details['outgoing_interface'] = '---'
                        else:
                            route_details['outgoing_interface'] = i.get('next-hop').get('outgoing-interface')
    
                        route_details['next_hop'] = i.get('next-hop').get('next-hop-address')
    
                        if i.get('active') is None:
                            route_details['active'] = 'Active Route'
                        else:
                            route_details['active'] = 'Inactive'
    
                        if isinstance(i.get('source-protocol'), dict):
                            route_details['source_protocol'] = i.get('source-protocol').get('#text')
                        else:
                            route_details['source_protocol'] = i.get('source-protocol')
    
                        # Append value of create key creating a list of dictionaries
                        self.routes[j.get('address_family')].append(route_details)

                    except AttributeError:
                        pass

    
    def get_routing_info(self, host, port, username, password):
        """Creates NETCONF Session and initiate getting the current RIB and protocols"""

        self.routes = collections.defaultdict(list)
        self.protocols = []

        try:
            # Ceate NETCONF connection
            with manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False,
                                 timeout=300) as session:

                xml_filter = f"""<filter>
                                <routing-state xmlns:rt="urn:ietf:params:xml:ns:yang:ietf-routing"/>
                                </filter>"""

                # Get data using filter
                get_state = session.get(xml_filter)
                # Convert to dictionary and slice
                int_status = xmltodict.parse(get_state.xml)["rpc-reply"]["data"]
                # Loop thought data
                for i in int_status.get('routing-state').get('routing-instance'):
                    for k, v in i.items():
                        # Gets routing protocol data
                        if k == 'routing-protocols':
                            self._routing_protocols(v, i.get('name'), i.get('type'), i.get('interfaces', {}))
                        elif k == 'ribs':
                            # Gets RIB data
                            self._rib(v)

                self._get_diff()
                self.previous_routes = self.routes

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

        return self.protocols, self.routes

    def _terminal_print(self):
        """Pring all protocols and rib to console"""

        """for i in self.protocols:
            print(f'{i["name"]:30}{i["type"]:30}{i["protocol"]:15}{i["id"]:10}{i["interfaces"]:20}')"""

        """print("\n")
        for k, v in self.routes.items():
            for i in v:
                print(f'{i["name"]:15}{i["address_family"]:10}{i["dest_prefix"]:20}{i["route_preference"]:5}'
                      f'{i["metric"]:10}{i["next_hop"]:20}{i["outgoing_interface"]:15}')"""

    def _get_diff(self):
        """Get route diffrence between current and previous rib tables"""

        old_dest = []
        new_dest = []
        routes = []

        if self.previous_routes:
            for v in self.routes.values():
                for i in v:
                    new_dest.append(i)
            for v in self.previous_routes.values():
                for i in v:
                    old_dest.append(i)

            #If routes have been added to the rib, this code will be used
            if len(old_dest) < len(new_dest):
                self._new_entries(new_dest, old_dest)

            elif len(old_dest) > len(new_dest):
                self._removed_entries(new_dest, old_dest)

    def _new_entries(self, new_dest, old_dest):
        """Used if the current rib table is larger then the previous table"""

        for i in new_dest:
            for h in old_dest:
                #Create status variable. Only change if the i or top level variable match the second level loop variable, h
                status = 0
                if i.get('dest_prefix') == h.get('dest_prefix'):
                    status = 1
                    break
                else:
                    continue

            #If status is still zero at the end of the loop than the is new , and we will modify the dictionary
            #to reflect the status
            if status == 0:
                i.update({'status': 'green'})
                i.update({'time': f'{time.strftime("%H")}:{time.strftime("%M")}:{time.strftime("%S")}'})
                self._flapping_routes['routes'].append(i)

    def _removed_entries(self, new_dest, old_dest):
        """Used if the current rib table is smaller then the previous table"""

        for i in old_dest:
            for h in new_dest:
                #Create status variable. Only change if the i or top level variable match the second level loop variable, h
                status = 0
                if i.get('dest_prefix') == h.get('dest_prefix'):
                    status = 1
                    break
                else:
                    continue
            #If status is still zero at the end of the loop than the route doesnt exist , and we will modify the dictionary
            #to reflect the status
            if status == 0:
                i.update({'status': 'orange'})
                i.update({'time': f'{time.strftime("%H")}:{time.strftime("%M")}:{time.strftime("%S")}'})
                self._flapping_routes['routes'].append(i)


    @property
    def flapping_routes(self):
        """Used to access _flapping_routes directly"""

        return self._flapping_routes

 
