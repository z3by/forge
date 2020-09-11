import pytest

import srv_msg
import srv_control
import misc

from forge_cfg import world


@pytest.mark.v6
@pytest.mark.flex_options
def test_flex_options_add():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.add_hooks('libdhcp_flex_option.so')

    world.dhcp_cfg["hooks-libraries"][0].update(
        {
            "parameters": {
                "options": [
                    {
                        "code": 31,
                        "add": "ifelse(option[39].exists,3000::1,3000::2)"
                    }
                ]
            }
        }
    )
    srv_control.build_and_send_config_files('SSH', 'configfile')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(31)
    srv_msg.response_check_option_content(31, 'value', '3000::1')
    srv_msg.response_check_option_content(31, 'value', '3000::2', expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(31)
    srv_msg.response_check_option_content(31, 'value', '3000::2')
    srv_msg.response_check_option_content(31, 'value', '3000::1', expect_include=False)


@pytest.mark.v6
@pytest.mark.flex_options
def test_flex_options_remove():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_opt('nisp-domain-name', 'ntp.example.com')
    srv_control.add_hooks('libdhcp_flex_option.so')

    world.dhcp_cfg["hooks-libraries"][0].update(
        {
            "parameters": {
                "options": [
                    {
                        "code": 30,
                        "remove": "option[39].exists"
                    }
                ]
            }
        }
    )
    srv_control.build_and_send_config_files('SSH', 'configfile')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_requests_option(30)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(30, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_requests_option(30)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(30)
    srv_msg.response_check_option_content(30, 'value', 'ntp.example.com.')


@pytest.mark.v6
@pytest.mark.flex_options
def test_flex_options_remove_non_existing():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.add_hooks('libdhcp_flex_option.so')

    world.dhcp_cfg["hooks-libraries"][0].update(
        {
            "parameters": {
                "options": [
                    {
                        "code": 30,
                        "remove": "option[39].exists"
                    }
                ]
            }
        }
    )
    srv_control.build_and_send_config_files('SSH', 'configfile')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_requests_option(30)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(30, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_requests_option(30)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(30, expect_include=False)


@pytest.mark.v6
@pytest.mark.flex_options
def test_flex_options_supersede_domain():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_opt('nisp-domain-name', 'ntp.example.com')
    srv_control.add_hooks('libdhcp_flex_option.so')

    world.dhcp_cfg["hooks-libraries"][0].update(
        {
            "parameters": {
                "options": [
                    {
                        "code": 30,
                        "supersede": "ifelse(relay6[0].peeraddr == 3000::1005, 'ntp2.notexample.com','')"
                    }
                ]
            }
        }
    )
    srv_control.build_and_send_config_files('SSH', 'configfile')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(30)
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'peeraddr', '3000::1005')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(30)
    srv_msg.response_check_option_content(30, 'value', 'ntp2.notexample.com.')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(30)
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'peeraddr', '3000::1')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(30)
    srv_msg.response_check_option_content(30, 'value', 'ntp.example.com.')


@pytest.mark.v6
@pytest.mark.flex_options
def test_flex_options_supersede_string():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_opt('new-posix-timezone', 'EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00')
    srv_control.add_hooks('libdhcp_flex_option.so')

    world.dhcp_cfg["hooks-libraries"][0].update(
        {
            "parameters": {
                "options": [
                    {
                        "code": 41,
                        "supersede": "ifelse(relay6[0].peeraddr == 3000::1005,"
                                     r"'EST5EDT4\,M3.2.0/02:00\,M11.1.0/02:00','')"
                    }
                ]
            }
        }
    )
    srv_control.build_and_send_config_files('SSH', 'configfile')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(41)
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'peeraddr', '3000::1005')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(41)
    srv_msg.response_check_option_content(41, 'optdata', r'EST5EDT4,M3.2.0/02:00,M11.1.0/02:00')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(41)
    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'peeraddr', '3000::1')
    srv_msg.client_sets_value('RelayAgent', 'ifaceid', 'abc')
    srv_msg.client_does_include('RelayAgent', 'interface-id')
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(18)
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    srv_msg.response_check_include_option(41)
    srv_msg.response_check_option_content(41, 'optdata', r'EST5EDT4,M3.2.0/02:00,M11.1.0/02:00')


@pytest.mark.v6
@pytest.mark.flex_options
def test_flex_options_all_actions():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.config_srv_opt('nisp-domain-name', 'ntp.example.com')
    srv_control.config_srv_opt('new-posix-timezone', 'EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00')
    srv_control.add_hooks('libdhcp_flex_option.so')

    world.dhcp_cfg["hooks-libraries"][0].update(
        {
            "parameters": {
                "options": [
                    {
                        # new-posix-timezone if vendor exist
                        "code": 41,
                        "supersede": "ifelse(vendor[*].exists, 'EST5\\,M4.3.0/02:00\\,M13.2.0/02:00','')"
                    },
                    {
                        # remove option 30 nisp-domain-name if client has a reservation
                        "code": 30,
                        "remove": "member('KNOWN')"
                    },
                    {
                        # if fqdn is present add sip-server-addr 3000::1 if not add sntp-servers 3000::2
                        "code": 22,
                        "add": "ifelse(option[39].exists,3000::1,3000::2)"
                    }
                ]
            }
        }
    )
    world.dhcp_cfg["subnet6"][0].update(
        {
            "reservations": [
                {
                    "ip-addresses": ["2001:db8:1::1000"],
                    "hw-address": "01:02:03:04:05:06"
                }
            ]
        }
    )

    srv_control.build_and_send_config_files('SSH', 'configfile')
    srv_control.start_srv('DHCP', 'started')

    # this client will trigger one change
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:01:02:03:04:05:07')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(41)
    srv_msg.client_requests_option(30)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(41)
    srv_msg.response_check_option_content(41, 'optdata', r'EST5EDT4,M3.2.0/02:00,M11.1.0/02:00')
    srv_msg.response_check_include_option(30)
    srv_msg.response_check_option_content(30, 'value', 'ntp.example.com.')
    srv_msg.response_check_include_option(22)
    srv_msg.response_check_option_content(22, 'addresses', '3000::2')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:01:02:03:04:05:07')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(41)
    srv_msg.client_requests_option(30)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(41)
    srv_msg.response_check_option_content(41, 'optdata', r'EST5EDT4,M3.2.0/02:00,M11.1.0/02:00')
    srv_msg.response_check_include_option(30)
    srv_msg.response_check_option_content(30, 'value', 'ntp.example.com.')
    srv_msg.response_check_include_option(22)
    srv_msg.response_check_option_content(22, 'addresses', '3000::2')

    # client will trigger all changes
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_requests_option(41)
    srv_msg.client_requests_option(30)
    srv_msg.client_requests_option(22)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(30, expect_include=False)
    srv_msg.response_check_include_option(41)
    srv_msg.response_check_option_content(41, 'optdata', r'EST5,M4.3.0/02:00,M13.2.0/02:00')
    srv_msg.response_check_include_option(22)
    srv_msg.response_check_option_content(22, 'addresses', '3000::1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'enterprisenum', '4491')
    srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.add_vendor_suboption('Client', 1026, '01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'vendor-specific-info')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:01:02:03:04:05:06')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'some-different-name')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_requests_option(41)
    srv_msg.client_requests_option(30)
    srv_msg.client_requests_option(22)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1000')
    srv_msg.response_check_include_option(30, expect_include=False)
    srv_msg.response_check_include_option(41)
    srv_msg.response_check_option_content(41, 'optdata', r'EST5,M4.3.0/02:00,M13.2.0/02:00')
    srv_msg.response_check_include_option(22)
    srv_msg.response_check_option_content(22, 'addresses', '3000::1')