
Feature: DHCPv6 Relay Agent 
    This is test for DHCPv6 message exchange between server and relay-agent with not permitted options in Relay-Forward message.  

@v6 @relay @relay_invalid
    Scenario: v6.relay.invalid.with_client_id

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include wrong-client-id.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8	
	
@v6 @relay @relay_invalid
    Scenario: v6.relay.invalid.with_server_id
	#add just serverid
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include wrong-server-id.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8

@v6 @relay @relay_invalid
    Scenario: v6.relay.invalid.opt_req
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client requests option 7.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8

@v6 @relay @relay_invalid @invalid_option @outline
    Scenario Outline: v6.relay.invalid.options.outline
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.
	
	#add options to relay message
	Client does include <opt_name>.
	...using relay-agent encapsulated in 1 level.
	
	Pass Criteria:
	Server MUST NOT respond with RELAYREPLY message.

	References: RFC3315 section 18.2.8
	
	Examples:
	| opt_name           |
	| preference         |
	| time               |
	| server-unicast     |
	| status-code        |
	| rapid-commit       |
	| reconfigure        |
	| reconfigure-accept |