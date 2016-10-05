
@v6
Scenario: 7550_1
Test Setup:
Time preferred-lifetime is configured with value 300.
Time valid-lifetime is configured with value 400.
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.

#subnet declarations:
#Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::100-2001:db8:1::200 pool.
Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
Server is configured with 3001:: prefix in subnet 0 with 64 prefix length and 96 delegated prefix length.
#Server is configured with another subnet on interface <interface> with 2001:db8:2::/64 subnet and 2001:db8:2::100-2001:db8:2::200 pool.
#Server is configured with 3002:: prefix in subnet 1 with 64 prefix length and 96 delegated prefix length.

#logger declarations (one is commented as and example)
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
#Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.

#enable 7550 support
Add to config file line: "new-leases-on-renew": False

#start server:
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
#Pause the Test.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 13.
Response sub-option 13 from option 3 MUST contain statuscode 2.

References: RFC 7550 Section 4.1. - Status Code placement

@v6
Scenario: 7550_2
Test Setup:
Time preferred-lifetime is configured with value 300.
Time valid-lifetime is configured with value 400.
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.

#subnet declarations:
#Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::100-2001:db8:1::200 pool.
Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
#Server is configured with another subnet on interface <interface> with 2001:db8:2::/64 subnet and 2001:db8:2::100-2001:db8:2::200 pool.
#Server is configured with 3002:: prefix in subnet 1 with 64 prefix length and 96 delegated prefix length.

#logger declarations (one is commented as and example)
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
#Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.

#enable 7550 support
Add to config file line: "new-leases-on-renew": True

#start server:
DHCP server is started.

Test Procedure:
Client does include IA-PD.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include IA-PD.
Client sends RENEW message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.
Response MUST include option 25.
Response option 25 MUST contain sub-option 26.

@v6
Scenario: 7550_3
Test Setup:
Time preferred-lifetime is configured with value 300.
Time valid-lifetime is configured with value 400.
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.

#subnet declarations:
#Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::100-2001:db8:1::200 pool.
Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
#Server is configured with another subnet on interface <interface> with 2001:db8:2::/64 subnet and 2001:db8:2::100-2001:db8:2::200 pool.
#Server is configured with 3002:: prefix in subnet 1 with 64 prefix length and 96 delegated prefix length.

#logger declarations (one is commented as and example)
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
#Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.

#enable 7550 support
Add to config file line: "new-leases-on-renew": True

#start server:
DHCP server is started.




Test Procedure:
Client requests option 7.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client copies IA_NA option from received message.
Client copies server-id option from received message.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client copies IA_NA option from received message.
Client does include IA-PD.
Client sends REBIND message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.
Response MUST include option 25.
Response option 25 MUST contain sub-option 26.

@v6
Scenario: 7550_4
Test Setup:
Time preferred-lifetime is configured with value 300.
Time valid-lifetime is configured with value 400.
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.

#subnet declarations:
#Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::100-2001:db8:1::200 pool.
Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
#Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
#Server is configured with another subnet on interface <interface> with 2001:db8:2::/64 subnet and 2001:db8:2::100-2001:db8:2::200 pool.
#Server is configured with 3002:: prefix in subnet 1 with 64 prefix length and 96 delegated prefix length.

#logger declarations (one is commented as and example)
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
#Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.

#enable 7550 support
Add to config file line: "new-leases-on-renew": True

#start server:
DHCP server is started.




Test Procedure:
Client requests option 7.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client copies IA_NA option from received message.
Client copies server-id option from received message.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client copies IA_NA option from received message.
Client does include IA-PD.
Client sends REBIND message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.
Response MUST include option 25.
Response option 25 MUST contain sub-option 13.
@v6
Scenario: 7550_5
Test Setup:
Time preferred-lifetime is configured with value 300.
Time valid-lifetime is configured with value 400.
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.

#subnet declarations:
#Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::100-2001:db8:1::200 pool.
Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
#Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
#Server is configured with another subnet on interface <interface> with 2001:db8:2::/64 subnet and 2001:db8:2::100-2001:db8:2::200 pool.
#Server is configured with 3002:: prefix in subnet 1 with 64 prefix length and 96 delegated prefix length.

#logger declarations (one is commented as and example)
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
#Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.

#enable 7550 support
Add to config file line: "new-leases-on-renew": True

#start server:
DHCP server is started.

Test Procedure:
#Client does include IA-PD.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include IA-PD.
Client sends RENEW message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.
Response MUST include option 25.
Response option 25 MUST contain sub-option 13.

@v6
Scenario: 7550_6
Test Setup:
Time preferred-lifetime is configured with value 300.
Time valid-lifetime is configured with value 400.
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.

#subnet declarations:
#Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::100-2001:db8:1::200 pool.
Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
#Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
#Server is configured with another subnet on interface <interface> with 2001:db8:2::/64 subnet and 2001:db8:2::100-2001:db8:2::200 pool.
#Server is configured with 3002:: prefix in subnet 1 with 64 prefix length and 96 delegated prefix length.

#logger declarations (one is commented as and example)
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
#Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.

#enable 7550 support
Add to config file line: "new-leases-on-renew": True

#start server:
DHCP server is started.

Test Procedure:
#Client does include IA-PD.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client sets T1 value to 0.
Client sets T2 value to 0.
Client sets validlft value to 0.
Client sets plen value to 96.
Client sets prefix value to ::.
Client does include IA_Prefix.
Client sends RENEW message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.
Response MUST include option 25.
Response option 25 MUST contain sub-option 13.


@v6
Scenario: 7550_7
Test Setup:
Time preferred-lifetime is configured with value 300.
Time valid-lifetime is configured with value 400.
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
#subnet declarations:
#Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::100-2001:db8:1::200 pool.
Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
#Server is configured with another subnet on interface <interface> with 2001:db8:2::/64 subnet and 2001:db8:2::100-2001:db8:2::200 pool.
#Server is configured with 3002:: prefix in subnet 1 with 64 prefix length and 96 delegated prefix length.
#logger declarations (one is commented as and example)
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
#Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
Add to config file line: "new-leases-on-renew": True

#start server:
DHCP server is started.

Test Procedure:
#Client does include IA-PD.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client sets T1 value to 0.
Client sets T2 value to 0.
Client sets validlft value to 0.
Client sets plen value to 96.
Client sets prefix value to 3001::1:0:0.
Client does include IA_Prefix.
# Client does include IA-PD.
Client sends RENEW message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.
Response MUST include option 25.
#Response option 25 MUST contain sub-option 13.

Test Procedure:
#Client does include IA-PD.
# Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
#       Client sends SOLICIT message.

Pass Criteria:
#      Server MUST respond with ADVERTISE message.

@v6
Scenario: 7550_8
Test Setup:
Time preferred-lifetime is configured with value 300.
Time valid-lifetime is configured with value 400.

Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.

#subnet declarations:
#Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::100-2001:db8:1::200 pool.
Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
#Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
#Server is configured with another subnet on interface <interface> with 2001:db8:2::/64 subnet and 2001:db8:2::100-2001:db8:2::200 pool.
#Server is configured with 3002:: prefix in subnet 1 with 64 prefix length and 96 delegated prefix length.

#logger declarations (one is commented as and example)
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
#Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.

#enable 7550 support
Add to config file line: "new-leases-on-renew": True

#start server:
DHCP server is started.

Test Procedure:
#Client does include IA-PD.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client sets T1 value to 0.
Client sets T2 value to 0.
Client sets validlft value to 0.
Client sets plen value to 96.
Client sets prefix value to ::.
#Client sets prefix value to 3000::1:0:0.
Client does include IA_Prefix.
Client sends REBIND message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.
Response MUST include option 25.
Response option 25 MUST contain sub-option 13.


@v6
Scenario: 7550_9
Test Setup:
Time preferred-lifetime is configured with value 300.
Time valid-lifetime is configured with value 400.
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
#subnet declarations:
#Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::100-2001:db8:1::200 pool.
Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
#Server is configured with another subnet on interface <interface> with 2001:db8:2::/64 subnet and 2001:db8:2::100-2001:db8:2::200 pool.
#Server is configured with 3002:: prefix in subnet 1 with 64 prefix length and 96 delegated prefix length.
#logger declarations (one is commented as and example)
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
#Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
Add to config file line: "new-leases-on-renew": True

#start server:
DHCP server is started.

Test Procedure:
#Client does include IA-PD.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client sets T1 value to 0.
Client sets T2 value to 0.
Client sets validlft value to 0.
Client sets plen value to 96.
Client sets prefix value to 3001::1:0:0.
Client does include IA_Prefix.
# Client does include IA-PD.
Client sends REBIND message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.
Response MUST include option 25.

@v6
Scenario: 7550_10
Test Setup:
Time preferred-lifetime is configured with value 300.
Time valid-lifetime is configured with value 400.
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
#subnet declarations:
#Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::100-2001:db8:1::200 pool.
Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
#Server is configured with another subnet on interface <interface> with 2001:db8:2::/64 subnet and 2001:db8:2::100-2001:db8:2::200 pool.
#Server is configured with 3002:: prefix in subnet 1 with 64 prefix length and 96 delegated prefix length.
#logger declarations (one is commented as and example)
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
#Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
Add to config file line: "new-leases-on-renew": True

#start server:
DHCP server is started.

Test Procedure:
Client does include IA-PD.
Client does NOT include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client copies server-id option from received message.
Client copies IA_PD option from received message.
Client does NOT include IA-NA.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client copies server-id option from received message.
Client copies IA_PD option from received message.
# Client does include IA-PD.
Client sends REBIND message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.
Response MUST include option 25.

@v6
Scenario: 7550_11
Test Setup:
Time preferred-lifetime is configured with value 300.
Time valid-lifetime is configured with value 400.
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
#subnet declarations:
#Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::100-2001:db8:1::200 pool.
Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
#Server is configured with another subnet on interface <interface> with 2001:db8:2::/64 subnet and 2001:db8:2::100-2001:db8:2::200 pool.
#Server is configured with 3002:: prefix in subnet 1 with 64 prefix length and 96 delegated prefix length.
#logger declarations (one is commented as and example)
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
#Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
Add to config file line: "new-leases-on-renew": True

#start server:
DHCP server is started.

Test Procedure:
Client does include IA-PD.
Client does NOT include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client copies server-id option from received message.
Client copies IA_PD option from received message.
Client does NOT include IA-NA.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client copies server-id option from received message.
Client copies IA_PD option from received message.
# Client does include IA-PD.
Client sends RENEW message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.
Response MUST include option 25.


@v6 @dhcp6 @PD @rfc3633
Scenario: prefix

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::3 pool.
Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
DHCP server is started.

Test Procedure:
Client does NOT include IA-NA.
Client does include IA-PD.
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 25.
Response option 25 MUST contain sub-option 26.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client does NOT include IA-NA.
Client copies server-id option from received message.
Client copies IA_PD option from received message.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 25.
Response option 25 MUST contain sub-option 26.


Test Procedure:
Client does NOT include IA-NA.
Client does include IA-PD.
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 25.
Response option 25 MUST contain sub-option 26.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
Client does NOT include IA-NA.
Client copies server-id option from received message.
Client copies IA_PD option from received message.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 25.
Response option 25 MUST contain sub-option 26.

@v6
Scenario: 7550_12
Test Setup:
Time preferred-lifetime is configured with value 300.
Time valid-lifetime is configured with value 400.
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
#subnet declarations:
Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
#Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
Add to config file line: "new-leases-on-renew": True

#start server:
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client copies server-id option from received message.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.



Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
Client does include IA-PD.
Client does NOT include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
Client copies server-id option from received message.
Client copies IA_PD option from received message.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
Client copies server-id option from received message.
Client copies IA_PD option from received message.
# Client does include IA-PD.
Client sends RENEW message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
@v6
Scenario: 7550_13
Test Setup:
Time preferred-lifetime is configured with value 300.
Time valid-lifetime is configured with value 400.
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
#subnet declarations:
Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
#Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
Add to config file line: "new-leases-on-renew": True
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
Client does include IA-PD.
Client does NOT include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
Client copies server-id option from received message.
Client copies IA_PD option from received message.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
Client copies server-id option from received message.
Client copies IA_PD option from received message.
Client sets T1 value to 0.
Client sets T2 value to 0.
Client sets validlft value to 0.
Client sets preflft value to 0.
Client sets IA_Address value to 3001::1.
Client does include IA_Address.

# Client does include IA-PD.
Client sends RENEW message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.
Response MUST include option 25.
@v6
Scenario: 7550_14
Test Setup:
Time preferred-lifetime is configured with value 300.
Time valid-lifetime is configured with value 400.
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
#subnet declarations:
Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
Server is configured with 3000:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
#Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
Add to config file line: "new-leases-on-renew": True
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client copies server-id option from received message.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.


Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
Client does include IA-PD.
Client does NOT include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
Client copies server-id option from received message.
Client copies IA_PD option from received message.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
Client copies server-id option from received message.
Client copies IA_PD option from received message.
Client sets T1 value to 0.
Client sets T2 value to 0.
Client sets validlft value to 0.
Client sets preflft value to 0.
Client sets IA_Address value to 3000::1.
Client does include IA_Address.

# Client does include IA-PD.
Client sends REBIND message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.
Response MUST include option 25.