__author__ = 'gaoxindai'


# coordinate_range factor
span_fac = 1
# number of beauties displayed
beauty_list_len = 50
# length of sample data to calculate average score
random_sample = 100
# server timezone
server_tz = 'US/Pacific'
# Api to get access token
get_access_token_api = "https://graph.facebook.com/oauth/access_token?client_id=616639911775014&" \
                       "client_secret=55ac4775709b528d382838107c2f6838&grant_type=client_credentials"
# validate FB token api
validate_fb_token_api = "https://graph.facebook.com/debug_token?input_token=%s&" \
                        "access_token=%s"
# validate receipt
validate_receipt_api = "https://sandbox.itunes.apple.com/verifyReceipt"