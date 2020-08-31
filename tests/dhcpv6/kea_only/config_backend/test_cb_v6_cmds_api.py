"""Kea database config backend commands hook testing"""

import pytest
import srv_msg

from cb_model import setup_server_for_config_backend_cmds

pytestmark = [pytest.mark.v6,
              pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend,
              pytest.mark.cb_cmds]


@pytest.fixture(autouse=True)
def run_around_tests():
    setup_server_for_config_backend_cmds()
    cmd = dict(command="remote-server6-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": "abc"}]})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)


def test_availability():
    cmd = dict(command='list-commands')
    response = srv_msg.send_ctrl_cmd(cmd)

    for cmd in ["remote-global-parameter6-del",
                "remote-global-parameter6-get",
                "remote-global-parameter6-get-all",
                "remote-global-parameter6-set",
                "remote-network6-del",
                "remote-network6-get",
                "remote-network6-list",
                "remote-network6-set",
                "remote-option-def6-del",
                "remote-option-def6-get",
                "remote-option-def6-get-all",
                "remote-option-def6-set",
                "remote-option6-global-del",
                "remote-option6-global-get",
                "remote-option6-global-get-all",
                "remote-option6-global-set",
                "remote-subnet6-del-by-id",
                "remote-subnet6-del-by-prefix",
                "remote-subnet6-get-by-id",
                "remote-subnet6-get-by-prefix",
                "remote-subnet6-list",
                "remote-subnet6-set"]:
        assert cmd in response['arguments']


# subnet tests
@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_subnet6_set_basic(channel):
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "id": 1,
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}


def test_remote_subnet6_set_empty_subnet():
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "shared-network-name": "",
                                                        "subnets": [{"subnet": "",
                                                                     "id": 1,
                                                                     "interface": "$(SERVER_IFACE)"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "subnet configuration failed: Invalid subnet syntax (prefix/len expected)" in response["text"]


def test_remote_subnet6_set_missing_subnet():
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "shared-network-name": "",
                                                        "subnets": [{"interface": "$(SERVER_IFACE)", "id": 1}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "subnet configuration failed: mandatory 'subnet' parameter " \
           "is missing for a subnet being configured" in response["text"]


def test_remote_subnet6_set_stateless():
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64",
                                                                     "id": 1,
                                                                     "shared-network-name": "",
                                                                     "interface": "$(SERVER_IFACE)"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}


def test_remote_subnet6_set_id():
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}


def test_remote_subnet6_set_duplicated_id():
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:2::/64", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:2::1-2001:db8:2::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "2001:db8:2::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "subnets": [{"id": 5, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "2001:db8:2::/64"}]},
                        "result": 0, "text": "1 IPv6 subnet(s) found."}


def test_remote_subnet6_set_duplicated_subnet():
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}


def test_remote_subnet6_set_all_values():
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"shared-network-name": "",
                                                                     "require-client-classes": ["XYZ"],
                                                                     "id": 2, "interface": "$(SERVER_IFACE)",
                                                                     "pools": [{"pool": "2001:db8:1::1-2001:db8:1::10",
                                                                                "option-data": [{"code": 7,
                                                                                                 "data": "12",
                                                                                                 "always-send": True,
                                                                                                 "csv-format": True}]}],
                                                                     "pd-pools": [{
                                                                         "delegated-len": 91,
                                                                         "prefix": "2001:db8:2::",
                                                                         "prefix-len": 90}],
                                                                     "reservation-mode": "all",
                                                                     "subnet": "2001:db8:1::/64",
                                                                     "valid-lifetime": 1000,
                                                                     "rebind-timer": 500,
                                                                     "renew-timer": 200,
                                                                     "option-data": [{"code": 7,
                                                                                      "data": "123",
                                                                                      "always-send": True,
                                                                                      "csv-format": True}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 2, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}


def test_remote_subnet6_get_all_values():
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"shared-network-name": "",
                                                                     "require-client-classes": ["XYZ"],
                                                                     "id": 2, "interface": "$(SERVER_IFACE)",
                                                                     "pools": [{"pool": "2001:db8:1::1-2001:db8:1::10",
                                                                                "option-data": [{"code": 7,
                                                                                                 "data": "12",
                                                                                                 "always-send": True,
                                                                                                 "csv-format": True}]}],
                                                                     "pd-pools": [{
                                                                         "delegated-len": 91,
                                                                         "prefix": "2001:db8:2::",
                                                                         "prefix-len": 90}],
                                                                     "reservation-mode": "all",
                                                                     "subnet": "2001:db8:1::/64",
                                                                     "valid-lifetime": 1000,
                                                                     "rebind-timer": 500,
                                                                     "renew-timer": 200,
                                                                     "option-data": [{"code": 7,
                                                                                      "data": "123",
                                                                                      "always-send": True,
                                                                                      "csv-format": True}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 2, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {
        "count": 1,
        "subnets": [{
            "metadata": {"server-tags": ["abc"]},
            "require-client-classes": ["XYZ"],
            "shared-network-name": None,
            "id": 2,
            "interface": srv_msg.get_interface(),
            "option-data": [{"always-send": True,
                             "code": 7,
                             "csv-format": True,
                             "name": "preference",
                             "space": "dhcp6",
                             "data": "123"}],
            "pools": [{
                "option-data": [{"code": 7,
                                 "data": "12",
                                 "name": "preference",
                                 "always-send": True,
                                 "csv-format": True,
                                 "space": "dhcp6"}],
                "pool": "2001:db8:1::1-2001:db8:1::10"}],
            "pd-pools": [{
                "option-data": [],
                "delegated-len": 91,
                "prefix": "2001:db8:2::",
                "prefix-len": 90}],
            "reservation-mode": "all",
            "subnet": "2001:db8:1::/64",
            "rebind-timer": 500,
            "renew-timer": 200,
            "relay": {"ip-addresses": []},
            "valid-lifetime": 1000}]}, "result": 0, "text": "IPv6 subnet 2001:db8:1::/64 found."}


# reservation-mode is integer in db, so we need to check if it's converted correctly
def test_remote_subnet6_set_reservation_mode_all():
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "reservation-mode": "disabled",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response["arguments"]["subnets"][0]["reservation-mode"] == "disabled"


def test_remote_subnet6_set_reservation_mode_global():
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "reservation-mode": "global",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response["arguments"]["subnets"][0]["reservation-mode"] == "global"


def test_remote_subnet6_set_reservation_mode_out_pool():
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "reservation-mode": "out-of-pool",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response["arguments"]["subnets"][0]["reservation-mode"] == "out-of-pool"


def test_remote_subnet6_set_reservation_mode_disabled():
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 1,
                                                                     "shared-network-name": "",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "reservation-mode": "disabled"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response["arguments"]["subnets"][0]["reservation-mode"] == "disabled"


def _subnet_set():
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 5,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 5, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}


def test_remote_subnet6_del_by_id():
    _subnet_set()

    cmd = dict(command="remote-subnet6-del-by-id", arguments={"remote": {"type": "mysql"},
                                                              "subnets": [{"id": 5}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv6 subnet(s) deleted."}


def test_remote_subnet6_del_by_id_incorrect_id():
    _subnet_set()

    cmd = dict(command="remote-subnet6-del-by-id", arguments={"remote": {"type": "mysql"},
                                                              "subnets": [{"id": 15}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 IPv6 subnet(s) deleted."}


def test_remote_subnet6_del_id_negative_missing_subnet():
    _subnet_set()

    cmd = dict(command="remote-subnet6-del-by-id", arguments={"remote": {"type": "mysql"},
                                                              "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'id' parameter"}


def test_remote_subnet6_del_by_prefix():
    _subnet_set()

    cmd = dict(command="remote-subnet6-del-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv6 subnet(s) deleted."}


def test_remote_subnet6_del_by_prefix_non_existing_subnet():
    _subnet_set()

    cmd = dict(command="remote-subnet6-del-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "2001:db8:2::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 IPv6 subnet(s) deleted."}


def test_remote_subnet6_del_by_prefix_missing_subnet_():
    _subnet_set()
    cmd = dict(command="remote-subnet6-del-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"id": 2}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'subnet' parameter"}


def test_remote_subnet6_get_by_id():
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"shared-network-name": "",
                                                                     "id": 2, "interface": "$(SERVER_IFACE)",
                                                                     "pools": [{"pool": "2001:db8:1::1-2001:db8:1::10",
                                                                                "option-data": [{"code": 7,
                                                                                                 "data": "123",
                                                                                                 "always-send": True,
                                                                                                 "csv-format": True}]}],
                                                                     "reservation-mode": "global",
                                                                     "subnet": "2001:db8:1::/64",
                                                                     "valid-lifetime": 1000,
                                                                     "rebind-timer": 500,
                                                                     "renew-timer": 200,
                                                                     "option-data": [{"code": 7,
                                                                                      "data": "12",
                                                                                      "always-send": True,
                                                                                      "csv-format": True}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 2, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-get-by-id", arguments={"remote": {"type": "mysql"},
                                                              "subnets": [{"id": 2}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "subnets": [{"metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None,
                                                   "id": 2, "interface": srv_msg.get_interface(),
                                                   "option-data": [{"always-send": True, "code": 7, "csv-format": True,
                                                                    "data": "12", "name": "preference",
                                                                    "space": "dhcp6"}],
                                                   "pools": [{"option-data": [{"always-send": True, "code": 7,
                                                                               "csv-format": True, "data": "123",
                                                                               "name": "preference",
                                                                               "space": "dhcp6"}],
                                                              "pool": "2001:db8:1::1-2001:db8:1::10"}],
                                                   "rebind-timer": 500, "renew-timer": 200,
                                                   "reservation-mode": "global",
                                                   "pd-pools": [],
                                                   "relay": {"ip-addresses": []},
                                                   "subnet": "2001:db8:1::/64", "valid-lifetime": 1000}]},
                        "result": 0, "text": "IPv6 subnet 2 found."}


def test_remote_subnet6_get_by_id_incorrect_id():
    _subnet_set()

    cmd = dict(command="remote-subnet6-get-by-id", arguments={"remote": {"type": "mysql"},
                                                              "subnets": [{"id": 3}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "subnets": []},
                        "result": 3, "text": "IPv6 subnet 3 not found."}


def test_remote_subnet6_get_by_id_missing_id():
    _subnet_set()

    cmd = dict(command="remote-subnet6-get-by-id", arguments={"remote": {"type": "mysql"},
                                                              "subnets": [{"subnet": 3}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1,
                        "text": "missing 'id' parameter"}


def test_remote_subnet6_get_by_prefix():
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"shared-network-name": "",
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:1::1-2001:db8:1::10"}],
                                                                     "reservation-mode": "all",
                                                                     "require-client-classes": ["XYZ"],
                                                                     "subnet": "2001:db8:1::/64", "id": 1,
                                                                     "valid-lifetime": 1000}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "2001:db8:1::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {
        "count": 1,
        "subnets": [{
            "metadata": {"server-tags": ["abc"]},
            "require-client-classes": ["XYZ"],
            "shared-network-name": None,
            "id": 1,
            "interface": srv_msg.get_interface(),
            "option-data": [],
            "pools": [{
                "option-data": [],
                "pool": "2001:db8:1::1-2001:db8:1::10"}],
            "reservation-mode": "all",
            "pd-pools": [],
            "relay": {"ip-addresses": []},
            "subnet": "2001:db8:1::/64",
            "valid-lifetime": 1000}]}, "result": 0, "text": "IPv6 subnet 2001:db8:1::/64 found."}


def test_remote_subnet6_get_by_prefix_negative():
    _subnet_set()

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "2001:db8:2::/63"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "subnets": []},
                        "result": 3, "text": "IPv6 subnet 2001:db8:2::/63 not found."}


def test_remote_subnet6_get_by_prefix_incorrect_prefix():
    _subnet_set()
    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"subnet": "::/64"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1,
                        "text": "unable to parse invalid IPv6 prefix ::/64"}


def test_remote_subnet6_get_by_prefix_missing_prefix():
    _subnet_set()

    cmd = dict(command="remote-subnet6-get-by-prefix", arguments={"remote": {"type": "mysql"},
                                                                  "subnets": [{"id": "2001:db8:2::/63"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1,
                        "text": "missing 'subnet' parameter"}


def test_remote_subnet6_list():
    _subnet_set()

    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:2::/64", "id": 3,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:2::1-2001:db8:2::10"}]}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:3::/64", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "",
                                                                     "pools": [
                                                                         {"pool": "2001:db8:3::1-2001:db8:3::10"}]}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-subnet6-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 3, "subnets": [{"id": 1,
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "shared-network-name": None,
                                                               "subnet": "2001:db8:3::/64"},
                                                              {"id": 3,
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "shared-network-name": None,
                                                               "subnet": "2001:db8:2::/64"},
                                                              {"id": 5,
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "shared-network-name": None,
                                                               "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "3 IPv6 subnet(s) found."}


# network tests
@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_network6_set_basic(channel):
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{"name": "floor13"}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"shared-networks": [{"name": "floor13"}]},
                        "result": 0, "text": "IPv6 shared network successfully set."}


def test_remote_network6_set_missing_name():
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "missing parameter 'name'" in response["text"]


def test_remote_network6_set_empty_name():
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "'name' parameter must not be empty"}


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_network6_get_basic(channel):
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network6-get", arguments={"remote": {"type": "mysql"},
                                                         "shared-networks": [{
                                                             "name": "net1"}]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"interface": srv_msg.get_interface(), "name": "net1",
                                                           "metadata": {"server-tags": ["abc"]},
                                                           "option-data": [], "relay": {"ip-addresses": []}}]},
                        "result": 0, "text": "IPv6 shared network 'net1' found."}


def test_remote_network6_get_all_values():
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "client-class": "abc",
                                                             "require-client-classes": ["XYZ"],
                                                             "rebind-timer": 200,
                                                             "renew-timer": 100,
                                                             "calculate-tee-times": True,
                                                             "t1-percent": 0.5,
                                                             "t2-percent": 0.8,
                                                             "rapid-commit": True,
                                                             "valid-lifetime": 300,
                                                             "reservation-mode": "global",
                                                             "user-context": {"some weird network": 55},
                                                             "interface": "$(SERVER_IFACE)",
                                                             "option-data": [{"code": 7,
                                                                              "data": "123",
                                                                              "always-send": True,
                                                                              "csv-format": True}]}]})
    srv_msg.send_ctrl_cmd(cmd)
    cmd = dict(command="remote-network6-get", arguments={"remote": {"type": "mysql"},
                                                         "shared-networks": [{
                                                             "name": "net1"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"client-class": "abc",
                                                           "rebind-timer": 200, "renew-timer": 100,
                                                           "valid-lifetime": 300, "reservation-mode": "global",
                                                           "interface": srv_msg.get_interface(),
                                                           "metadata": {"server-tags": ["abc"]},
                                                           "require-client-classes": ["XYZ"],
                                                           "calculate-tee-times": True,
                                                           "t1-percent": 0.5,
                                                           "t2-percent": 0.8,
                                                           "rapid-commit": True,
                                                           "name": "net1",
                                                           "option-data": [{"always-send": True, "code": 7,
                                                                            "csv-format": True, "data": "123",
                                                                            "name": "preference",
                                                                            "space": "dhcp6"}],
                                                           "relay": {"ip-addresses": []},
                                                           "user-context": {"some weird network": 55}}]},
                        "result": 0, "text": "IPv6 shared network 'net1' found."}


def test_remote_network6_set_t1_t2():
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "calculate-tee-times": True,
                                                             "t1-percent": 0.5,
                                                             "t2-percent": 10,
                                                             "interface": "$(SERVER_IFACE)"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "'t2-percent' parameter is not a real" in response["text"]

    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "calculate-tee-times": True,
                                                             "t1-percent": 10,
                                                             "t2-percent": 0.5,
                                                             "interface": "$(SERVER_IFACE)"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "'t1-percent' parameter is not a real" in response["text"]

    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "calculate-tee-times": True,
                                                             "t1-percent": 0.5,
                                                             "t2-percent": 0.1,
                                                             "interface": "$(SERVER_IFACE)"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "t1-percent:  0.5 is invalid, it must be less than t2-percent: 0.1" in response["text"]


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_network6_list_basic(channel):
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2, "shared-networks": [{"metadata": {"server-tags": ["abc"]},
                                                                       "name": "net1"},
                                                                      {"metadata": {"server-tags": ["abc"]},
                                                                       "name": "net2"}]},
                        "result": 0,
                        "text": "2 IPv6 shared network(s) found."}


def test_remote_network6_list_no_networks():
    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv6 shared network(s) found."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_network6_del_basic(channel):
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd, channel=channel)

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 2,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]}, "name": "net1"},
                                                          {"metadata": {"server-tags": ["abc"]}, "name": "net2"}]},
                        "result": 0,
                        "text": "2 IPv6 shared network(s) found."}

    cmd = dict(command="remote-network6-del", arguments={"remote": {"type": "mysql"},
                                                         "shared-networks": [{"name": "net1"}]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv6 shared network(s) deleted."}

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]}, "name": "net2"}]},
                        "result": 0, "text": "1 IPv6 shared network(s) found."}

    cmd = dict(command="remote-network6-del", arguments={"remote": {"type": "mysql"},
                                                         "shared-networks": [{"name": "net2"}]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv6 shared network(s) deleted."}

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel, exp_result=3)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv6 shared network(s) found."}


def test_remote_network6_del_subnet_keep():
    # add networks
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 2,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]},
                                                           "name": "net1"},
                                                          {"metadata": {"server-tags": ["abc"]},
                                                           "name": "net2"}]},
                        "result": 0,
                        "text": "2 IPv6 shared network(s) found."}

    # add subnets to networks
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "net1",
                                                                     "pools": [{
                                                                         "pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:2::/64", "id": 2,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "net2",
                                                                     "pools": [{
                                                                         "pool": "2001:db8:2::1-2001:db8:2::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 2, "subnet": "2001:db8:2::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    # we want to have 2 subnets
    cmd = dict(command="remote-subnet6-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2, "subnets": [{"id": 1, "subnet": "2001:db8:1::/64",
                                                               "shared-network-name": "net1",
                                                               "metadata": {"server-tags": ["abc"]}},
                                                              {"id": 2, "subnet": "2001:db8:2::/64",
                                                               "shared-network-name": "net2",
                                                               "metadata": {"server-tags": ["abc"]}}]},
                        "result": 0, "text": "2 IPv6 subnet(s) found."}

    cmd = dict(command="remote-network6-del", arguments={"remote": {"type": "mysql"}, "subnets-action": "keep",
                                                         "shared-networks": [{"name": "net1"}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv6 shared network(s) deleted."}

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]}, "name": "net2"}]},
                        "result": 0, "text": "1 IPv6 shared network(s) found."}

    # after deleting network we still want to have 2 subnets
    cmd = dict(command="remote-subnet6-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2,
                                      "subnets": [{"id": 1, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "2001:db8:1::/64"},
                                                  {"id": 2, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": "net2", "subnet": "2001:db8:2::/64"}]},
                        "result": 0, "text": "2 IPv6 subnet(s) found."}

    cmd = dict(command="remote-network6-del", arguments={"remote": {"type": "mysql"}, "subnets-action": "keep",
                                                         "shared-networks": [{"name": "net2"}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv6 shared network(s) deleted."}

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv6 shared network(s) found."}

    # after removing all networks we still want to have both subnets
    cmd = dict(command="remote-subnet6-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2,
                                      "subnets": [{"id": 1, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "2001:db8:1::/64"},
                                                  {"id": 2, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": None, "subnet": "2001:db8:2::/64"}]},
                        "result": 0, "text": "2 IPv6 subnet(s) found."}


def test_remote_network6_del_subnet_delete():
    # add networks
    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net1",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-network6-set", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"],
                                                         "shared-networks": [{
                                                             "name": "net2",
                                                             "interface": "$(SERVER_IFACE)"}]})
    srv_msg.send_ctrl_cmd(cmd)

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 2,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]},
                                                           "name": "net1"},
                                                          {"metadata": {"server-tags": ["abc"]},
                                                           "name": "net2"}]},
                        "result": 0,
                        "text": "2 IPv6 shared network(s) found."}

    # add subnets to networks
    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:1::/64", "id": 1,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "net1",
                                                                     "pools": [{
                                                                         "pool": "2001:db8:1::1-2001:db8:1::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 1, "subnet": "2001:db8:1::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    cmd = dict(command="remote-subnet6-set", arguments={"remote": {"type": "mysql"},
                                                        "server-tags": ["abc"],
                                                        "subnets": [{"subnet": "2001:db8:2::/64", "id": 2,
                                                                     "interface": "$(SERVER_IFACE)",
                                                                     "shared-network-name": "net2",
                                                                     "pools": [{
                                                                         "pool": "2001:db8:2::1-2001:db8:2::10"}]}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"subnets": [{"id": 2, "subnet": "2001:db8:2::/64"}]},
                        "result": 0, "text": "IPv6 subnet successfully set."}

    # we want to have 2 subnets
    cmd = dict(command="remote-subnet6-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2, "subnets": [{"id": 1, "subnet": "2001:db8:1::/64",
                                                               "shared-network-name": "net1",
                                                               "metadata": {"server-tags": ["abc"]}},
                                                              {"id": 2, "subnet": "2001:db8:2::/64",
                                                               "shared-network-name": "net2",
                                                               "metadata": {"server-tags": ["abc"]}}]},
                        "result": 0, "text": "2 IPv6 subnet(s) found."}

    cmd = dict(command="remote-network6-del", arguments={"remote": {"type": "mysql"}, "subnets-action": "delete",
                                                         "shared-networks": [{"name": "net1"}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv6 shared network(s) deleted."}

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "shared-networks": [{"metadata": {"server-tags": ["abc"]}, "name": "net2"}]},
                        "result": 0, "text": "1 IPv6 shared network(s) found."}

    # after deleting network we still want to have 2 subnets
    cmd = dict(command="remote-subnet6-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "subnets": [{"id": 2, "metadata": {"server-tags": ["abc"]},
                                                   "shared-network-name": "net2", "subnet": "2001:db8:2::/64"}]},
                        "result": 0, "text": "1 IPv6 subnet(s) found."}

    cmd = dict(command="remote-network6-del", arguments={"remote": {"type": "mysql"}, "subnets-action": "delete",
                                                         "shared-networks": [{"name": "net2"}]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 IPv6 shared network(s) deleted."}

    cmd = dict(command="remote-network6-list", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0,
                                      "shared-networks": []},
                        "result": 3,
                        "text": "0 IPv6 shared network(s) found."}

    # all subnets should be removed now
    cmd = dict(command="remote-subnet6-list", arguments={"remote": {"type": "mysql"},
                                                         "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "subnets": []},
                        "result": 3, "text": "0 IPv6 subnet(s) found."}


def _set_global_parameter():
    cmd = dict(command="remote-global-parameter6-set", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": {
                                                                      "decline-probation-period": 123456}})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "parameters": {"decline-probation-period": 123456}},
                        "result": 0,
                        "text": "1 DHCPv6 global parameter(s) successfully set."}


# global-parameter tests
def test_remote_global_parameter6_set_integer():
    cmd = dict(command="remote-global-parameter6-set", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": {"valid-lifetime": 1000}})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "parameters": {"valid-lifetime": 1000}},
                        "result": 0,
                        "text": "1 DHCPv6 global parameter(s) successfully set."}


def test_remote_global_parameter6_set_incorrect_parameter():
    cmd = dict(command="remote-global-parameter6-set", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": {"decline-aaa-period": 1234556}})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "unknown parameter 'decline-aaa-period'"}


def test_remote_global_parameter6_del():
    _set_global_parameter()

    cmd = dict(command="remote-global-parameter6-del", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": ["decline-probation-period"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1},
                        "result": 0, "text": "1 DHCPv6 global parameter(s) deleted."}


def test_remote_global_parameter6_del_not_existing_parameter():
    cmd = dict(command="remote-global-parameter6-del", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": ["decline-probation-period"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0},
                        "result": 3, "text": "0 DHCPv6 global parameter(s) deleted."}


def test_remote_global_parameter6_get():
    _set_global_parameter()

    cmd = dict(command="remote-global-parameter6-get", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": ["decline-probation-period"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1,
                                      "parameters": {"decline-probation-period": 123456,
                                                     "metadata": {"server-tags": ["abc"]}}},
                        "result": 0, "text": "'decline-probation-period' DHCPv6 global parameter found."}


def test_remote_global_parameter6_get_all_one():
    _set_global_parameter()

    cmd = dict(command="remote-global-parameter6-get-all", arguments={"remote": {"type": "mysql"},
                                                                      "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "parameters": [{"decline-probation-period": 123456,
                                                                  "metadata": {"server-tags": ["abc"]}}]},
                        "result": 0, "text": "1 DHCPv6 global parameter(s) found."}


def test_remote_global_parameter6_get_all_multiple():
    _set_global_parameter()

    cmd = dict(command="remote-global-parameter6-set", arguments={"remote": {"type": "mysql"},
                                                                  "server-tags": ["abc"],
                                                                  "parameters": {"calculate-tee-times": True}})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 1, "parameters": {"calculate-tee-times": True}},
                        "result": 0,
                        "text": "1 DHCPv6 global parameter(s) successfully set."}

    cmd = dict(command="remote-global-parameter6-get-all", arguments={"remote": {"type": "mysql"},
                                                                      "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response["result"] == 0
    assert response["text"] == "2 DHCPv6 global parameter(s) found."
    assert response["arguments"]["count"] == 2
    assert {"calculate-tee-times": True, "metadata": {"server-tags": ["abc"]}} in response["arguments"]["parameters"]
    assert {"decline-probation-period": 123456,
            "metadata": {"server-tags": ["abc"]}} in response["arguments"]["parameters"]


def test_remote_global_parameter6_get_all_zero():
    cmd = dict(command="remote-global-parameter6-get-all", arguments={"remote": {"type": "mysql"},
                                                                      "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "parameters": []},
                        "result": 3, "text": "0 DHCPv6 global parameter(s) found."}


def _set_option_def(channel='http'):
    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32"}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "dhcp6"}]},
                        "result": 0, "text": "DHCPv6 option definition successfully set."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_option_def6_set_basic(channel):
    _set_option_def(channel)


def test_remote_option_def6_set_using_zero_as_code():
    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 0,
                                                                "type": "uint32"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "invalid option code 0: reserved value" in response["text"]


def test_remote_option_def6_set_using_standard_code():
    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 24,
                                                                "type": "uint32"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "an option with code 24 already exists in space 'dhcp6'"}


def test_remote_option_def6_set_missing_parameters():
    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "array": False,
                                                                "record-types": "",
                                                                "space": "dhcp6",
                                                                "encapsulate": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "missing parameter 'name'" in response["text"]

    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "aa",
                                                                "type": "uint32",
                                                                "array": False,
                                                                "record-types": "",
                                                                "space": "dhcp6",
                                                                "encapsulate": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "missing parameter 'code'" in response["text"]

    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "aa",
                                                                "code": 234,
                                                                "array": False,
                                                                "record-types": "",
                                                                "space": "dhcp6",
                                                                "encapsulate": ""}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "missing parameter 'type'" in response["text"]


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_option_def6_get_basic(channel):
    _set_option_def()

    cmd = dict(command="remote-option-def6-get", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "code": 222}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "name": "foo", "record-types": "", "space": "dhcp6",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "DHCPv6 option definition 222 in 'dhcp6' found."}


def test_remote_option_def6_get_multiple_defs():
    _set_option_def()

    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv6 option definition successfully set."}

    cmd = dict(command="remote-option-def6-get", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "code": 222,
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "name": "foo", "record-types": "", "space": "abc",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "DHCPv6 option definition 222 in 'abc' found."}


def test_remote_option_def6_get_missing_code():
    cmd = dict(command="remote-option-def6-get", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert response == {"result": 1, "text": "missing 'code' parameter"}


def test_remote_option_def6_get_all_option_not_defined():
    cmd = dict(command="remote-option-def6-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)

    assert response == {"arguments": {"count": 0, "option-defs": []},
                        "result": 3, "text": "0 DHCPv6 option definition(s) found."}


def test_remote_option_def6_get_all_multiple_defs():
    _set_option_def()

    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv6 option definition successfully set."}

    cmd = dict(command="remote-option-def6-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 2, "option-defs": [{"array": False, "code": 222,
                                                                   "encapsulate": "", "name": "foo",
                                                                   "record-types": "", "space": "abc",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "type": "uint32"},
                                                                  {"array": False, "code": 222,
                                                                   "encapsulate": "", "name": "foo",
                                                                   "record-types": "", "space": "dhcp6",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "2 DHCPv6 option definition(s) found."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_option_def6_get_all_basic(channel):
    _set_option_def()

    cmd = dict(command="remote-option-def6-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "name": "foo", "record-types": "", "space": "dhcp6",
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "1 DHCPv6 option definition(s) found."}


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_option_def6_del_basic(channel):
    _set_option_def()

    cmd = dict(command="remote-option-def6-del", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"],
                                                            "option-defs": [{"code": 222}]})

    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv6 option definition(s) deleted."}


def test_remote_option_def6_del_different_space():
    _set_option_def()

    cmd = dict(command="remote-option-def6-del", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"],
                                                            "option-defs": [{"code": 222, "space": "abc"}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv6 option definition(s) deleted."}


def test_remote_option_def6_del_incorrect_code():
    cmd = dict(command="remote-option-def6-del", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"], "option-defs": [{"name": 22}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}

    cmd = dict(command="remote-option-def6-del", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"], "option-defs": [{}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}

    cmd = dict(command="remote-option-def6-del", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{"code": "abc"}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


def test_remote_option_def6_del_missing_option():
    cmd = dict(command="remote-option-def6-del", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{"code": 212}]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv6 option definition(s) deleted."}


def test_remote_option_def6_del_multiple_options():
    _set_option_def()

    cmd = dict(command="remote-option-def6-set", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{
                                                                "name": "foo",
                                                                "code": 222,
                                                                "type": "uint32",
                                                                "space": "abc"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"option-defs": [{"code": 222, "space": "abc"}]},
                        "result": 0, "text": "DHCPv6 option definition successfully set."}

    cmd = dict(command="remote-option-def6-del", arguments={"remote": {"type": "mysql"},
                                                            "server-tags": ["abc"],
                                                            "option-defs": [{"code": 222}]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv6 option definition(s) deleted."}

    cmd = dict(command="remote-option-def6-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "option-defs": [{"array": False, "code": 222, "encapsulate": "",
                                                                   "metadata": {"server-tags": ["abc"]},
                                                                   "name": "foo", "record-types": "", "space": "abc",
                                                                   "type": "uint32"}]},
                        "result": 0, "text": "1 DHCPv6 option definition(s) found."}


def _set_global_option(channel='http'):
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 7,
                                                                   "data": "123"}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)

    assert response == {"result": 0, "text": "DHCPv6 option successfully set.",
                        "arguments": {"options": [{"code": 7, "space": "dhcp6"}]}}


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_global_option6_global_set_basic(channel):
    _set_global_option(channel)


def test_remote_global_option6_global_set_missing_data():
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 7}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "no option value specified" in response["text"]


def test_remote_global_option6_global_set_name():
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "name": "sip-server-dns",
                                                                   "data": "isc.example.com"}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"options": [{"code": 21, "space": "dhcp6"}]},
                        "result": 0, "text": "DHCPv6 option successfully set."}


def test_remote_global_option6_global_set_incorrect_code_missing_name():
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": "aaa"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert "'code' parameter is not an integer" in response["text"]


def test_remote_global_option6_global_set_incorrect_name_missing_code():
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "name": 123}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "'name' parameter is not a string" in response["text"]


def test_remote_global_option6_global_set_missing_code_and_name():
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "option data configuration requires one of 'code' or 'name' parameters to be specified" in response["text"]


def test_remote_global_option6_global_set_incorrect_code():
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "aa",
                                                                            "name": "cc"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "'code' parameter is not an integer" in response["text"]


def test_remote_global_option6_global_set_incorrect_name():
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 7,
                                                                            "name": 7,
                                                                            "data": "123"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "'name' parameter is not a string" in response["text"]


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_global_option6_global_get_basic(channel):
    _set_global_option()

    cmd = dict(command="remote-option6-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 7}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": False, "code": 7, "csv-format": True,
                                                               "data": "123",
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "name": "preference", "space": "dhcp6"}]},
                        "result": 0, "text": "DHCPv6 option 7 in 'dhcp6' found."}


def test_remote_global_option6_global_set_different_space():
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 7,
                                                                            "data": "123",
                                                                            "always-send": True,
                                                                            "csv-format": True,
                                                                            "space": "xyz"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "definition for the option 'xyz.' having code 7 does not exist" in response["text"]


def test_remote_global_option6_global_set_csv_false_incorrect():
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 7,
                                                                            "data": "12Z3",
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "option data is not a valid string of hexadecimal digits: 12Z3" in response["text"]


def test_remote_global_option6_global_set_csv_false_incorrect_hex():
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 7,
                                                                            "data": "C0000201Z",
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)

    assert "option data is not a valid string of hexadecimal digits: C0000201Z" in response["text"]


@pytest.mark.parametrize('channel', ['socket', 'http'])
def test_remote_global_option6_global_del_basic(channel):
    _set_global_option()

    cmd = dict(command="remote-option6-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 7}]})
    response = srv_msg.send_ctrl_cmd(cmd, channel=channel)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv6 option(s) deleted."}


def test_remote_global_option6_global_del_missing_code():
    cmd = dict(command="remote-option6-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"ab": 7}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}


def test_remote_global_option6_global_del_incorrect_code():
    cmd = dict(command="remote-option6-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "7"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


def test_remote_global_option6_global_del_missing_option():
    cmd = dict(command="remote-option6-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 7}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0}, "result": 3, "text": "0 DHCPv6 option(s) deleted."}


def test_remote_global_option6_global_get_missing_code():
    cmd = dict(command="remote-option6-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"ab": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "missing 'code' parameter"}


def test_remote_global_option6_global_get_incorrect_code():
    cmd = dict(command="remote-option6-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": "7"}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=1)
    assert response == {"result": 1, "text": "'code' parameter is not an integer"}


def test_remote_global_option6_global_get_missing_option():
    cmd = dict(command="remote-option6-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 6}]})
    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0, "options": []},
                        "result": 3, "text": "DHCPv6 option 6 in 'dhcp6' not found."}


def test_remote_global_option6_global_get_csv_false():
    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 22,
                                                                            "data": "C0000301C0000302",
                                                                            "always-send": True,
                                                                            "csv-format": False}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv6 option successfully set.",
                        "arguments": {"options": [{"code": 7, "space": "dhcp6"}]}}

    cmd = dict(command="remote-option6-global-get", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 22}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": True, "code": 22, "csv-format": False,
                                                               "data": "C0000301C0000302",
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "name": "sip-server-addr", "space": "dhcp6"}]},
                        "result": 0, "text": "DHCPv6 option 6 in 'dhcp6' found."}


def test_remote_global_option6_global_get_all():
    _set_global_option()

    cmd = dict(command="remote-option6-global-set", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{
                                                                   "code": 22,
                                                                   "data": "2001:db8::2"}]})
    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"result": 0, "text": "DHCPv6 option successfully set.",
                        "arguments": {"options": [{"code": 22, "space": "dhcp6"}]}}

    cmd = dict(command="remote-option6-global-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)

    assert response == {"arguments": {"count": 2,
                                      "options": [{"always-send": False, "code": 7, "csv-format": True,
                                                   "metadata": {"server-tags": ["abc"]},
                                                   "data": "123", "name": "preference",
                                                   "space": "dhcp6"},
                                                  {"always-send": False, "code": 22, "csv-format": True,
                                                   "metadata": {"server-tags": ["abc"]},
                                                   "data": "2001:db8::2", "name": "sip-server-addr",
                                                   "space": "dhcp6"}]},
                        "result": 0, "text": "2 DHCPv6 option(s) found."}

    cmd = dict(command="remote-option6-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 7}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv6 option(s) deleted."}

    cmd = dict(command="remote-option6-global-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1, "options": [{"always-send": False, "code": 22, "csv-format": True,
                                                               "data": "2001:db8::2", "name": "sip-server-addr",
                                                               "metadata": {"server-tags": ["abc"]},
                                                               "space": "dhcp6"}]},
                        "result": 0, "text": "1 DHCPv6 option(s) found."}

    cmd = dict(command="remote-option6-global-del", arguments={"remote": {"type": "mysql"},
                                                               "server-tags": ["abc"],
                                                               "options": [{"code": 22}]})
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {"arguments": {"count": 1}, "result": 0, "text": "1 DHCPv6 option(s) deleted."}

    cmd = dict(command="remote-option6-global-get-all", arguments={"remote": {"type": "mysql"}, "server-tags": ["abc"]})

    response = srv_msg.send_ctrl_cmd(cmd, exp_result=3)
    assert response == {"arguments": {"count": 0, "options": []}, "result": 3, "text": "0 DHCPv6 option(s) found."}
