import copy
import json
import logging
import pprint

import srv_msg
import srv_control
import misc
from cb_api import global_parameter_set, subnet_set, network_set, subnet_del_by_prefix
from forge_cfg import world


log = logging.getLogger('forge')


def get_config():
    cmd = {"command": "config-get", "arguments": {}}
    response = srv_msg.send_request(world.proto, cmd)
    assert response['result'] == 0
    return response['arguments']


def _reload():
    # request config reloading
    cmd = {"command": "config-reload", "arguments": {}}
    response = srv_msg.send_request(world.proto, cmd)
    assert response == {'result': 0, 'text': 'Configuration successful.'}


class ConfigElem(object):
    def __init__(self, parent_cfg):
        self.parent_cfg = parent_cfg

    def get_root(self):
        if self.parent_cfg:
            return self.parent_cfg.get_root()
        else:
            return self

    def get_parent(self):
        return self.parent_cfg


class ConfigNetworkModel(ConfigElem):
    def __init__(self, parent_cfg, network_cfg):
        ConfigElem.__init__(self, parent_cfg)
        self.cfg = network_cfg

    def get_dict(self):
        cfg = copy.deepcopy(self.cfg)

        subnets = self.parent_cfg.get_subnets(network=self.cfg['name'])
        if subnets:
            proto = world.proto[1]
            subnets_key = 'subnet' + proto
            cfg[subnets_key] = []
            for sn in subnets:
                cfg[subnets_key].append(sn.get_dict())

        return cfg

    def update(self, **kwargs):
        for param, val in kwargs.items():
            param = param.replace('_', '-')
            if val is None:
                if param in self.cfg:
                    del self.cfg[param]
            else:
                self.cfg[param] = val

        # send command
        response = network_set(self.cfg)
        assert response["result"] == 0

        # request config reloading and check result
        config = self.get_root().reload_and_check()

        return config


class ConfigSubnetModel(ConfigElem):
    def __init__(self, parent_cfg, subnet_cfg):
        ConfigElem.__init__(self, parent_cfg)
        self.cfg = subnet_cfg
        if 'shared-network-name' not in self.cfg:
            self.cfg['shared-network-name'] = ''

    def get_dict(self):
        cfg = copy.deepcopy(self.cfg)
        del cfg['shared-network-name']
        return cfg

    def update(self, **kwargs):
        # prepare arguments
        if 'pool' in kwargs:
            pool = kwargs.pop('pool')
            self.cfg['pools'] = [{"pool": pool}]

        for param, val in kwargs.items():
            param = param.replace('_', '-')
            if val is None:
                if param in self.cfg:
                    del self.cfg[param]
            else:
                self.cfg[param] = val

        # send command
        response = subnet_set(self.cfg)
        assert response["result"] == 0

        # request config reloading and check result
        config = self.get_root().reload_and_check()

        return config

    def delete(self):
        response = subnet_del_by_prefix(self.cfg['subnet'])
        assert response["result"] == 0

        config = self.get_root().reload_and_check()
        return config

def _substitute_vars(cfg):
    for k, v in cfg.items():
        if isinstance(v, basestring):
            cfg[k] = srv_control.test_define_value(v)[0]
        elif isinstance(v, dict):
            _substitute_vars(v)
        elif isinstance(v, list):
            new_list = []
            for lv in v:
                if isinstance(lv, dict):
                    _substitute_vars(lv)
                    new_list.append(lv)
                elif isinstance(lv, basestring):
                    new_list.append(srv_control.test_define_value(lv)[0])
                else:
                    new_list.append(lv)
            cfg[k] = new_list

CONFIG_DEFAULTS = {}
CONFIG_DEFAULTS['v4'] = {
    'decline-probation-period': 86400,
    'echo-client-id': True,
    'match-client-id': True,
    'next-server': '0.0.0.0',
    'reservation-mode': 'all',
    't1-percent': 0.5,
    't2-percent': 0.875,
    'valid-lifetime': 7200,
    }
CONFIG_DEFAULTS['v6'] = {
    'calculate-tee-times': True,
    'decline-probation-period': 86400,
    "mac-sources": ["any"],
    'preferred-lifetime': 3600,
    'relay-supplied-options': ["65"],
    "reservation-mode": "all",
    "server-id": {
        "enterprise-id": 0,
        "htype": 0,
        "identifier": "",
        "persist": True,
        "time": 0,
        "type": "LLT"
    },
    't1-percent': 0.5,
    't2-percent': 0.8,
    'valid-lifetime': 7200,
}


def get_cfg_default(name):
    return CONFIG_DEFAULTS[world.proto][name]


class ConfigModel(ConfigElem):
    def __init__(self, init_cfg, force_reload=True):
        ConfigElem.__init__(self, None)
        self.cfg = init_cfg
        self.subnets = {}
        self.subnet_id = 0
        self.shared_networks = {}

        if 'subnets' in init_cfg:
            for sn in init_cfg['subnets']:
                subnet_cfg = ConfigSubnetModel(self, sn)
                self.subnets[sn['subnet']] = subnet_cfg

        self.force_reload = force_reload

    def get_dict(self):
        proto = world.proto[1]

        cfg = copy.deepcopy(self.cfg)
        if self.subnets:
            subnets_key = 'subnet' + proto
            cfg[subnets_key] = []
            for sn in self.subnets.values():
                if sn.cfg['shared-network-name'] is '':
                    cfg[subnets_key].append(sn.get_dict())

        if self.shared_networks:
            cfg['shared-networks'] = []
            for net in self.shared_networks.values():
                cfg['shared-networks'].append(net.get_dict())

        dhcp_key = 'Dhcp' + proto
        cfg = {dhcp_key: cfg,
               "Control-agent": {"http-host": '$(MGMT_ADDRESS)',
                                 "http-port": 8000,
                                 "control-sockets": {"dhcp" + proto: {"socket-type": 'unix',
                                                               "socket-name": '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket'}}},
               "Logging": {"loggers": [{"name":"kea-dhcp" + proto,
                                        "output_options":[{"output": "$(SOFTWARE_INSTALL_PATH)/var/kea/kea.log"}],
                                        "debuglevel":99,
                                        "severity":"DEBUG"}]}}

        _substitute_vars(cfg)

        return cfg

    def reload_and_check(self):
        if not self.force_reload:
            return {}

        _reload()
        config = self.compare_local_with_server()
        return config

    def compare_local_with_server(self):
        proto = world.proto[1]
        dhcp_key = 'Dhcp' + proto
        # get config seen by server and compare it with our configuration
        srv_config = get_config()
        my_cfg = self.get_dict()
        # log.info('MY CFG\n%s', pprint.pformat(my_cfg))
        # log.info('KEA CFG\n%s', pprint.pformat(srv_config['Dhcp4']))
        _compare(srv_config[dhcp_key], my_cfg[dhcp_key])
        return srv_config

    def set_global_parameter(self, **kwargs):
        # prepare command
        parameters = {}
        for param, val in kwargs.items():
            param = param.replace('_', '-')
            if val is None:
                if param in self.cfg:
                    del self.cfg[param]
            else:
                parameters[param] = val
                self.cfg[param] = val

        response = global_parameter_set(parameters)
        assert response["result"] == 0

        # request config reloading and check result
        config = self.reload_and_check()

        return config


    def add_network(self, **kwargs):
        # prepare command
        network = {
            "name": "floor13",
            "interface": "$(SERVER_IFACE)"}

        if world.proto == 'v6':
            network['rapid-commit'] = False  # presence required - set False by default

        for param, val in kwargs.items():
            if val is None:
                continue
            param = param.replace('_', '-')
            network[param] = val

        # send command
        response = network_set(network)
        assert response["result"] == 0

        network_cfg = ConfigNetworkModel(self, network)
        self.shared_networks[network['name']] = network_cfg

        # request config reloading and check result
        config = self.reload_and_check()

        return network_cfg, config

    def update_network(self, **kwargs):
        # find network
        if 'network' not in kwargs:
            assert len(self.shared_networks) == 1
            network = self.shared_networks.values()[0]
        else:
            network = None
            for n in self.shared_networks.values():
                if n['name'] == kwargs['network']:
                    network = n
            if network is None:
                raise Exception('Cannot find network %s for update' % kwargs['network'])

        config = network.update(**kwargs)
        return config

    def gen_subnet_id(self):
        self.subnet_id += 1
        return self.subnet_id

    def add_subnet(self, **kwargs):
        # prepare command
        default_pool_range = "192.168.50.1-192.168.50.100" if world.proto == 'v4' else '2001:db8:1::1-2001:db8:1::100'
        subnet = {
            "id": self.gen_subnet_id(),
            "subnet": "192.168.50.0/24" if world.proto == 'v4' else '2001:db8:1::/64',
            "interface": "$(SERVER_IFACE)",
            "shared-network-name": "",
            "pools": [{"pool": kwargs.pop('pool') if 'pool' in kwargs else default_pool_range}]}

        if world.proto == 'v6':
            subnet['rapid-commit'] = False  # presence required - set False by default

        for param, val in kwargs.items():
            if val is None:
                continue
            if param == 'network':
                param = 'shared-network-name'
                val = val.cfg['name']
            subnet[param.replace('_', '-')] = val

        # send command
        response = subnet_set(subnet)
        assert response["result"] == 0

        subnet_cfg = ConfigSubnetModel(self, subnet)
        self.subnets[subnet['subnet']] = subnet_cfg

        # request config reloading and check result
        config = self.get_root().reload_and_check()

        return subnet_cfg, config

    def update_subnet(self, **kwargs):
        # find subnet
        if 'subnet' not in kwargs:
            assert len(self.subnets) == 1
            subnet = self.subnets.values()[0]
        else:
            subnet = None
            for sn in self.subnets.values():
                if sn['subnet'] == kwargs['subnet']:
                    subnet = sn
            if subnet is None:
                raise Exception('Cannot find subnet %s for update' % kwargs['subnet'])

        config = subnet.update(**kwargs)
        return config

    def del_subnet(self, **kwargs):
        # find subnet
        if 'subnet' not in kwargs:
            assert len(self.subnets) == 1
            subnet = self.subnets.values()[0]
        else:
            subnet = None
            for sn in self.subnets.values():
                if sn['subnet'] == kwargs['subnet']:
                    subnet = sn
            if subnet is None:
                raise Exception('Cannot find subnet %s for update' % kwargs['subnet'])

        del self.subnets[subnet.cfg['subnet']]

        config = subnet.delete()
        return config

    def get_subnets(self, network=None):
        subnets = []
        for sn in self.subnets.values():
            if (network is not None and sn.cfg['shared-network-name'] == network) or network is None:
                subnets.append(sn)
        return subnets


def _merge_configs(a, b, path=None):
    if path is None:
        path = []
    for k in b:
        if k in a:
            if isinstance(a[k], dict) and isinstance(b[k], dict):
                _merge_configs(a[k], b[k], path + [str(k)])
            elif isinstance(a[k], list) and isinstance(b[k], list):
                for al, bl in zip(a[k], b[k]):
                    _merge_configs(al, bl)
            elif a[k] == b[k]:
                pass
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[k] = b[k]
    return a


def _compare(recv_any, exp_any):
    if isinstance(exp_any, dict):
        _compare_dicts(recv_any, exp_any)
    elif isinstance(recv_any, list):
        _compare_lists(recv_any, exp_any)
    else:
        assert recv_any == exp_any


def _compare_dicts(rcvd_dict, exp_dict):
    all_keys = set(rcvd_dict.keys()).union(set(exp_dict.keys()))
    for k in all_keys:
        if k in ['id', 'config-control', 'lease-database', 'server-tag',
                 'interfaces-config', 'dhcp-queue-control', 'dhcp-ddns',
                 'hooks-libraries', 'sanity-checks', 'expired-leases-processing',
                 'control-socket', 'host-reservation-identifiers', 'relay']:
            # TODO: for now ignore these fields
            continue
        if k in exp_dict:
            if exp_dict[k]:
                assert k in rcvd_dict
                _compare(rcvd_dict[k], exp_dict[k])
            else:
                assert k not in rcvd_dict or rcvd_dict[k] == exp_dict[k]
        if k in rcvd_dict and rcvd_dict[k]:
            if k not in exp_dict:
                if k in CONFIG_DEFAULTS[world.proto]:
                    assert rcvd_dict[k] == CONFIG_DEFAULTS[world.proto][k]
                else:
                    assert k in exp_dict
            else:
                _compare(rcvd_dict[k], exp_dict[k])


def _compare_lists(rcvd_list, exp_list):
    assert len(rcvd_list) == len(exp_list)
    for r_v, e_v in zip(rcvd_list, exp_list):
        _compare(r_v, e_v)


def _normalize_keys(kwargs):
    for k in kwargs:
        nk = k.replace('_', '-')
        if nk != k:
            kwargs[nk] = kwargs[k]
            del kwargs[k]


def setup_server(**kwargs):
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')

    config_model_args = {}
    init_cfg = {"interfaces-config": {"interfaces": ["$(SERVER_IFACE)"]},
                "lease-database": {"type": "memfile"},
                "control-socket": {"socket-type": 'unix',
                                   "socket-name":'$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket'}}

    for param, val in kwargs.items():
        if val is None or param == 'check-config':
            continue
        if param in ['force-reload']:
            # these fields are passed to ConfigModel
            config_model_args['force_reload'] = val
            continue

        param = param.replace('_', '-')
        init_cfg[param] = val


    cfg = ConfigModel(init_cfg, **config_model_args)

    srv_control.agent_control_channel('host_address', 'host_port', 'socket_type', 'socket_name')  # TODO: to force enablic ctrl-agent
    srv_control.build_and_send_config_files2(cfg.get_dict(), 'SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # check actual configuration if requested
    if 'check-config' in kwargs and kwargs['check-config']:
        srv_config = cfg.compare_local_with_server()
        return cfg, srv_config

    return cfg


def setup_server_for_config_backend_cmds(**kwargs):
    default_cfg = {"hooks-libraries": [{"library": "$(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_cb_cmds.so"},
                                       {"library": "$(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_mysql_cb.so"}],
                   "server-tag": "abc",
                   "config-control": {"config-databases":[{"user":"$(DB_USER)",
                                                           "password":"$(DB_PASSWD)",
                                                           "name":"$(DB_NAME)",
                                                           "type":"mysql"}]}}

    _normalize_keys(kwargs)
    init_cfg = _merge_configs(default_cfg, kwargs)
    result = setup_server(**init_cfg)

    return result


def setup_server_with_radius(**kwargs):
    default_cfg = {"hooks-libraries": [{
        # Load the host cache hook library. It is needed by the RADIUS
        # library to keep the attributes from authorization to later user
        # for accounting.
        "library": "$(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_host_cache.so"
    }, {
        # Load the RADIUS hook library.
        "library": "$(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_radius.so",
        "parameters": {
            "client-id-printable": True,
            # Configure an access (aka authentication/authorization) server.
            "access": {
                # This starts the list of access servers
                "servers": [{
                    # These are parameters for the first (and only) access server
                    "name": world.f_cfg.mgmt_address,
                    "port": 1812,
                    "secret": "testing123"}],
                "attributes": [{
                        "name": "password",
                    "expr": "hexstring(pkt4.mac, ':')"}]},
            "accounting": {
                "servers": [{
                    # These are parameters for the first (and only) access server
                    "name": world.f_cfg.mgmt_address,
                    "port": 1813,
                    "secret": "testing123"
                }]
            }
        }
    }]}

    _normalize_keys(kwargs)
    init_cfg = _merge_configs(default_cfg, kwargs)
    result = setup_server(**init_cfg)

    return result