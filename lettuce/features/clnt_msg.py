from init_all import PROTO, SOFTWARE_UNDER_TEST
from lettuce import world, step
import importlib

# TODO: write some comments what particular functions do; file's getting messy.

if PROTO == "v6":
    clntMsg = importlib.import_module("protosupport.%s.clnt_msg"  % (PROTO))
    borrowedSteps = importlib.import_module("protosupport.%s.srv_msg"  % (PROTO))

##############   getting client message   ##############

    @step("Sniffing client (\S+) message from network.")
    def client_msg_capture(step, msgType):
        clntMsg.client_msg_capture(step, msgType)

##############   validating received message   ##############

    @step("Client MUST (NOT )?respond with (\S+) message.")
    def client_send_receive(step, yes_no, msgType):
        contain = not (yes_no == "NOT ")
        clntMsg.client_send_receive(step, contain, msgType)

    @step("Client message MUST (NOT )?contain option (\d+).")
    def client_msg_contains_opt(step, yes_or_no, opt):
        contain = not (yes_or_no == "NOT ")
        clntMsg.client_msg_contains_opt(step, contain, opt)

    @step("Client message MUST (NOT )?contain (\d+) options with opt-code (\d+).")
    def client_msg_count_opt(step, yes_no, count, optcode):
        contain = not (yes_no == "NOT ")
        clntMsg.client_msg_count_opt(step, contain, count, optcode)

    @step("Client message MUST (NOT )?contain (\d+) sub-options with opt-code (\d+) within option (\d+).")
    def client_msg_count_subopt(step, yes_no, count, subopt_code, opt_code):
        contain = not (yes_no == "NOT ")
        clntMsg.client_msg_count_subopt(step, contain, count, subopt_code, opt_code)

    @step("Client message MUST (NOT )?contain (\S+) field in option (\d+).")
    def client_check_field_presence(step, yes_no, field, optcode):
        contain = not (yes_no == "NOT ")
        clntMsg.client_check_field_presence(step, contain, field, optcode)

    @step("Client message option (\d+) MUST (NOT )?include sub-option (\d+).")
    def client_msg_contains_subopt(step, opt_code, yes_or_no, subopt_code):
        contain = not (yes_or_no == "NOT ")
        clntMsg.client_msg_contains_subopt(step, opt_code, contain, subopt_code)

    @step("Message was sent after at least (\S+) second.")
    def client_check_time_delay(step, timeval):
        preciseTimeVal = float(timeval)
        clntMsg.client_check_time_delay(step, preciseTimeVal)

    @step("(\S+) value in client message is the same as saved one.")
    def client_cmp_values(step, value):
        clntMsg.client_cmp_values(step, value)

    @step("Client message sub-option (\d+) from option (\d+) MUST (NOT )?contain (\S+) (\S+).")
    def client_subopt_check_value(step, subopt_code, opt_code, yes_or_no, value_name, value):
        expect = not (yes_or_no == "NOT ")
        clntMsg.client_subopt_check_value(step, subopt_code, opt_code, expect, value_name, value)

    @step("Client message option (\d+) MUST (NOT )?contain (\S+) (\S+).")
    def client_opt_check_value(step, opt_code, yes_or_no, value_name, value):
        expect = not (yes_or_no == "NOT ")
        clntMsg.client_opt_check_value(step, opt_code, expect, value_name, value)

##############   building server message   #############

    @step("Server builds new message.")
    def srv_msg_clean(step):
        clntMsg.srv_msg_clean(step)

    @step("Server sets wrong (\S+) value.")
    def server_set_wrong_val(step, value):
        clntMsg.server_set_wrong_val(step, value)

    @step("(\S+) value is set to (\S+).")
    def server_sets_value(step, value_name, new_value):
        clntMsg.msg_set_value(step, value_name, new_value)

    @step("Server adds (\S+) (\d+ )?option to message.")
    def add_option(step, opt, optcode):
        clntMsg.add_option(step, opt, optcode)

    @step("Server adds another (\S+) option to message.")
    def add_another_option(step, opt):
        clntMsg.add_another_option(step, opt)

    @step("Server sends (back )?(\S+) message.")
    def server_build_msg(step, back, msgType):
        response = not (back == "back ")
        clntMsg.server_build_msg(step, response, msgType)

else:
    pass
