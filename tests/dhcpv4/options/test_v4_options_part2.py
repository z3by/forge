"""DHCPv4 options part2"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_control
import srv_msg


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_path_mtu_plateau_table():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('path-mtu-plateau-table', '100,300,500')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(25)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'value', 100)
    srv_msg.response_check_option_content(25, 'value', 300)
    srv_msg.response_check_option_content(25, 'value', 500)


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_interface_mtu():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('interface-mtu', '321')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(26)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(26)
    srv_msg.response_check_option_content(26, 'value', '321')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_broadcast_address():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('broadcast-address', '255.255.255.0')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(28)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(28)
    srv_msg.response_check_option_content(28, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_router_solicitation_address():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('router-solicitation-address', '199.199.199.1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(32)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(32)
    srv_msg.response_check_option_content(32, 'value', '199.199.199.1')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_static_routes():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('static-routes', '199.199.199.1,70.70.70.1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(33)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(33)
    srv_msg.response_check_option_content(33, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(33, 'value', '70.70.70.1')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_arp_cache_timeout():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('arp-cache-timeout', '48')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(35)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(35)
    srv_msg.response_check_option_content(35, 'value', 48)


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_default_tcp_ttl():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('default-tcp-ttl', '44')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(37)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(37)
    srv_msg.response_check_option_content(37, 'value', 44)


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_tcp_keepalive_interval():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('tcp-keepalive-interval', '4896')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(38)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(38)
    srv_msg.response_check_option_content(38, 'value', '4896')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_nis_domain():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('nis-domain', 'some.domain.com')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(40)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(40)
    srv_msg.response_check_option_content(40, 'value', 'some.domain.com')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_nis_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('nis-servers', '199.199.199.1,100.100.100.15')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(41)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(41)
    srv_msg.response_check_option_content(41, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(41, 'value', '100.100.100.15')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_ntp_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('ntp-servers', '199.199.199.1,100.100.100.15')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(42)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(42)
    srv_msg.response_check_option_content(42, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(42, 'value', '100.100.100.15')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_netbios_name_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('netbios-name-servers', '188.188.188.2,100.100.100.15')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(44)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(44)
    srv_msg.response_check_option_content(44, 'value', '188.188.188.2')
    srv_msg.response_check_option_content(44, 'value', '100.100.100.15')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_netbios_dd_server():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('netbios-dd-server', '188.188.188.2,70.70.70.1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(45)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(45)
    srv_msg.response_check_option_content(45, 'value', '188.188.188.2')
    srv_msg.response_check_option_content(45, 'value', '70.70.70.1')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_netbios_node_type():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('netbios-node-type', '8')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(46)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(46)
    srv_msg.response_check_option_content(46, 'value', 8)


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_netbios_scope():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('netbios-scope', 'global')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(47)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(47)
    srv_msg.response_check_option_content(47, 'value', 'global')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_font_servers():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('font-servers', '188.188.188.2,100.100.100.1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(48)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(48)
    srv_msg.response_check_option_content(48, 'value', '188.188.188.2')
    srv_msg.response_check_option_content(48, 'value', '100.100.100.1')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_x_display_manager():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('x-display-manager', '188.188.188.2,150.150.150.10')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(49)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(49)
    srv_msg.response_check_option_content(49, 'value', '188.188.188.2')
    srv_msg.response_check_option_content(49, 'value', '150.150.150.10')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_dhcp_requested_address():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('dhcp-requested-address', '188.188.188.2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(50)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(50)
    srv_msg.response_check_option_content(50, 'value', '188.188.188.2')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_dhcp_option_overload():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('dhcp-option-overload', '1')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(52)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(52)
    srv_msg.response_check_option_content(52, 'value', 1)


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_dhcp_message():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('dhcp-message', 'some-message')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(56)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(56)
    srv_msg.response_check_option_content(56, 'value', 'some-message')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_dhcp_max_message_size():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('dhcp-max-message-size', '2349')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(57)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(57)
    srv_msg.response_check_option_content(57, 'value', '2349')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_renew_timer():

    misc.test_setup()
    srv_control.set_time('renew-timer', 999)
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(58)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(58)
    srv_msg.response_check_option_content(58, 'value', 999)


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_rebind_timer():

    misc.test_setup()
    srv_control.set_time('rebind-timer', '1999')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(59)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(59)
    srv_msg.response_check_option_content(59, 'value', '1999')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_nwip_domain_name():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('nwip-domain-name', 'some.domain.com')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(62)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(62)
    srv_msg.response_check_option_content(62, 'value', 'some.domain.com')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_boot_file_name():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('boot-file-name', 'somefilename')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(67)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(67)
    srv_msg.response_check_option_content(67, 'value', 'somefilename')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_client_last_transaction_time():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('client-last-transaction-time', '3424')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(91)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(91)
    srv_msg.response_check_option_content(91, 'value', 3424)


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_associated_ip():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('associated-ip', '188.188.188.2,199.188.188.12')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(92)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(92)
    srv_msg.response_check_option_content(92, 'value', '188.188.188.2')
    srv_msg.response_check_option_content(92, 'value', '199.188.188.12')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.subnet
def test_v4_options_subnet_selection():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')
    srv_control.config_srv_opt('subnet-selection', '188.188.188.2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option(118)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(118)
    srv_msg.response_check_option_content(118, 'value', '188.188.188.2')
